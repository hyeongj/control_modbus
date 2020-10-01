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
_SQL_VARIABLE=[]
_OBJ=None
# ---------------------

# ======================================================================================== 
POSTGRES = {
    'user': 'postgres',
    'pw': 'Hoons0408!',
    'db': 'postgres',
    'host': 'database-1.c0bhgyjg3dyh.us-east-2.rds.amazonaws.com',
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
	val=[[] for _ in range(13)]
	
	fmt='%B %d %H:%M'

	for j in yy:
		tmp=j.TIME_CREATED
		conv=tmp.replace(microsecond=0).strftime(fmt)
		val[0].append(conv)
		val[1].append(j.GAIN)
		val[2].append(j.THRES_T)
		val[3].append(j.THRES_A)
		val[4].append(j.RATE)
		val[5].append(j.CHS)
		val[6].append(j.AMP)
		val[7].append(j.TOF)
		val[8].append(j.HEIGHT)
		val[9].append(j.HUMIDITY)
		val[10].append(j.T_SBC)
		val[11].append(j.T_MODEM)
		val[12].append(j.T_BOX)

	pydic={'Time (GMT)':val[0], 'GAIN': val[1], 'THT': val[2], 'THA': val[3], 
			'RATE': val[4], 'CHS': val[5], 'AMP': val[6], 'TOF': val[7], 'HEIGHT': val[8], 
			'RH': val[9], 'Temp.1' : val[10], 'Temp.2' : val[11], 
			'Temp.3' : val[12]}

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
	HEIGHT = db.Column(db.Float, unique=False, nullable=True)
	HUMIDITY = db.Column(db.Integer, unique=False, nullable=True)
	T_SBC = db.Column(db.Integer, unique=False, nullable=True)
	T_MODEM = db.Column(db.Integer, unique=False, nullable=True)
	T_BOX = db.Column(db.Integer, unique=False, nullable=True)
	WAVEFORM = db.Column(db.LargeBinary, unique=False, nullable=True)
	

	def __repr__(self):
		return '<tbconed %r>' % self.TIME_CREATED


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
			_OBJ=df.to_html(classes='tdata', header="true",table_id="example")
 
		except:
			pydic={'Time (GMT)':[], 'GAIN': [], 'THT': [], 'THA': [], 
			'RATE': [], 'CHS': [], 'AMP':[], 'TOF': [], 'HEIGHT': [], 
			'RH': [], 'Temp.1' : [], 'Temp.2' : [], 
			'Temp.3' : []}

			df=pd.DataFrame(pydic)
			_OBJ=df.to_html(classes='tdata', header="true",table_id="example")
	 
 
		return render_template("index.html", tables=[_OBJ])
	else:
		return redirect(url_for('base'))



@app.route('/historydata')
def historydata():
	''' This is history plot from SQL'''
	# global tvalues, hvalues,startdate, enddate	
	try:
		df=READSQLDATA(dbconed)
		_SQL_TIME=df['Time (GMT)'].values.tolist()
		_SQL_VARIABLE=df['HEIGHT'].values.tolist()	
	
	except:
		_SQL_TIME=[]
		_SQL_VARIABLE=[]

	jsontable = {'Date': _SQL_TIME, 'height': _SQL_VARIABLE}
	return jsonify(jsontable)
 

# ==============================================
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

 


