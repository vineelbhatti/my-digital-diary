from flask import *
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from flask_moment import Moment
import time
from datetime import datetime
import random
from bson.objectid import ObjectId

app = Flask("UserDetails")
app.config['MONGO_URI'] = "mongodb://localhost:27017/UserDetails-db"


Bootstrap(app)


mongo = PyMongo(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'sOmE_rAnDom_woRd'

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('UserRegistration.html')
    elif request.method == 'POST':
        doc = {}
        for item in request.form:
            doc[item]=request.form[item]
        mongo.db.UserDetails.insert_one(doc)
        flash('Account created successfully!')
        time.sleep(3)
        return redirect('/Login')
@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('Login.html')
    elif request.method == 'POST':
        doc = {'Email': request.form['Email'], 'Password': request.form['Password']}
        found = mongo.db.UserDetails.find_one(doc)

        if found is None:
            flash('The email and password you entered did not match our records. Please double-check and try again.')
            return redirect('/Login')
        else:
            session['user-info'] = {'FirstName' : found['FirstName'], 'LastName' : found['LastName'], 'Email' : found['Email'], 'loginTime': datetime.utcnow()}
            return redirect('/home')
@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user-info' in session:
        if request.method == "GET":
            savedEntries = mongo.db.entries.find({'Email': session['user-info']['Email']})
            list1 = []
            for x in savedEntries:
                list1.append(x)
            print(list1)
            return render_template('home.html', entries=list1)
        elif request.method == "POST":
            print('hi')
            entry = {'Email': session['user-info']['Email'], 'content': request.form['content'], 'time':datetime.utcnow()}
            print(request.form['content'])
            mongo.db.entries.insert_one(entry)
            return redirect('/home')
    else:
        flash('You need to login first!')
        return redirect
@app.route('/logout')
def logout():
    session.pop('user-info')
    return redirect('/Login')
app.run(debug=True)
