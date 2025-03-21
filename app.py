from flask import Flask, render_template, request, redirect, session
import sqlite3
import bcrypt
 
app = Flask(__name__)
 
app.secret_key = "abc123"
 
def start_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        '''
    cursor.execute(sql)
    conn.commit()
    conn.close()
 
start_db()
 
def register_user(name, password):
    if request.method == 'POST':
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
 
        try:
            sql = 'INSERT INTO users (name, password) VALUES (?, ?)'
            cursor.execute(sql, (name, hashed_password))
            conn.commit()
            conn.close()
            return render_template('account_created.html', name=name)
       
        except sqlite3.IntegrityError:
            return render_template('register.html', error="Brukernavnet er allerede tatt, prøv et annet!")
 
    return render_template('register.html')
 
def login_user(name, password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
   
    sql = 'SELECT id, password FROM users WHERE name = ?'
    cursor.execute(sql, (name,))
    user = cursor.fetchone()
   
    if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
        session['name'] = name
        session['user_id'] = user[0]
        conn.close()
        return redirect('/')
    else:
        conn.close()
        return render_template('login.html', error="Feil brukernavn eller passord!")
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form["name"]
        password = request.form["password"]
        return register_user(name, password)
 
@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        if session.get("name"):
            return render_template("login.html")
        else:
            return render_template("login.html")
    else:
        name = request.form["name"]
        password = request.form["password"]
        return login_user(name, password)
 
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
 
if __name__ == '__main__':
    app.run(debug=True, port=2800, host="0.0.0.0")