from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time
 



iIP ='127.0.0.1' 
# iIP ='192.168.1.42' 

def modconnect(IP):
	PORT=1502
	cli = ModbusClient(host=IP, port=PORT)
	return cli

 
try: 
	cli=modconnect(iIP)
	print("Connected")
except:
	print("Not connected!")

x=9

while x!=0:
	x= input("Enter MODBUS Commend? ")
	x=int(x)
	if x>1000 and x<1030:
		cli.write_coil(x,1)
	if x>1030 and x<1040:
		y=input("enter 0 or 1?")
		cli.write_coil(x,y)
	if x==3000:
		MODBUS_GET=cli.read_holding_registers(40001,19)
		time.sleep(0.5)
		MODBUS_DATA=MODBUS_GET.registers
		'''
		_temp1 = box temp
		_temp2 = TR1 temp
		_temp3 = TR2 temp
		'''
		JSONDATA={'_speed':MODBUS_DATA[0], '_buffer':(MODBUS_DATA[2]-1)*100,'_time_in':MODBUS_DATA[1], '_maxth':MODBUS_DATA[3], '_gain':MODBUS_DATA[4],
					 '_rate':MODBUS_DATA[5], '_sel_channel':MODBUS_DATA[8], '_sel_amp':MODBUS_DATA[9],  
					'_height1':MODBUS_DATA[10]/10,  '_height2':MODBUS_DATA[11]/10,  '_height3':MODBUS_DATA[12]/10,  '_height4':MODBUS_DATA[13]/10,
					'_humidity':MODBUS_DATA[15],  '_temp1':MODBUS_DATA[14],  '_temp2':MODBUS_DATA[16],  '_temp3':MODBUS_DATA[17],
					 '_CNT_THRESHOLD':MODBUS_DATA[18]
				}
		# tof1 = 1e6*2*JSONDATA["_height1"]*0.0254/JSONDATA["_speed"]
		# tof2 = 1e6*2*JSONDATA["_height2"]*0.0254/JSONDATA["_speed"]
		# tof3 = 1e6*2*JSONDATA["_height3"]*0.0254/JSONDATA["_speed"]
		# tof4 = 1e6*2*JSONDATA["_height4"]*0.0254/JSONDATA["_speed"]

		print(f'CHANNEL: {JSONDATA["_sel_channel"]}')
		print(f'RATE, Buffer: {JSONDATA["_rate"]}, {JSONDATA["_buffer"]}')
		print(f'Threshold Time / Amp: {JSONDATA["_time_in"]} / {JSONDATA["_maxth"]}')
		print(f'TR1 Height: {JSONDATA["_height1"],JSONDATA["_height2"],JSONDATA["_height3"],JSONDATA["_height4"]}  inch')
		print(f'Humidity: {JSONDATA["_humidity"]} %')
		print(f'Box, TR1, TR2 Temp: {JSONDATA["_temp1"],JSONDATA["_temp2"],JSONDATA["_temp3"]}')
		

'''
select
		CMD	    HEX	    COMMENTS	VALUE		DEC	**HEX**	CHAR
		1001	0X3E9	Set speed	1500		48	**30**	  0
		1002	0X3EA	Set speed	6000		49	**31**	  1
		1003	0X3EB	SET RATE	0			50	**32**	  2
		1004	0X3EC	SET RATE	1			51	**33**	  3
		1005	0X3ED	SET RATE	2			52	**34**	  4
		1006	0X3EE	SET RATE	3			53	**35**	  5
		1007	0X3EF	Set Channel	0			54	**36**	  6
		1008	0X3F0	Set Channel	1			55	**37**	  7
		1009	0X3F1	Set Channel	2			56	**38**	  8
		1010	0X3F2	Set Channel	3			57	**39**	  9
		1011	0X3F3	INITIAL					58	**3A**	  :
		1012	0X3F4	gain +=20				59	**3B**	  ;
		1013	0X3F5	gain -=20				60	**3C**	  <
		1014	0X3F6	maxth +=20				61	**3D**	  =
		1015	0X3F7	maxth -+20				62	**3E**	  >
		1016	0X3F8	timein +=1				63	**3F**	  ?
		1017	0X3F9	timin -=1				64	**40**	  @
		1018	0X3FA	speed +=4				65	**41**	  A
		1019	0X3FB	speed -=4				66	**42**	  B
		1020	0X3FC	SAVE WAVE				67	**43**	  C
		1021	0X3FD	USBUT-ON				68	**44**	  D
		1022	0X3FE	Rectifier	0			69	**45**	  E
		1023	0X3FF	Rectifier	3			70	**46**	  F
		1024	0X400	SHOW Graph				71	**47**	  G
		1025	0X401	GRAPH OFF				72	**48**	  H
		1026	0X402	buffer		1000		73	**49**	  I
		1027	0X403	buffer		2000		74	**4A**	  J
		1028	0X404	buffer		4000		75	**4B**	  K
		1029	0X405	buffer		8000		76	**4C**	  L
		1030	0x406	DYNAMIC FALSE (0)		
		1031	0x407	Reconnect Arduino)      
		1032	0x408	Reconnect USBUT         
		1033	0x409	Reconnect SQL           
		1034	0x40A	ARDUINO DIO1ON -REBOOT		
		1035	0x40B	CNT SAVING count	 
		1036	0x40C	WAVEFORM
		1037	0x40D	CNT SAVING 10/1000 

'''

