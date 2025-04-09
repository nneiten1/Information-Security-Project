from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("User Registered")
    except sqlite3.IntegrityError:
        print("Username already exists")
    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone

    conn.close()
    return user is not None


@app.route('/')
def home():
        return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if register_user(username, password):
            return "Registered successfully! <a href='/login'>Login</a>"
        else:
            return "Username is already in use."
    return render_template('register.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if login_user(username, password):
            return f"Welcome, {username}!"
        else:
            return "Invalid login."
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)