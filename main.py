from flask import Flask, render_template, session, request, Response,jsonify,redirect, url_for
from flask_socketio import SocketIO, emit, disconnect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import json
import pandas as pd

import os, sys, time
import eventlet
eventlet.monkey_patch() 

#===global variables==============================

USERCOUNT=0
PASSWORD = 'password' 	 
# =================
_SQL_TIME=[]
_SQL_VARIABLE1 = []
_SQL_VARIABLE2 = []
_SQL_VARIABLE3 = []
_SQL_VARIABLE4 = []
_SQL_VARIABLE5 = []
_SQL_VARIABLE6 = []
_SQL_VARIABLE7 = []
_SQL_VARIABLE8 = []
_SQL_VARIABLE9 = []

_OBJ=None
# ---------------------

# ======================================================================================== 
POSTGRES = {
    'user': 'coned_postgres',
    'pw': 'Wz1Sc3Ac2E3ff5k4mSdE',
    'db': 'postgres',
    'host': 'coned-database-1.c0bhgyjg3dyh.us-east-2.rds.amazonaws.com',
    'port': '5432',
}
DATABASE_URL='postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
# ========================================================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(50)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['DEBUG'] = False 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)    
# =====================================+

def READSQLDATA(dbname):
	yy=dbname.query.all()
	val=[[] for _ in range(10)]	
	fmt='%B %d %H:%M'
	

	for j in yy:
		tmp=j.TIME_CREATED
		conv=tmp.replace(microsecond=0).strftime(fmt)
		val[0].append(conv)
		val[1].append(j.HEIGHT1)
		val[2].append(j.HEIGHT2)
		val[3].append(j.HEIGHT3)
		val[4].append(j.HEIGHT4)
		val[5].append(j.HUMIDITY)
		val[6].append(j.BOX_TEMP)
		val[7].append(j.SBC_TEMP)
		val[8].append(j.TRANS1_TEMP)
		val[9].append(j.TRANS2_TEMP)
		
 
	pydic={ 'Time (GMT)'    : val[0], 
			'Sensor#1 (in)' : val[1],
			'Sensor#2 (in)' : val[2],
			'Sensor#3 (in)' : val[3],
			'Sensor#4 (in)' : val[4],
			'HUMIDITY (%)'  : val[5], 
			u"Box (\u2103)" : val[6],
			u"SBC (\u2103)" : val[7], 
			u"TR#1 (\u2103)": val[8], 
			u"TR#2 (\u2103)": val[9]
			}
 
	df=pd.DataFrame(pydic)
 
	return df


class dbconed(db.Model):
	__tablename__ = 'tbconed'
 
	id = db.Column(db.Integer, primary_key=True)
	TIME_CREATED = db.Column(db.DateTime(timezone=True), server_default=func.now())
	GAIN = db.Column(db.Integer, unique=False, nullable=True)
	THRES_T = db.Column(db.Float, unique=False, nullable=True)
	THRES_A = db.Column(db.Integer, unique=False, nullable=True)
	RATE = db.Column(db.Integer, unique=False, nullable=True)
	CHS = db.Column(db.Integer, unique=False, nullable=True)
	AMP = db.Column(db.Integer, unique=False, nullable=True)
	TOF = db.Column(db.Float, unique=False, nullable=True)
	HEIGHT1 = db.Column(db.Float, unique=False, nullable=True)
	HEIGHT2 = db.Column(db.Float, unique=False, nullable=True)
	HEIGHT3 = db.Column(db.Float, unique=False, nullable=True)
	HEIGHT4 = db.Column(db.Float, unique=False, nullable=True)
	BOX_TEMP = db.Column(db.Integer, unique=False, nullable=True)
	HUMIDITY = db.Column(db.Integer, unique=False, nullable=True)
	TRANS1_TEMP = db.Column(db.Integer, unique=False, nullable=True)
	TRANS2_TEMP = db.Column(db.Integer, unique=False, nullable=True)
	SBC_TEMP = db.Column(db.Integer, unique=False, nullable=True)
	WAVEFORM = db.Column(db.LargeBinary, unique=False, nullable=True)
	

	def __repr__(self):
		return '<tbconed %r>' % self.HUMIDITY

# ==============================================================
@app.route('/')
def base():
   return render_template('base.html')

@app.route('/client',methods = ['POST', 'GET'])
def client():
	if request.method == 'POST':
		client = request.form
	if client['Name'] == PASSWORD:
		try:	
			df=READSQLDATA(dbconed)
			# print('success')
			_OBJ=df.to_html(classes='tdata', header="true",table_id="example")
 
		except:
			# print('failed to read')
			pydic={ 'Time (GMT)' :[], 
				'Sensor#1 (in)'  : [],
				'Sensor#2 (in)'  : [],
				'Sensor#3 (in)'  : [],
				'Sensor#4 (in)'  : [],
				'HUMIDITY (%)'   : [], 
				u"Box (\u2103)"  : [],
				u"SBC (\u2103)"  : [], 
				u"TR#1 (\u2103)" : [], 
				u"TR#2 (\u2103)" : []
			}

	 
			df=pd.DataFrame(pydic)
			_OBJ=df.to_html(classes='tdata', header="true",table_id="example")
	 
 
		return render_template("index.html", tables=[_OBJ])
	else:
		return redirect(url_for('base'))

# ==============================================================

@app.route('/historydata')
def historydata():
	''' This is history plot from SQL'''
	
	df=READSQLDATA(dbconed)
	# print( df['HEIGHT 1'])
	try:
		df=READSQLDATA(dbconed)
		_SQL_TIME	   = df['Time (GMT)'].values.tolist()
		_SQL_VARIABLE1 = df['Sensor#1 (in)'].values.tolist()	
		_SQL_VARIABLE2 = df['Sensor#2 (in)'].values.tolist()	
		_SQL_VARIABLE3 = df['Sensor#3 (in)'].values.tolist()	
		_SQL_VARIABLE4 = df['Sensor#4 (in)'].values.tolist()
		_SQL_VARIABLE5 = df['Box (\u2103)'].values.tolist()
		_SQL_VARIABLE6 = df['HUMIDITY (%)'].values.tolist()
		_SQL_VARIABLE7 = df['SBC (\u2103)'].values.tolist()	
		_SQL_VARIABLE8 = df['TR#1 (\u2103)'].values.tolist()	
		_SQL_VARIABLE9 = df['TR#2 (\u2103)'].values.tolist()			
 
	
	except:
		_SQL_TIME=[]
		_SQL_VARIABLE1=[]
		_SQL_VARIABLE2=[]
		_SQL_VARIABLE3=[]
		_SQL_VARIABLE4=[]
		_SQL_VARIABLE5=[]
		_SQL_VARIABLE6=[]
		_SQL_VARIABLE7=[]
		_SQL_VARIABLE8=[]
		_SQL_VARIABLE9=[]

	jsontable = {
				'Date': _SQL_TIME, 
				'HEIGHT1': _SQL_VARIABLE1, 
				'HEIGHT2': _SQL_VARIABLE2, 
				'HEIGHT3': _SQL_VARIABLE3, 
				'HEIGHT4': _SQL_VARIABLE4,
				'BOX_TEMP': _SQL_VARIABLE5, 
				'HUMIDITY': _SQL_VARIABLE6, 
				'SBC_TEMP': _SQL_VARIABLE7,
				'TRANS_TEMP1': _SQL_VARIABLE8, 
				'TRANS_TEMP2': _SQL_VARIABLE9, 
				}
	 
	return jsonify(jsontable)
 

# ====Count connect user number==========================================
@socketio.on('connect', namespace='/test')
def test_connect(): 
	global USERCOUNT
	USERCOUNT += 1
	# print(f'Client #{USERCOUNT} connected')
	socketio.emit('my_count_response',{'data': 'Current User - %d'%USERCOUNT},namespace='/test')
	
 
@socketio.on('disconnect', namespace='/test')
def test_disconnect():
	global USERCOUNT
	USERCOUNT-=1

	print(f'Client #{USERCOUNT} connected')
 
	socketio.emit('my_count_response',{'data': 'Current User - %d'%USERCOUNT},namespace='/test')


#====================================================+

if __name__ == '__main__':
	socketio.run(app,host='0.0.0.0', port=5000)

 


