import corr, time, numpy, struct, sys,socket
import matplotlib.pyplot as plt



pkt_period = 1024#100  #in FPGA clocks (200MHz) la cague
payload_len = 900#50   #in 64bit words

gen_rate = 1.*payload_len/pkt_period*135
tge_rate = gen_rate/(8./10*156.25)*10
print('data rate: %.2f GSa/s' %(tge_rate))

dest_ip  =192*(2**24) + 168*(2**16) + 0*(2**8)+29#10*(2**24) + 30 #10.0.0.30
fabric_port=60000         
source_ip=10*(2**24) + 20 #10.0.0.20
mac_base=(2<<40) + (2<<32)
ip_prefix='10. 0. 0.'     #Used for the purposes of printing output.


tx_core_name = 'gbe0'
rx_core_name = 'gbe1'


fpga = corr.katcp_wrapper.FpgaClient('192.168.0.40')
time.sleep(1)
bof = 'gbe_ex2.bof.gz'#'gbe_ex.bof.gz'
fpga.upload_program_bof(bof, 3000)
time.sleep(1)



fpga.tap_start('rx_tap',rx_core_name,mac_base+dest_ip,dest_ip,fabric_port)
fpga.tap_start('tx_tap',tx_core_name,mac_base+source_ip,source_ip,fabric_port)


fpga.write_int('packet_period',pkt_period)
fpga.write_int('packet_payload_len',payload_len)

fpga.write_int('dest_ip',dest_ip)
fpga.write_int('dest_port',fabric_port)



fpga.write_int('gbe_rst',1)
fpga.write_int('gbe_rst',0)
fpga.write_int('cnt_rst',1)
fpga.write_int('cnt_rst',0)

fpga.write_int('packet_enable',1)
time.sleep(2)

rx_data = struct.unpack('>16384Q', fpga.read('rx_data', 2**14*8))
#rx_data = struct.unpack('>1024Q',fpga.read('rx_data',1024*8))
tx_data = struct.unpack('>1024Q',fpga.read('tx_data',1024*8))


fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)


ax1.plot(tx_data)
ax1.set_title('tx_data')
ax1.grid()
ax2.plot(rx_data)
ax2.set_title('rx_data')
ax2.grid()

plt.show()
