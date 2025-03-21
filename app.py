from flask import Flask, render_template, request, redirect, session
import sqlite3
import bcrypt

app = Flask(__name__)

app.secret_key = "abc123"

def start_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    sql_users = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    '''
    cursor.execute(sql_users)

    sql_results = '''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    '''
    cursor.execute(sql_results)

    conn.commit()
    conn.close()

def save_result(user_id, score):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    sql = 'INSERT INTO results (user_id, score) VALUES (?, ?)'
    cursor.execute(sql, (user_id, score))
    conn.commit()
    conn.close()

def get_highscore_results():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    sql = '''
        SELECT users.name, results.score
        FROM results
        JOIN users ON results.user_id = users.id
        ORDER BY results.score DESC
        LIMIT 10
    '''
    cursor.execute(sql)
    top_results = cursor.fetchall()
    conn.close()
    return top_results

def get_user_highscore_results(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    sql = '''
        SELECT score
        FROM results
        WHERE user_id = ?
        ORDER BY score DESC
        LIMIT 10
    '''
    cursor.execute(sql, (user_id,))
    top_results = cursor.fetchall()
    conn.close()
    return top_results

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

@app.route('/play')
def play_page():
    return render_template('play.html')

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
        return render_template("login.html")
    else:
        name = request.form["name"]
        password = request.form["password"]
        return login_user(name, password)

@app.route('/submit_result', methods=['POST'])
def submit_result():
    if 'user_id' in session:
        score = int(request.form['score'])
        user_id = session['user_id']
        save_result(user_id, score)
    return redirect('/play')

@app.route('/highscore')
def highscore_page():
    top_results = get_highscore_results()
    return render_template('highscore.html', top_results=top_results)

@app.route('/user_highscore')
def user_highscore_page():
    if 'user_id' in session:
        user_id = session['user_id']
        top_results = get_user_highscore_results(user_id)
        return render_template('user_highscore.html', top_results=top_results)
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=2800, host="0.0.0.0")
