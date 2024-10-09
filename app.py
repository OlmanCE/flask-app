from flask import Flask, render_template, request, redirect, url_for, session, g
import secrets
from db import get_db, init_app

app = Flask(__name__)
app.secret_key = secrets.token_hex()

app.config['DATABASE'] = 'user_data.db'

init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        if len(password) < 10:
            error = 'La contraseña debe tener al menos 10 caracteres.'
            return render_template('signup.html', error=error)

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            error = 'El nombre de usuario ya existe. Por favor elija otro.'
            return render_template('signup.html', error=error)

        cursor.execute('INSERT INTO users (email, username, password) VALUES (?, ?, ?)', (email, username, password))
        conn.commit()
        
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if user:
            session['username'] = username
            return redirect(url_for('profile', username=username))
        else:
            error = 'Nombre de usuario o contraseña incorrectos.'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    if 'username' not in session or session['username'] != username:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    if user:
        profile = {
            "username": user['username'],
            "email": user['email'],
            "pictureURL": user['pictureURL'] if 'pictureURL' in user.keys() else '',
            "fullName": user['fullName'] if 'fullName' in user.keys() else '',
            "address": user['address'] if 'address' in user.keys() else '',
            "birthday": user['birthday'] if 'birthday' in user.keys() else '',
            "linkedIn": user['linkedIn'] if 'linkedIn' in user.keys() else '',
            "socialMedia": user['socialMedia'] if 'socialMedia' in user.keys() else ''
        }

        return render_template('profile.html', profile=profile)
    else:
        error = 'Usuario no encontrado.'
        return render_template('login.html', error=error)

@app.route('/editProfile/<username>', methods=['GET', 'POST'])
def edit_profile(username):
    if 'username' not in session or session['username'] != username:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        pictureURL = request.form.get('pictureURL', '')
        fullName = request.form.get('fullName', '')
        address = request.form.get('address', '')
        birthday = request.form.get('birthday', '')
        linkedIn = request.form.get('linkedIn', '')
        socialMedia = request.form.get('socialMedia', '')

        cursor.execute('''
            UPDATE users SET
                pictureURL = ?,
                fullName = ?,
                address = ?,
                birthday = ?,
                linkedIn = ?,
                socialMedia = ?
            WHERE username = ?
        ''', (pictureURL, fullName, address, birthday, linkedIn, socialMedia, username))
        conn.commit()
        
        return redirect(url_for('profile', username=username))
    else:
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        user_data = {
            "username": user['username'],
            "pictureURL": user['pictureURL'] if 'pictureURL' in user.keys() else '',
            "fullName": user['fullName'] if 'fullName' in user.keys() else '',
            "address": user['address'] if 'address' in user.keys() else '',
            "birthday": user['birthday'] if 'birthday' in user.keys() else '',
            "linkedIn": user['linkedIn'] if 'linkedIn' in user.keys() else '',
            "socialMedia": user['socialMedia'] if 'socialMedia' in user.keys() else ''
        }
        return render_template('edit_profile.html', user=user_data)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)