from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return "success"
    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed: users.username' in str(e):
            return "username_exists"
        else:
            return "intrgrity_error"
    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone

    conn.close()
    return user is not None


@app.route('/')
def home():
        return render_template('home.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm_password']
        
        if password != confirm:
            return "Passwords do not match!"
        
        result = register_user(username, password)
        if result == "success":
            return redirect(url_for('login'))
        elif result == "username_exists":
            return "Username already exists!"
        
    return render_template('register.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if login_user(username, password):
            return redirect(url_for('home'))
        else:
            return "Invalid login."
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)