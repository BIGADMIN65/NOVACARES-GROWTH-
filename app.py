from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'novacares_secret_key_2026'

# Create database and table automatically
conn = sqlite3.connect('database.db')
conn.execute('''CREATE TABLE IF NOT EXISTS users 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             name TEXT NOT NULL, 
             email TEXT UNIQUE NOT NULL, 
             password TEXT NOT NULL, 
             balance REAL DEFAULT 0.0)''')
conn.execute('DELETE FROM users')  # <-- ADD THIS LINE TO WIPE OLD DATA
conn.commit()
conn.close()

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
  conn.execute('INSERT INTO users (name, email, password, balance) VALUES (?, ?, ?, ?)', (name, email, password, 0.0))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return "Email already exists! <a href='/signup'>Try again</a>"
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid email or password <a href='/login'>Try again</a>"
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
    conn.close()
    
    return f"Welcome {user['name']}! Your balance is: ${user['balance']}"

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
