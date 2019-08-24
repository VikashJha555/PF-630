#Libraries

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Config

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///medhive.db'
db=SQLAlchemy(app)

from EzyDiagnoseGo import routes
