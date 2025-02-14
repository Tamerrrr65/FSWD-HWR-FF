---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
[Mert Giousouf, Tamer Abu Hweidi]

{: .no_toc }
# Reference documentation

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## [Section / module]

### `Home()`
**Route:** `/`  
**Methods:** `GET`  
**Purpose:** Lädt die Hauptseite und zeigt verfügbare Fragebögen an. Prüft, ob der Nutzer angemeldet ist.  

### `Nachhaltigkeit()`
**Route:** `/Nachhaltigkeit`  
**Methods:** `GET`  
**Purpose:** Zeigt die Nachhaltigkeitsseite mit Fragebögen an.  

### `Anmelden()`
**Route:** `/Anmelden`  
**Methods:** `GET`, `POST`  
**Purpose:** Erlaubt Nutzern die Anmeldung. Prüft Login-Daten und speichert die Sitzung.  

### `Registrieren()`
**Route:** `/Registrieren`  
**Methods:** `GET`, `POST`  
**Purpose:** Ermöglicht neuen Nutzern die Registrierung mit Passwort-Verschlüsselung.  

### `Empfehlungen()`
**Route:** `/Empfehlungen`  
**Methods:** `GET`  
**Purpose:** Zeigt eine Seite mit Empfehlungen an.  

### `Gesetze()`
**Route:** `/Gesetze`  
**Methods:** `GET`  
**Purpose:** Lädt eine Informationsseite zu Gesetzen.  

### `Abmelden()`
**Route:** `/Abmelden`  
**Methods:** `GET`  
**Purpose:** Beendet die Sitzung und leitet zur Startseite weiter.  

### `Gesichert()`
**Route:** `/Gesichert`  
**Methods:** `GET`  
**Purpose:** Geschützte Seite, die nur angemeldete Nutzer sehen können.  

### `Fragebögen()`
**Route:** `/Fragebögen`  
**Methods:** `GET`  
**Purpose:** Listet alle verfügbaren Fragebögen auf.  

### `show_fragebogen()`
**Route:** `/Fragebögen/<int:fragebogen_id>`  
**Methods:** `GET`  
**Purpose:** Zeigt einen spezifischen Fragebogen mit Fragen an.  

### `submit_fragebogen()`
**Route:** `/submit_fragebogen`  
**Methods:** `POST`  
**Purpose:** Speichert die Antworten eines Nutzers und wertet sie aus.  

### `beantworteter_fragebogen_loeschen()`
**Route:** `/beantworteter_fragebogen_loeschen`  
**Methods:** `POST`  
**Purpose:** Löscht die gespeicherten Antworten eines Nutzers zu einem Fragebogen.  

### `Ergebnisse()`
**Route:** `/Ergebnisse`  
**Methods:** `GET`  
**Purpose:** Zeigt die gespeicherten Antworten und Auswertungen eines Nutzers an.  

### `Profil()`
**Route:** `/Profil`  
**Methods:** `GET`  
**Purpose:** Zeigt das Nutzerprofil mit persönlichen Fragebögen an.  

### `admin_panel()`
**Route:** `/admin`  
**Methods:** `GET`  
**Purpose:** Öffnet das Admin-Panel zur Verwaltung von Fragebögen.  

### `fragebogen_bearbeiten()`
**Route:** `/admin/Fragebögen/<int:fragebogen_id>`  
**Methods:** `GET`  
**Purpose:** Zeigt Fragen und Auswertungen eines Fragebogens an, um sie zu bearbeiten.  

### `FragebogenHinzufuegen()`
**Route:** `/admin/FragebogenHinzufuegen`  
**Methods:** `GET`, `POST`  
**Purpose:** Erlaubt Admins, neue Fragebögen hinzuzufügen.  

### `fragebogen_loeschen()`
**Route:** `/admin/fragebogen/<int:fragebogen_id>/delete`  
**Methods:** `POST`  
**Purpose:** Löscht einen Fragebogen aus der Datenbank.  

### `frage_hinzufuegen()`
**Route:** `/admin/Fragebögen/<int:fragebogen_id>/hinzufuegen`  
**Methods:** `GET`, `POST`  
**Purpose:** Fügt einer bestehenden Umfrage neue Fragen hinzu.  

### `frage_loeschen()`
**Route:** `/admin/fragen/<int:fragen_id>/loeschen`  
**Methods:** `GET`  
**Purpose:** Löscht eine einzelne Frage aus einem Fragebogen.