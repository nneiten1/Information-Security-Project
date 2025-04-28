from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import bcrypt
from cryptography.fernet import Fernet

app = Flask(__name__)

def load_key():
    with open('secret.key', 'rb') as key_file:
        return key_file.read()
    
key = load_key()
cipher_suite = Fernet(key)

def hash_password(plain_password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed

def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def encrypt_data(plain_text):
    return cipher_suite.encrypt(plain_text.encode('utf-8'))

def decrypt_data(encrypted_text):
    return cipher_suite.decrypt(encrypted_text).decode('utf-8')




def register_user(username, password, phone, email):
    conn = sqlite3.connect('neitenbachDB.db')
    cursor = conn.cursor()

    try:
        hashed_password = hash_password(password)
        encrypt_phone = encrypt_data(phone)
        encrypt_email = encrypt_data(email)

        cursor.execute("INSERT INTO users (username, password, phone, email) VALUES (?, ?, ?, ?)",
                       (username, hashed_password, encrypt_phone, encrypt_email)
        )
        conn.commit()
        return "success"
    except sqlite3.IntegrityError as e:
        print("IntegrityError:", e)
        if 'UNIQUE constraint failed: users.username' in str(e):
            return "username_exists"
        else:
            return "integrity_error"
    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect('neitenbachDB.db')
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    conn.close()

    if result:
        stored_hashed_password = result[0]
        return check_password(password, stored_hashed_password)
    else:
        return False


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