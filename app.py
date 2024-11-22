from flask import Flask, render_template, request,session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from gridfs import GridFS
import config




app = Flask(__name__)
app.secret_key = config.SECRET_KEY

client = MongoClient('mongodb+srv://sohamnsharma:rdcv4c75@sih.cgxnw.mongodb.net/?retryWrites=true&w=majority&appName=sih')
db = client['sih']
users = db['users']
documents = db['documents']
fs = GridFS(db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Renders the signup page
    return render_template('signup.html')

# Route to render the login page (GET request)
@app.route('/login', methods=['GET'])
def login():
    error = request.args.get('error')
    return render_template('login.html', error=error)

# Route to handle form submission (POST request)
@app.route('/login', methods=['POST'])
def handle_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({"username": username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
        return 'Invalid username or password'
    return render_template('index.html')

# Route for dashboard (after successful login)
@app.route('/dashboard')
def dashboard():
    return "Welcome to the Dashboard!"


@app.route('/signup', methods=['GET', 'POST'])
def handle_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if users.find_one({"username": username}):
            return 'Username already exists'
        users.insert_one({"username": username, "password": password})
        return redirect(url_for('login'))
    return render_template('signup.html')



if __name__ == '__main__':
    app.run(debug=True)
