from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import bcrypt

app = Flask(__name__)

def hash_password(plain_password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed

def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def register_user(username, password, phone, email):
    conn = sqlite3.connect('neitenbachDB.db')
    cursor = conn.cursor()

    try:
        hashed_password = hash_password(password).decode('utf-8')

        query = f"INSERT INTO USERS (username, password, email, phone) VALUES ('{username}', '{hashed_password}', '{phone}', '{email}')"
        print("Executing query:", query)
        cursor.execute(query)
        conn.commit()
        return "success"
    except sqlite3.IntegrityError as e:
        print("IntegrityError:", e)
        if 'UNIQUE constraint failed: neitenbachDB.username' in str(e):
            return "username_exists"
        else:
            return "integrity_error"
    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect('neitenbachDB.db')
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print("Executing login query:", query)
    cursor.execute(query)
    result = cursor.fetchone()

    conn.close()
    return result is not None


@app.route('/')
def home():
        return render_template('home.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm_password']
        phone = request.form['phone']
        email = request.form['email']
        
        if password != confirm:
            return "Passwords do not match!"
        
        result = register_user(username, password, phone, email)
        print("Registration result:", result)
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