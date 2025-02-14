from flask import Flask, render_template, request, redirect, url_for, session
import io
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps
from datetime import datetime
from Datenbanken import init_db, get_frageboegen, fragen_nach_datum_sortiert

init_db()

app = Flask(__name__)
app.secret_key = 'dein_secret_key'  

@app.route('/')
def Home():
    frageboegen = get_frageboegen()
    if 'Angemeldet' in session:
        return render_template('Hauptseite.html', Angemeldet=True, username=session.get('username'), frageboegen=frageboegen)
    return render_template('Hauptseite.html', Angemeldet=False, frageboegen=frageboegen)

@app.route('/Nachhaltigkeit')
def Nachhaltigkeit():
    frageboegen = get_frageboegen()
    return render_template('Nachhaltigkeit.html', Angemeldet=session.get('Angemeldet'), username=session.get('username'), frageboegen=frageboegen)

@app.route('/Anmelden', methods=['GET', 'POST'])
def Anmelden():
    frageboegen = get_frageboegen()
    if 'Angemeldet' in session:
        return redirect(url_for('Home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == '123':
            session['admin_angemeldet'] = True
            return redirect(url_for('admin_panel'))
     
        conn = sqlite3.connect('Datenbanken/nutzer.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM nutzer WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            stored_password = result[2]
            if check_password_hash(stored_password, password):
                session['Angemeldet'] = True
                session['username'] = username
                session['nutzer_id'] = result[0]
                return redirect(url_for('Home'))
            else:
                return render_template('Anmelden.html', error="Falsches Passwort")
        else:
            return render_template('Anmelden.html', error="Benutzer nicht gefunden")
    
    return render_template('Anmelden.html', frageboegen=frageboegen)

@app.route('/Registrieren', methods=['GET', 'POST'])
def Registrieren():
    frageboegen = get_frageboegen()

    if 'Angemeldet' in session:
        return redirect(url_for('Home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('Datenbanken/nutzer.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM nutzer WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return render_template('Registrieren.html', error="Benutzername existiert bereits.")
        
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO nutzer (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()
        return redirect(url_for('Anmelden'))

    return render_template('Registrieren.html', frageboegen=frageboegen)

@app.route('/Empfehlungen')
def Empfehlungen():
    frageboegen = get_frageboegen()

    if 'Angemeldet' in session:
        return render_template('Empfehlungen.html', Angemeldet=True, username=session.get('username'), frageboegen=frageboegen)
    return render_template('Empfehlungen.html', Angemeldet=False, frageboegen=frageboegen)

@app.route('/Gesetze')
def Gesetze():
    return render_template('Gesetze.html')

@app.route('/Abmelden')
def Abmelden():
    session.pop('Angemeldet', None)
    session.pop('username', None)
    return redirect(url_for('Home'))

def Anmeldung_Benötigt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'Angemeldet' not in session:
            return redirect(url_for('Home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/Gesichert')
@Anmeldung_Benötigt
def Gesichert():
    return f"Hallo {session.get('username')}, dies ist eine geschützte Seite."

@app.route('/Fragebögen')
def Fragebögen():
    frageboegen = get_frageboegen()
    return render_template('Fragebögen.html', Angemeldet=session.get('Angemeldet'), username=session.get('username'), frageboegen=frageboegen)

@app.route('/Fragebögen/<int:fragebogen_id>')
def show_fragebogen(fragebogen_id):
    if 'Angemeldet' not in session:
        return redirect(url_for('Anmelden'))
    
    frageboegen = get_frageboegen()

    conn = sqlite3.connect('Datenbanken/frageboegen.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, titel, beschreibung FROM frageboegen WHERE id = ?', (fragebogen_id,))
    fragebogen = cursor.fetchone()

    cursor.execute('SELECT id, text, fragen_art FROM fragen WHERE frageboegen_id = ?', (fragebogen_id,))
    fragen = cursor.fetchall()

    conn.close()

    print(fragen)
    if fragebogen:
        fragebogen_data = {
            'id': fragebogen[0],
            'titel': fragebogen[1],
            'beschreibung': fragebogen[2]
        }

    return render_template('Frage.html', frageboegen=frageboegen, Angemeldet=session.get('Angemeldet'), username=session.get('username'), fragebogen=fragebogen_data, fragen=fragen)

@app.route('/submit_fragebogen', methods=['POST'])
def submit_fragebogen():
    nutzer = session['nutzer_id']
    fragebogen_id = request.form['fragebogen_id']
    answers = {}

    conn = sqlite3.connect('Datenbanken/frageboegen.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, fragen_art FROM fragen WHERE frageboegen_id = ?', (fragebogen_id,))
    fragen = cursor.fetchall()

    conn.commit()
    conn.close()

    for frage_id, fragen_art in fragen:
        
        if fragen_art == 'range':
            antwort = int(request.form[f'frage{frage_id}'])
        else:
            antwort = int(request.form[f'frage{frage_id}'])
            if antwort == 0:
                antwort = 2
            elif antwort == 1:
                antwort = 1
        
        conn = sqlite3.connect('Datenbanken/antworten.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO frageboegen_antworten (nutzer_id, frageboegen_id, fragen_id, antwort)
            VALUES (?, ?, ?, ?)
        ''', (nutzer, fragebogen_id, frage_id, antwort))

        conn.commit()
        conn.close()

        if antwort == 0:
            antwort = 1

        conn = sqlite3.connect('Datenbanken/auswertungen.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT auswertungs_text
            FROM auswertungen
            WHERE fragen_id = ? AND auswahlmoeglichkeit = ?
        ''', (frage_id, str(antwort)))


        print(frage_id, antwort)

        auswertungs_text = cursor.fetchone()[0]
        answers[frage_id] = auswertungs_text
        print(frage_id, auswertungs_text)

        conn.commit()
        conn.close()

    return redirect(url_for('Ergebnisse'))

@app.route('/beantworteter_fragebogen_loeschen', methods=['POST'])
@Anmeldung_Benötigt
def beantworteter_fragebogen_loeschen():
    nutzer_id = session.get('nutzer_id')
    fragebogen_id = request.form.get('fragebogen_id')
    erstellt_am = request.form.get('erstellt_am')

    if not fragebogen_id or not erstellt_am:
        return redirect(url_for('Ergebnisse'))

    try:
        conn = sqlite3.connect('Datenbanken/antworten.db')
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM frageboegen_antworten 
            WHERE nutzer_id = ? 
            AND frageboegen_id = ? 
            AND erstellt_am = ?
        """, (nutzer_id, fragebogen_id, erstellt_am))

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Fehler beim Löschen des Fragebogens: {e}")

    return redirect(url_for('Ergebnisse'))

@app.route('/Ergebnisse')
def Ergebnisse():
    frageboegen = get_frageboegen()

    if 'Angemeldet' in session:
        nutzer_id = session.get('nutzer_id')

        if not nutzer_id:
            return redirect(url_for('Anmelden'))

        conn = sqlite3.connect('Datenbanken/nutzer.db')
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.isolation_level = None

        cursor = conn.cursor()

        cursor.execute("ATTACH DATABASE 'Datenbanken/antworten.db' AS antworten;")
        cursor.execute("ATTACH DATABASE 'Datenbanken/frageboegen.db' AS frageboegen;")
        cursor.execute("ATTACH DATABASE 'Datenbanken/auswertungen.db' AS auswertungen;")

        cursor.execute("""
            SELECT 
                qr.frageboegen_id, 
                q.titel, 
                qr.erstellt_am, 
                qs.text AS frage_text,
                qs.fragen_art,   
                qr.antwort, 
                et.auswertungs_text
            FROM antworten.frageboegen_antworten qr
            JOIN frageboegen.frageboegen q ON qr.frageboegen_id = q.id
            JOIN frageboegen.fragen qs ON qr.fragen_id = qs.id
            LEFT JOIN auswertungen.auswertungen et 
                ON et.fragen_id = qs.id AND et.auswahlmoeglichkeit = qr.antwort
            WHERE qr.nutzer_id = ?
            ORDER BY qr.erstellt_am DESC;
        """, (nutzer_id,))

        results = cursor.fetchall()
        conn.close()

        fragebogen_data = {}
        for row in results:
            fragebogen_id = row[0]
            if fragebogen_id not in fragebogen_data:
                fragebogen_data[fragebogen_id] = {
                    'titel': row[1],
                    'fragen': []
                }

            antwort = row[5]
            if row[4] == 'radio' and row[5] == '1': 
                antwort = 'Ja'
            elif row[4] == 'radio' and row[5] == '0':
                antwort = 'Nein'

            frage_data = {
                'erstellt_am': row[2],
                'frage_text': row[3],
                'fragen_art': row[4],
                'antwort': antwort,
                'auswertungs_text': row[6] if row[6] else "N/A"
            }
            fragebogen_data[fragebogen_id]['fragen'].append(frage_data)

        results = fragen_nach_datum_sortiert(fragebogen_data)

        return render_template(
            'Ergebnisse.html', 
            Angemeldet=True, 
            username=session.get('username'), 
            frageboegen=frageboegen, 
            results=results
        )

    return redirect(url_for('Anmelden'))

@app.route('/Profil')
def Profil():
    frageboegen = get_frageboegen()

    if 'Angemeldet' in session:
        return render_template('Profil.html', Angemeldet=True, username=session.get('username'), frageboegen=frageboegen)
    return render_template('Profil.html', Angemeldet=False, frageboegen=frageboegen)


@app.route('/admin')
def admin_panel():
    if not session.get('admin_angemeldet'):
        session.pop('admin_angemeldet', None)
        session.pop('Angemeldet', None)
        session.pop('username', None)
        return redirect(url_for('Anmelden'))

    frageboegen = get_frageboegen()
    return render_template('AdminPanel.html', frageboegen=frageboegen, admin_checked=True)

@app.route('/admin/Fragebögen/<int:fragebogen_id>')
def fragebogen_bearbeiten(fragebogen_id):
    if not session.get('admin_angemeldet'):
        return redirect(url_for('admin_login'))

    conn = sqlite3.connect('Datenbanken/frageboegen.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT q.id, q.text, q.fragen_art
        FROM fragen q
        WHERE q.frageboegen_id = ?
    ''', (fragebogen_id,))
    fragen = cursor.fetchall()

    conn.close()


    conn = sqlite3.connect('Datenbanken/auswertungen.db')
    cursor = conn.cursor()

    fragebogen_auswertungen = {}
    for fragen_id, text, fragen_art in fragen:
        cursor.execute('''
            SELECT auswertungs_text, auswahlmoeglichkeit
            FROM auswertungen
            WHERE fragen_id = ?
            ORDER BY auswahlmoeglichkeit
        ''', (fragen_id,))
        auswertungen = cursor.fetchall()
        fragebogen_auswertungen[fragen_id] = auswertungen


    conn.close()

    return render_template(
        'FragebogenBearbeiten.html',
        fragen=fragen, 
        fragebogen_auswertungen=fragebogen_auswertungen, 
        fragebogen_id=fragebogen_id, 
        admin_checked=True
    )

@app.route('/admin/FragebogenHinzufuegen', methods=['GET', 'POST'])
def FragebogenHinzufuegen():
    if not session.get('admin_angemeldet'):
        return redirect(url_for('Anmelden'))

    if request.method == 'POST':
        titel = request.form['titel']
        beschreibung = request.form['beschreibung']

        conn = sqlite3.connect('Datenbanken/frageboegen.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO frageboegen (titel, beschreibung) VALUES (?, ?)', (titel, beschreibung))
        conn.commit()
        conn.close()

        return redirect(url_for('admin_panel'))

    return render_template('FragebogenHinzufuegen.html')

@app.route('/admin/fragebogen/<int:fragebogen_id>/delete', methods=['POST'])
def fragebogen_loeschen(fragebogen_id):
    if not session.get('admin_angemeldet'):
        return redirect(url_for('Anmelden'))

    try:
        conn = sqlite3.connect('Datenbanken/frageboegen.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM frageboegen WHERE id = ?', (fragebogen_id,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Fehler beim Löschen des Fragebogens: {e}")

    return redirect(url_for('admin_panel'))

@app.route('/admin/Fragebögen/<int:fragebogen_id>/hinzufuegen', methods=['GET', 'POST'])
def frage_hinzufuegen(fragebogen_id):
    if not session.get('admin_angemeldet'):
        return redirect(url_for('admin_angemeldet'))
    
    if request.method == 'POST':
        text = request.form['text']
        fragen_art = request.form['fragen_art']

        conn = sqlite3.connect('Datenbanken/frageboegen.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO fragen (text, fragen_art, frageboegen_id)
            VALUES (?, ?, ?)
        ''', (text, fragen_art, fragebogen_id))
        fragen_id = cursor.lastrowid

        conn.commit()
        conn.close()

        conn = sqlite3.connect('Datenbanken/auswertungen.db')
        cursor = conn.cursor()

        if fragen_art  == 'range':
            for i in range(1, 6):
                auswertungs_text = request.form.get(f'evaluation_range_{i}')
                cursor.execute('''
                    INSERT INTO auswertungen  (fragen_id, auswertungs_text, auswahlmoeglichkeit)
                    VALUES (?, ?, ?)
                ''', (fragen_id, auswertungs_text, i))
        else:
            for i in range(1, 3):
                auswertungs_text = request.form.get(f'evaluation_radio_{i}')
                cursor.execute('''
                    INSERT INTO auswertungen  (fragen_id, auswertungs_text, auswahlmoeglichkeit)
                    VALUES (?, ?, ?)
                ''', (fragen_id, auswertungs_text, i))

        conn.commit()
        conn.close()
        return redirect('/admin')
    
    return render_template('FragenHinzufuegen.html', fragebogen_id=fragebogen_id, frageboegen = get_frageboegen())

@app.route('/admin/fragen/<int:fragen_id>/loeschen')
def frage_loeschen(fragen_id):
    if not session.get('admin_angemeldet'):
        return redirect(url_for('admin_login'))

    try:
        connection = sqlite3.connect('Datenbanken/auswertungen.db')
        cursor = connection.cursor()

        cursor.execute('DELETE FROM auswertungen WHERE fragen_id = ?', (fragen_id,))
        connection.commit()
        connection.close()

        connection_two = sqlite3.connect('Datenbanken/frageboegen.db')
        cursor_two = connection_two.cursor()

        cursor_two.execute('SELECT frageboegen_id FROM fragen WHERE id = ?', (fragen_id,))
        fragebogen = cursor_two.fetchone()

        if fragebogen:
            fragebogen_id = fragebogen[0]

            cursor_two.execute('DELETE FROM fragen WHERE id = ?', (fragen_id,))
            connection_two.commit()
            connection_two.close()

            return redirect(url_for('fragebogen_bearbeiten', fragebogen_id=fragebogen_id))

    except sqlite3.Error as e:
        connection.rollback()
        print(f"Fehler beim Löschen der Frage: {e}")
    finally:
        if connection:
            connection.close()
        if connection_two:
            connection_two.close()

    return redirect(url_for('admin_panel'))

@app.route('/admin/fragen/<int:fragen_id>/bearbeiten', methods=['GET', 'POST'])
def frage_bearbeiten(fragen_id):
    if not session.get('admin_angemeldet'):
        return redirect(url_for('admin_login'))

    conn = sqlite3.connect('Datenbanken/frageboegen.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, text, fragen_art, frageboegen_id FROM fragen WHERE id = ?", (fragen_id,))
    frage = cursor.fetchone()
    conn.close()

    if not frage:
        return "Frage nicht gefunden", 404

    fragebogen_id = frage[3]

    conn = sqlite3.connect('Datenbanken/auswertungen.db')
    cursor = conn.cursor()
    cursor.execute("SELECT auswertungs_text, auswahlmoeglichkeit FROM auswertungen WHERE fragen_id = ?", (fragen_id,))
    auswertungen = cursor.fetchall()
    conn.close()

    fragebogen_auswertungen = {fragen_id: auswertungen}

    if request.method == 'POST':
        neuer_text = request.form['text']
        neue_fragen_art = request.form['fragen_art']

        conn = sqlite3.connect('Datenbanken/frageboegen.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE fragen SET text = ?, fragen_art = ? WHERE id = ?", (neuer_text, neue_fragen_art, fragen_id))
        conn.commit()
        conn.close()

        conn = sqlite3.connect('Datenbanken/auswertungen.db')
        cursor = conn.cursor()
        for auswahlmoeglichkeit, _ in auswertungen:
            neue_auswertung = request.form.get(f"evaluation_{auswahlmoeglichkeit}", "").strip()
            if neue_auswertung:
                cursor.execute("UPDATE auswertungen SET auswertungs_text = ? WHERE fragen_id = ? AND auswahlmoeglichkeit = ?", 
                               (neue_auswertung, fragen_id, auswahlmoeglichkeit))
        conn.commit()
        conn.close()

        return redirect(url_for('fragebogen_bearbeiten', fragebogen_id=fragebogen_id))

    return render_template(
        'FragenBearbeiten.html', 
        frage=frage, 
        fragebogen_auswertungen=fragebogen_auswertungen
    )

if __name__ == "__main__":
    app.run(debug=True)