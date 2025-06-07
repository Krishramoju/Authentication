from flask import Flask, request, redirect, session, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.environ.get("NEUROOS_SECRET_KEY", "supersecret")

users = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "User already exists!"
        users[username] = generate_password_hash(password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users or not check_password_hash(users[username], password):
            return "Invalid credentials."
        session['username'] = username
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/ai')
@login_required
def ai_app():
    return "Welcome to the AI App!"

@app.route('/brain-teaser')
@login_required
def brain_teaser():
    return "Welcome to Brain Teaser App!"

@app.route('/recruitment')
@login_required
def recruitment():
    return "Welcome to Recruitment App!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
