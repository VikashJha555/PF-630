from datetime import datetime
from EzyDiagnoseGo import db 

#Models

class User(db.Model):

    uid=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    email=db.Column(db.String(40),unique=True,nullable=False)
    contact=db.Column(db.String(13),unique=True)
    address=db.Column(db.String(120),nullable=False)
    gender=db.Column(db.String(6),nullable=False)
    age=db.Column(db.Integer,nullable=False)


    role=db.relationship('Role',backref='user',lazy=True)
    doctor=db.relationship('Doctor',backref='user',lazy=True)
    customer=db.relationship('Customer',backref='user',lazy=True)
    
    def __repr__(self):
        return "Username: %s\nEmail: %s\nContact:%s\n Address:%s\n Gender: %s\nAge: %s"%(self.username,self.email,self.contact,self.address,self.gender,self.age)

class Role(db.Model):

    entry_id=db.Column(db.Integer,primary_key=True)
    rname=db.Column(db.String(8),nullable=False)
    uid=db.Column(db.Integer,db.ForeignKey('user.uid'),nullable=False)

    def __repr__(self):
        return "Profile_type= %s"%(self.rname)

class Doctor(db.Model):

    did=db.Column(db.Integer,primary_key=True)
    specialisation=db.Column(db.String(60),nullable=False)
    rating=db.Column(db.Integer,nullable=False)
    fee=db.Column(db.Integer,nullable=False)    
    availablity=db.Column(db.String(10),nullable=False)
    location=db.Column(db.String(20),nullable=False)
    uid=db.Column(db.Integer,db.ForeignKey('user.uid'),nullable=False) 

    orders=db.relationship('Order',backref='doctor',lazy=True)
    
    
    def __repr__(self):
        return "Doctor_id: %s\nSpecialisation: %s\nRating: %s\nFee: %s\nAvailability: %s\nLocation: %s"%(self.did,self.specialisation,self.rating,self.fee,self.availablity,self.location)

class Customer(db.Model):

    cid=db.Column(db.Integer,primary_key=True)
    medical_condition=db.Column(db.String(60),nullable=False)
    location=db.Column(db.String(20),nullable=False)
    uid=db.Column(db.Integer,db.ForeignKey('user.uid'),nullable=False)

    orders=db.relationship('Order',backref='client',lazy=True)
    
    def __repr__(self):
        return "Customer_id: %s\nMedical Condition: %s\nLocation: %s"%(self.cid,self.medical_condition,self.location)

class Order(db.Model):

    oid=db.Column(db.Integer,primary_key=True)
    cid=db.Column(db.Integer,db.ForeignKey('customer.cid'),nullable=False)
    did=db.Column(db.Integer,db.ForeignKey('doctor.did'),nullable=False)
    date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    
    def __repr__(self):
        return "Order_id= %s\nCustomer_id= %s\nDoctor_id= %s\nDate: %s"%(self.oid,self.cid,self.did,self.date)
