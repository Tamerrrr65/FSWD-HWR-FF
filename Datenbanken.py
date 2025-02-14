import sqlite3
import datetime
import os
from collections import defaultdict
import io

def fragen_nach_datum_sortiert(results):
    grouped_results = {}
    for fragebogen_id, data in results.items():
        grouped_questions = defaultdict(list)
        for frage in data["fragen"]:
            erstellt_am = frage["erstellt_am"]
            grouped_questions[erstellt_am].append(frage)
        
        grouped_results[fragebogen_id] = {
            "titel": data["titel"],
            "grouped_questions": dict(grouped_questions)
        }
    return grouped_results

def get_frageboegen():
    connection = sqlite3.connect('Datenbanken/frageboegen.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM frageboegen')
    frageboegen = cursor.fetchall()
    connection.close()

    return frageboegen

def get_fragen_fuer_frageboegen(fragebogen_id):
    connection = sqlite3.connect('Datenbanken/frageboegen.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM questions WHERE fragebogen_id = ?', (fragebogen_id,))
    questions = cursor.fetchall()
    connection.close()
    return questions

def init_db():
    db_path = 'Datenbanken'
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    
    # Nutzer-Datenbank
    if not os.path.exists(f'{db_path}/nutzer.db'):
        connection = sqlite3.connect(f'{db_path}/nutzer.db')
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nutzer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        connection.commit()
        connection.close()
    
    # Fragebögen-Datenbank
    if not os.path.exists(f'{db_path}/frageboegen.db'):
        connection = sqlite3.connect(f'{db_path}/frageboegen.db')
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS frageboegen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titel TEXT NOT NULL,
                beschreibung TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fragen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                fragen_art TEXT NOT NULL,
                frageboegen_id INTEGER NOT NULL,
                FOREIGN KEY (frageboegen_id) REFERENCES frageboegen (id) ON DELETE CASCADE
            )
        ''')
        connection.commit()
        connection.close()
    
    # Auswertungen-Datenbank
    if not os.path.exists(f'{db_path}/auswertungen.db'):
        connection = sqlite3.connect(f'{db_path}/auswertungen.db')
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS auswertungen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fragen_id INTEGER NOT NULL,
                auswahlmoelichkeit INTEGER NOT NULL,
                auswertungs_text TEXT NOT NULL,
                FOREIGN KEY (fragen_id) REFERENCES fragen (id) ON DELETE CASCADE
            )
        ''')
        connection.commit()
        connection.close()
    
    # Antworten-Datenbank
    if not os.path.exists(f'{db_path}/antworten.db'):
        connection = sqlite3.connect(f'{db_path}/antworten.db')
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS frageboegen_antworten (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nutzer_id INTEGER NOT NULL,
                frageboegen_id INTEGER NOT NULL,
                fragen_id INTEGER NOT NULL,
                antwort INTEGER NOT NULL,
                erstellt_am TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (nutzer_id) REFERENCES nutzer (id) ON DELETE CASCADE,
                FOREIGN KEY (frageboegen_id) REFERENCES frageboegen (id) ON DELETE CASCADE,
                FOREIGN KEY (fragen_id) REFERENCES frage (id) ON DELETE CASCADE
            )
        ''')
        connection.commit()
        connection.close()