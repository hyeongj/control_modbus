from threading import Lock, Thread, Event
from flask import Flask, render_template, session, request, Response,jsonify,redirect, url_for
from flask_socketio import SocketIO, emit, disconnect
import os, sys, time
import json 
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

import eventlet
eventlet.monkey_patch() 
#===global variables==============================


THREAD_LOCK = Lock()
LIVEGRAPH=False
BACKGROUND_READING = False
MODBUS_CONN=False

USERCOUNT=0 
THREAD = None
MODBUS_CONNECT = None
cli = None

DEMO='172.16.81.133'
# ========================================

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(50)
app.config['DEBUG'] = True 
socketio = SocketIO(app)    
# =====================================+

def modconnect(IP):
	global cli
	PORT=1502
	cli = ModbusClient(host=IP, port=PORT)


# ==============================================================
@app.route('/')
def base():
   return render_template('index.html')

##==============================================

@socketio.on('connect', namespace='/test')
def test_connect(): 
	global THREAD, MODBUS_CONNECT, USERCOUNT, BACKGROUND_READING
	USERCOUNT += 1
	print(f'Client #{USERCOUNT} connected')
	BACKGROUND_READING=True
	if THREAD is None:
		with THREAD_LOCK:	
			THREAD = socketio.start_background_task(BACKGROUND_PULSER)
			# socketio.start_background_task(BACKGROUND_GRAPH)

	socketio.emit('my_count_response',{'data': 'Current User - %d'%USERCOUNT},namespace='/test')

#//background Read values from read holding registers.....

def BACKGROUND_PULSER():
	global BACKGROUND_READING, cli, MODBUS_CONN
	cnt=0
 
  #===========================================================
	while True:
		if MODBUS_CONN:
			out=" On"
		else:
			out=" Off"
		socketio.emit('modbus_response',{'data': out },namespace='/test')
		 
		if BACKGROUND_READING:
			try:
				#read input register 	
				MODBUS_GET=cli.read_holding_registers(40001,19)
				socketio.sleep(1)
				MODBUS_DATA=MODBUS_GET.registers
 
				JSONDATA={'_speed':MODBUS_DATA[0], '_buffer':(MODBUS_DATA[2]-1)*100,'_time_in':MODBUS_DATA[1], '_maxth':MODBUS_DATA[3], '_gain':MODBUS_DATA[4], '_rate':MODBUS_DATA[5], 
				'_sel_channel':MODBUS_DATA[8], '_sel_amp':MODBUS_DATA[9],  
				'_height1':MODBUS_DATA[10]/10,  '_height2':MODBUS_DATA[11]/10,  '_height3':MODBUS_DATA[12]/10,  '_height4':MODBUS_DATA[13]/10,
				'_humidity':MODBUS_DATA[15],  '_temp1':MODBUS_DATA[14],  '_temp2':MODBUS_DATA[16],  '_temp3':MODBUS_DATA[17]
				,  '_CNT_THRESHOLD':MODBUS_DATA[18]
				}
				# print(JSONDATA)
				socketio.emit('my_rate_response',JSONDATA,namespace='/test')			 
				MODBUS_CONN=True
			 		
			except:
				MODBUS_CONN=False
				print(f'waiting....{cnt}')
				cnt+=1
				socketio.sleep(1)
 
		else:
			print('pause')
			MODBUS_CONN=False
			socketio.sleep(1)



# ====Count connect user number==========================================
 
 
@socketio.on('disconnect', namespace='/test')
def test_disconnect():
	global USERCOUNT
	USERCOUNT-=1

	print(f'Client #{USERCOUNT} connected')
 
	socketio.emit('my_count_response',{'data': 'Current User - %d'%USERCOUNT},namespace='/test')


#====================================================+

	
# ==============SEND COMMANDS= (REGISTER #)==================================================================
@socketio.on('send_event_request', namespace='/test')
def test_message(message):
	global cli, livefigure,BACKGROUND_READING
	ad=str(message['data'])
	''' write Coil'''

	if ad.find("0x")>=0:
		addr=int(ad,0)  #conver hex to decimal
		print(addr)
		print('Message Sent')
		cli.write_coil(addr,0)


	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'Command: "%s"'%ad , 'count': session['receive_count']})
 

 #======================TCP/IP NETWORK IP connect form===================================
@socketio.on('my_event_request', namespace='/test')
def test_message3(message):
	''' IP change '''
	global BACKGROUND_READING, cli, MODBUS_CONN
	IP=str(message['data'])
	if IP=='DEMO':
		#DEMO=nslookup()
		IP=DEMO
	
	try:
		modconnect(IP)
		cli.read_input_registers(30001,1)
		BACKGROUND_READING=True
		MODBUS_CONN=True
		print(f"{IP} Connecting")
	except:
		print(f"{IP} not Connected")
		BACKGROUND_READING=False
		MODBUS_CONN=False

# =========BUTTON==========================================
@socketio.on('start_request', namespace='/test')
def get_request():
	global BACKGROUND_READING
	BACKGROUND_READING= not BACKGROUND_READING

@socketio.on('init_request', namespace='/test')
def get_request():
	cli.write_coil(1011,0)  #1019 True	


@socketio.on('gain0_request', namespace='/test')
def get_request():
	cli.write_coil(1012,0)  #1019 True	

@socketio.on('gain1_request', namespace='/test')
def get_request():
	cli.write_coil(1013,0)  #1019 True	

@socketio.on('amp0_request', namespace='/test')
def get_request():
	cli.write_coil(1014,0)  #1019 True	
	print("1014")

@socketio.on('amp1_request', namespace='/test')
def get_request():
	cli.write_coil(1015,0)  #1019 True	

@socketio.on('ttime0_request', namespace='/test')
def get_request():
	cli.write_coil(1016,0)  #1019 True	
 
@socketio.on('ttime1_request', namespace='/test')
def get_requesth():
	cli.write_coil(1017,0)  #1019 True	

@socketio.on('sinterval0_request', namespace='/test')
def get_request():
	cli.write_coil(1035,0)  #1019 True	
 
@socketio.on('sinterval1_request', namespace='/test')
def get_requesth():
	cli.write_coil(1035,1)  #1019 True	

@socketio.on('rate0_request', namespace='/test')
def get_request():
	cli.write_coil(1003,0)  #1019 True
	print('ok')

@socketio.on('rate1_request', namespace='/test')
def get_request():
	cli.write_coil(1004,0)  #1019 True

@socketio.on('rate2_request', namespace='/test')
def get_request():
	cli.write_coil(1005,0)  #1019 True

@socketio.on('rate3_request', namespace='/test')
def get_request():
	cli.write_coil(1006,0)  #1019 True	

# ================================

@socketio.on('ch0_request', namespace='/test')
def get_request():
	cli.write_coil(1007,0)  #1019 True
	cli.write_coil(1020,0)  #1019 True
 
@socketio.on('ch1_request', namespace='/test')
def get_request():
	cli.write_coil(1008,0)  #1019 True
	cli.write_coil(1020,1)  #1019 True

@socketio.on('ch2_request', namespace='/test')
def get_request():
	cli.write_coil(1009,0)  #1019 True
	cli.write_coil(1020,0)  #1019 True

@socketio.on('ch3_request', namespace='/test')
def get_request():
	cli.write_coil(1010,0)  #1019 True
	cli.write_coil(1020,0)  #1019 True	


 


# ==============GRAPH===================================================================

@socketio.on('graph_request', namespace='/test')
def get_requesth():
	global LIVEGRAPH
	LIVEGRAPH=True
	cli.write_coil(1024,0)  #1019 True	
	print("graph on")
 
@socketio.on('graphoff_request', namespace='/test')
def get_requesth():
	global LIVEGRAPH
	LIVEGRAPH=False
	cli.write_coil(1025,0)  #1019 True	
	print("graph off")

@socketio.on('REBOOT_request', namespace='/test')
def get_requesth():
	cli.write_coil(1034,1)  #1019 True	
	print("Arduino ON/OFF")


#=================================================
if __name__ == '__main__':
	socketio.run(app,host='0.0.0.0', port=5000)
