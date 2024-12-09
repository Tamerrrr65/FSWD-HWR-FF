from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps

# Diese Funktion erstellt die SQLite-Datenbank und die Tabelle
def init_db():
    if not os.path.exists('Nutzer.db'):
        conn = sqlite3.connect('Nutzer.db')  # Diese Zeile erstellt die Datei, wenn sie noch nicht existiert
        cursor = conn.cursor()
        
        # Tabelle erstellen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print("Datenbank und Tabelle wurden erfolgreich erstellt.")
    else:
        print("Datenbank existiert bereits.")

# Datenbank initialisieren
init_db()

app = Flask(__name__)
app.secret_key = 'dein_secret_key'  

@app.route('/')
def Home():
    if 'Angemeldet' in session:  # Benutzer ist angemeldet
        return render_template('Hauptseite.html', Angemeldet=True, username=session.get('username'))
    return render_template('Hauptseite.html', Angemeldet=False)  # Benutzer ist nicht angemeldet

@app.route('/Zweitseite')
def Zweit():
    return render_template('Zweitseite.html')

@app.route('/Test')
def Test():
    return render_template('Test.html')

@app.route('/Anmelden', methods=['GET', 'POST'])
def Anmelden():
    if 'Angemeldet' in session:  # Wenn der Benutzer schon eingeloggt ist
        return redirect(url_for('Home'))
    
    if request.method == 'POST':  # Wenn das Formular abgesendet wird
        username = request.form['username']
        password = request.form['password']
     
        conn = sqlite3.connect('Nutzer.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()  # Nur ein Ergebnis zurückholen
        conn.close()

        if result:  # Wenn der Benutzer existiert
            stored_password = result[0]  # Das gespeicherte Passwort holen
            if check_password_hash(stored_password, password):  # Passwort überprüfen
                session['Angemeldet'] = True
                session['username'] = username
                return redirect(url_for('Home'))  # Zur Hauptseite weiterleiten
            else:
                return render_template('Anmelden.html', error="Falsches Passwort")  # Fehlermeldung bei falschem Passwort
        else:
            return render_template('Anmelden.html', error="Benutzer nicht gefunden")  # Fehlermeldung bei Benutzer nicht gefunden
    
    return render_template('Anmelden.html')

@app.route('/Registrieren', methods=['GET', 'POST'])
def Registrieren():
    if 'Angemeldet' in session:  # Wenn der Benutzer angemeldet ist
        return redirect(url_for('Home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('Nutzer.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return render_template('Registrieren.html', error="Benutzername existiert bereits.")
        
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()
        return redirect(url_for('Anmelden'))

    return render_template('Registrieren.html')

@app.route('/Gesetze')
def Gesetze():
    return render_template('Gesetze.html')

@app.route('/Abmelden')
def Abmelden():
    session.pop('Angemeldet', None)
    session.pop('username', None)
    return redirect(url_for('Home'))

# Diese Funktion stellt sicher, dass die geschützte Seite nur für eingeloggte Benutzer zugänglich ist
def Anmeldung_Benötigt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'Angemeldet' not in session:
            return redirect(url_for('Home'))  # Wenn der Benutzer nicht eingeloggt ist, leite ihn zum Anmelden weiter
        return f(*args, **kwargs)
    return decorated_function

@app.route('/Gesichert')
@Anmeldung_Benötigt
def Gesichert():
    return f"Hallo {session.get('username')}, dies ist eine geschützte Seite."

if __name__ == "__main__":
    app.run(debug=True)