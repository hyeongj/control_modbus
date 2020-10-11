from threading import Lock, Thread, Event
from flask import Flask, render_template, session, request, Response,jsonify,redirect, url_for
from flask_socketio import SocketIO, emit, disconnect
import os, sys, time
import json 
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import numpy as np
import matplotlib.pylab as plt
import eventlet
eventlet.monkey_patch() 

import sqlalchemy as db
from io import BytesIO
import base64
#===global variables==============================
POSTGRES = {
    'user': 'coned_postgres',
    'pw': 'Wz1Sc3Ac2E3ff5k4mSdE',
    'db': 'postgres',
    'host': 'coned-database-1.c0bhgyjg3dyh.us-east-2.rds.amazonaws.com',
    'port': '5432',
}
DATABASE_URL='postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES



# ========================================

THREAD_LOCK = Lock()
LIVEGRAPH=False
BACKGROUND_READING = True
MODBUS_CONN=False
JSONDATA={}
USERCOUNT=0 
THREAD = None
SQL_CON=None 
cli = None
CON = "SQL SERVER NOT CONNECTED"
DEMO='172.16.81.133'
DIS='0.0.0.0'
 
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

def matplotimage():
	global SQL_CON,JSONDATA
	if SQL_CON!=None:	
		# select last column of waveform data
		cmd = 'SELECT "TIME_CREATED", "CHS", "RATE", "WAVEFORM" from tbconed WHERE "WAVEFORM" IS NOT NULL ORDER BY ID DESC LIMIT 1;' 
		result=SQL_CON.execute(cmd)
		for row in result:
			tmp=row

		gtime=tmp[0]
		gchs=tmp[1]
		rate=tmp[2]
		gwave=np.frombuffer(tmp[3], dtype="Int8")
		crate=50

		if rate == 0:
			crate = 50
		if rate == 1:
			crate = 25
		if rate == 2:
			crate = 12.5
		if rate == 3:
			crate = 6.25

		buffer = len(gwave)
		xvalue = [x/crate for x in range(buffer)]
		

		plt.figure(figsize=(13,4.5))
		plt.clf()
		plt.title(f'Captured time : {gtime}')
		plt.plot(xvalue, gwave,'k-', linewidth=0.5, label = f'Channel = {gchs}')
		plt.grid(which='both', linestyle='-', linewidth='0.5', color='black')
		plt.legend(loc=1)
		plt.xlabel("Time (us)",fontsize="13")
		plt.ylabel("Amplitude",fontsize="13")

		figfile = BytesIO()
		plt.savefig(figfile, format='png')
		figfile.seek(0)  # rewind to beginning of file
		figdata_png = figfile.getvalue()  # extract string (stream of bytes)
		
		figdata_png = base64.b64encode(figdata_png)
		
		return figdata_png


# ==============================================================
@app.route('/')
def base():
	# global resultfig,SQL_CON
	# engine = db.create_engine(DATABASE_URL)
	# SQL_CON = engine.connect()
	# resultfig=matplotimage()
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
	global BACKGROUND_READING, cli, MODBUS_CONN, JSONDATA, CON,SQL_CON
	cnt=0
 
  #===========================================================
	while True:
		if MODBUS_CONN:
			out=" On"
		else:
			out=" Off"
		socketio.emit('modbus_response',{'data': out },namespace='/test')
		if SQL_CON!=None:
			CON = "SQL SERVER CONNECTED"
		else:
			CON = "SQL SERVER NOT CONNECTED" 
 
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
				,  '_CNT_THRESHOLD':MODBUS_DATA[18], '_SQL_CONN':CON
				}
				# print(JSONDATA)
				# socketio.emit('my_rate_response',JSONDATA,namespace='/test')			 
				MODBUS_CONN=True
			 		
			except:
				MODBUS_CONN=False
				JSONDATA={'_speed':0, '_buffer':0,'_time_in':0, '_maxth':0, '_gain':0, '_rate':0, 
				'_sel_channel':0, '_sel_amp':0,  '_height1':0,  '_height2':0,  '_height3':0,  '_height4':0,
				'_humidity':0,  '_temp1':0,  '_temp2':0,  '_temp3':0
				,  '_CNT_THRESHOLD':0, '_SQL_CONN':CON
				}
				print(f'waiting....{cnt}')
				cnt+=1
				socketio.sleep(1)

			socketio.emit('my_rate_response',JSONDATA,namespace='/test')	
		
		else:
			print('pause')
			MODBUS_CONN=False
			socketio.sleep(1)




 


# ====Count connect user number==========================================
 
 
@socketio.on('disconnect', namespace='/test')
def test_disconnect():
	global USERCOUNT, SQL_CON, cli
	USERCOUNT-=1
	print(f'Client #{USERCOUNT} connected')	

	if SQL_CON !=None:
		SQL_CON.close()
		SQL_CON = None
	modconnect(DIS)
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
		# cli.read_input_registers(30001,1)
		BACKGROUND_READING=True
		MODBUS_CONN=True
		print(f"{IP} Connected")
	except:
		print(f"{IP} not Connected")
		BACKGROUND_READING=False
		MODBUS_CONN=False

# =========BUTTON==========================================
@socketio.on('start_request', namespace='/test')
def get_request():
	global BACKGROUND_READING
	BACKGROUND_READING= not BACKGROUND_READING
	
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'BACKGROUND_READING - %s'%BACKGROUND_READING, 'count': session['receive_count']})

@socketio.on('init_request', namespace='/test')
def get_request():
	cli.write_coil(1011,0)  #1019 True	
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'Initialized', 'count': session['receive_count']})


@socketio.on('gain0_request', namespace='/test')
def get_request():
	cli.write_coil(1012,0)  #1019 True	
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'Increase gain', 'count': session['receive_count']})

@socketio.on('gain1_request', namespace='/test')
def get_request():
	cli.write_coil(1013,0)  #1019 True	
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'Lower gain', 'count': session['receive_count']})

@socketio.on('amp0_request', namespace='/test')
def get_request():
	cli.write_coil(1014,0)  #1019 True	
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'Increase threshold amplitude', 'count': session['receive_count']})

@socketio.on('amp1_request', namespace='/test')
def get_request():
	cli.write_coil(1015,0)  #1019 True	
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'Lower threshold amplitude', 'count': session['receive_count']})

@socketio.on('ttime0_request', namespace='/test')
def get_request():
	cli.write_coil(1016,0)  #1019 True	
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'Increase threshold time', 'count': session['receive_count']})
 
@socketio.on('ttime1_request', namespace='/test')
def get_requesth():
	cli.write_coil(1017,0)  #1019 True	
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'Lower threshold time', 'count': session['receive_count']})

@socketio.on('sinterval0_request', namespace='/test')
def get_request():
	cli.write_coil(1035,0)  #1019 True	
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'Increase interval', 'count': session['receive_count']})
 
@socketio.on('sinterval1_request', namespace='/test')
def get_requesth():
	cli.write_coil(1035,1)  #1019 True	
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'Lower interval', 'count': session['receive_count']})

@socketio.on('rate0_request', namespace='/test')
def get_request():
	cli.write_coil(1003,0)  #1019 True
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'Rate = 50 MHz', 'count': session['receive_count']})

@socketio.on('rate1_request', namespace='/test')
def get_request():
	cli.write_coil(1004,0)  #1019 True
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'Rate = 25 MHz', 'count': session['receive_count']})

@socketio.on('rate2_request', namespace='/test')
def get_request():
	cli.write_coil(1005,0)  #1019 True
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'Rate = 12.5 MHz', 'count': session['receive_count']})

@socketio.on('rate3_request', namespace='/test')
def get_request():
	cli.write_coil(1006,0)  #1019 True	
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'Rate = 6.25 MHz', 'count': session['receive_count']})


@socketio.on('BUFFER0_request', namespace='/test')
def get_request():
	cli.write_coil(1026,0)  #1019 True
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'BUFFER = 1000', 'count': session['receive_count']})

@socketio.on('BUFFER1_request', namespace='/test')
def get_request():
	cli.write_coil(1027,0)  #1019 True
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'BUFFER = 2000', 'count': session['receive_count']})

@socketio.on('BUFFER2_request', namespace='/test')
def get_request():
	cli.write_coil(1028,0)  #1019 True
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'BUFFER = 4000', 'count': session['receive_count']})

@socketio.on('BUFFER3_request', namespace='/test')
def get_request():
	cli.write_coil(1029,0)  #1019 True	
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': 'BUFFER = 8000', 'count': session['receive_count']})
			
# ================================

@socketio.on('ch0_request', namespace='/test')
def get_request():
	ad = "CH0"
	cli.write_coil(1007,0)  #1019 True
	cli.write_coil(1036,0)  #1019 True
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': '"%s" SAVED'%ad, 'count': session['receive_count']})
 
 
@socketio.on('ch1_request', namespace='/test')
def get_request():
	ad = "CH1"
	cli.write_coil(1008,0)  #1019 True
	cli.write_coil(1036,0)  #1019 True
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': '"%s" SAVED'%ad, 'count': session['receive_count']})
 

@socketio.on('ch2_request', namespace='/test')
def get_request():
	ad = "CH2"
	cli.write_coil(1009,0)  #1019 True
	cli.write_coil(1036,0)  #1019 True
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_send_response',
			{'data': '"%s" SAVED'%ad, 'count': session['receive_count']})
 

@socketio.on('ch3_request', namespace='/test')
def get_request():
	ad = "CH3"
	cli.write_coil(1010,0)  #1019 True
	cli.write_coil(1036,0)  #1019 True	
	session['receive_count'] = session.get('receive_count', 0) + 1
	socketio.emit('my_send_response',
			{'data': '"%s" SAVED'%ad, 'count': session['receive_count']})
 


 


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

@socketio.on('SQL_request', namespace='/test')
def get_requesth():
	global CON, SQL_CON
	engine = db.create_engine(DATABASE_URL)
	SQL_CON = engine.connect()
 
	 
@socketio.on('SQL_d_request', namespace='/test')
def get_requesth():
	global CON, SQL_CON
	SQL_CON.close()
	SQL_CON = None
	
@socketio.on('matplot_request', namespace='/test')
def get_sqlrequesth():
	resultfig=matplotimage()
	resultfig=resultfig.decode('utf8')
	socketio.emit('my_sql_response',{'data': resultfig },namespace='/test')

	 
 

#=================================================
if __name__ == '__main__':
	socketio.run(app,host='0.0.0.0', port=5000)
