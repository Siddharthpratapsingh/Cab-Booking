from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mongologinexample'
app.config['MONGO_URI'] = 'mongodb://localhost'

mongo = PyMongo(app)

@app.route('/')
def index():
    

    return render_template('homepage.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name' : request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            
                return "Successfully logged in"
            return render_template('book.html')   
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
           
            return redirect(url_for('book'))
        
        return 'That username already exists!'

    return render_template('signup.html')

@app.route('/book',methods=['POST','GET'])
def book():
    if request.method == 'POST':
        users = mongo.db.users
        users.insert({'start' : request.form['StartLocation'], 'drop' : request.form['DropLocation'],'time':request.form['Time']})
           
        return 'Your Cab is successfully Booked'
        
        

    return render_template('book.html')
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
