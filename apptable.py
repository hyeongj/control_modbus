from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

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
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# =====================================+
 

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
		return '<tbconed %r>' % self.TIME_CREATED

# ==============================================================


  


