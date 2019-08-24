from flask import render_template,request
from EzyDiagnoseGo import app
from EzyDiagnoseGo import db
from EzyDiagnoseGo.models import User,Role,Doctor,Customer,Order
import os
from flask import Flask, render_template, request
from flask import send_from_directory
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import tensorflow as tf
from keras import optimizers
import numpy as np

# Interface & Interactivity

uid=None

dir_path = os.path.dirname(os.path.realpath(__file__))
# UPLOAD_FOLDER = dir_path + '/uploads'
# STATIC_FOLDER = dir_path + '/static'
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
MEDHIVE='EzyDiagnoseGo'

graph = tf.get_default_graph()
with graph.as_default():

    # load model at very first
    model = load_model(MEDHIVE+'/'+STATIC_FOLDER + '/' + 'model_design.h5')
    model.compile(optimizer = optimizers.RMSprop(lr=1e-4), loss = 'binary_crossentropy', metrics = ['accuracy'])




# call model to predict an image
def api(full_path):
    data = image.load_img(full_path, target_size=(150, 150, 3))
    data = np.expand_dims(data, axis=0)
    data = data * 1.0 / 255

    with graph.as_default():
        predicted = model.predict(data)
        return predicted

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user_register')
def user_register():
    return render_template('user_register.html')

@app.route('/ezyDiagnose')
def ezyDiagnose():
    return render_template('ezyDiagnose.html')

@app.route('/role_register',methods=["Post"])
def role_register():

    lenght=0
    
    username=request.form.get("Username")
    password=request.form.get("Password")
    email=request.form.get("Email")
    contact=request.form.get("Contact")
    address=request.form.get("Address")
    gender=request.form.get("Gender")
    age=request.form.get("Age")

    userdata=User.query.all()
    lenght=len(userdata)

    global uid
    uid=lenght+1

    user=User(uid=uid,username=username,password=password,email=email,contact=contact,address=address,gender=gender,age=age)
    
    db.session.add(user)

    db.session.commit()

    return render_template("role_register.html")


@app.route('/profile_register',methods=["Post"])
def profile_register():

    rlist=Role.query.all()
    rlen=len(rlist)
    entry_id=rlen+1

    role=request.form.get("Role")

    user_role=Role(entry_id=entry_id,rname=role,uid=uid)

    db.session.add(user_role)

    db.session.commit()

    if(role=="Doctor" or role=="doctor"):
        return render_template("doctor_register.html")

    elif(role=="Customer" or role=="customer"):
        return render_template("customer_register.html")

    else:
        User.query.filter_by(uid=uid).delete()
        db.session.commit()
        return render_template("invalid.html")

        
@app.route('/doctor_register',methods=["Post"])
def doctor_register():

    dlist=Doctor.query.all()
    dlen=len(dlist)
    did=dlen+1
    specialisation=request.form.get("Specialisation")
    rating=request.form.get("Rating")
    fee=request.form.get("Fee")
    availabilty=request.form.get("Availability")
    location=request.form.get("Location")

    user_doc=Doctor(did=did,specialisation=specialisation,rating=rating,fee=fee,availablity=availabilty,location=location,uid=uid)

    db.session.add(user_doc)

    db.session.commit()

    upd_dlist=Doctor.query.all()
    upd_dlen=len(dlist)

    userdata=User.query.filter_by(uid=uid).first()
    roledata=Role.query.filter_by(uid=uid).first()
    docdata=Doctor.query.filter_by(did=upd_dlen).first()
    
    
    return render_template("dcomplete.html",userdata=userdata,roledata=roledata,docdata=docdata)


@app.route('/customer_register',methods=["Post"])
def customer_register():

    clist=Customer.query.all()
    clen=len(clist)
    cid=clen+1
    medcon=request.form.get("Medcon")
    location=request.form.get("Location")

    user_cus=Customer(medical_condition=medcon,location=location,uid=uid)

    db.session.add(user_cus)

    db.session.commit()

    upd_clist=Customer.query.all()
    upd_clen=len(upd_clist)
    
    userdata=User.query.filter_by(uid=uid).first()
    roledata=Role.query.filter_by(uid=uid).first()
    cusdata=Customer.query.filter_by(cid=upd_clen).first()
    
    return render_template("ccomplete.html",userdata=userdata,roledata=roledata,cusdata=cusdata)


@app.route('/order')
def order():
    return render_template("order.html")

@app.route('/predict')
def predict():
    return render_template("predict.html")


@app.route('/orderconfirm',methods=["Post"])
def orderconfirm():

    cid=request.form.get("cid")
    cid=int(cid)
    did=request.form.get("did")
    did=int(did)
    data=Customer.query.filter_by(cid=cid).first()
    key=data.uid
    did=request.form.get("did")
    username=request.form.get("Username")
    password=request.form.get("Password")
    userdata=User.query.all()
    lenght=len(userdata)
    upd_userdata=User.query.filter_by(username=username).first()
    user_uid=upd_userdata.uid

    if(user_uid==key):
        for i in range(0,lenght):
                if(username==userdata[i].username):
                    if(password==userdata[i].password):
                        order=Order(cid=cid,did=did)
                        db.session.add(order)
                        db.session.commit()

                        olist=Order.query.all()
                        olen=len(olist)
                        odata=Order.query.filter_by(oid=olen).first()
                        return render_template("ocomplete.html",odata=odata)
                    else:
                        return render_template("invalid.html")
                           
        return render_template("invalid.html")

    else:
        return render_template("invalid.html")
    

@app.route('/listings')
def listings():
    
    docdata=Doctor.query.all()
    return render_template("listings.html", docdata=docdata)


@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/results',methods=["Post"])
def results():

    keyword=request.form.get("SearchQuery")
    category=request.form.get("Category")

    if(category=="ID"):
        value=int(keyword)
        data=Doctor.query.filter_by(did=value).all()
        return render_template("results.html",data=data)
    elif(category=="Location" or category=="location"):
        data=Doctor.query.filter(Doctor.location.like('%'+keyword+'%')).all()
        return render_template("results.html",data=data)
    elif(category=="Specialisation" or category=="specialisation"):
        data=Doctor.query.filter(Doctor.specialisation.like("%"+keyword+"%")).all()
        return render_template("results.html",data=data)    
    elif(category=="Availability" or category=="availability"):
        data=Doctor.query.filter(Doctor.availablity.like("%"+keyword+"%")).all()
        return render_template("results.html",data=data)
    elif(category=="Fee" or category=="fee"):
        value=int(keyword)
        data=Doctor.query.filter_by(fee=value)
        return render_template("results.html",data=data)
    elif(category=="Rating" or category=="rating"):
        value=int(keyword)
        data=Doctor.query.filter_by(rating=value).all()
        return render_template("results.html",data=data)
    else:
        return render_template("invalid.html")
    

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/dashboard',methods=["Post"])
def dashboard():
    username=request.form.get("Username")
    password=request.form.get("Password")
    userdata=User.query.all()
    lenght=len(userdata)
    for i in range(0,lenght):
                if(username==userdata[i].username):
                    if(password==userdata[i].password):
                        user_data=User.query.filter_by(username=username).first()
                        uid=user_data.uid

                        if(Customer.query.filter_by(uid=uid).first()):
                            profile_data=Customer.query.filter_by(uid=uid).first()
                            cid=profile_data.cid
                            orders=Order.query.filter_by(cid=cid).all()
                        elif(Doctor.query.filter_by(uid=uid).first()):
                            profile_data=Doctor.query.filter_by(uid=uid).first()
                            did=profile_data.did
                            orders=Order.query.filter_by(did=did).all()
                        else:
                            return render_template("invalid.html")
                                    
                        return render_template("dashboard.html",user_data=user_data,orders=orders)

                    else:
                        return render_template("invalid.html")

    return render_template("invalid.html")



@app.route('/upload', methods=['POST','GET'])
def upload_file():

    if request.method == 'GET':
        return render_template('index.html')
    else:
        file = request.files['image']
        full_name = os.path.join(MEDHIVE+'/'+UPLOAD_FOLDER, file.filename)
        file.save(full_name)

        indices = {0: 'Pneumonia', 1: 'Not Pneumonia'}
        result = api(full_name)

        predicted_class = np.asscalar(np.argmax(result, axis=1))
        accuracy = round(result[0][predicted_class] * 100, 2)
        label = indices[predicted_class]

    return render_template('predict.html', image_file_name = file.filename, label = label, accuracy = accuracy)


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

