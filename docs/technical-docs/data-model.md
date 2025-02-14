---
title: Data Model
parent: Technical Docs
nav_order: 2
---

{: .label }
[Mert Giousouf, Tamer Abu Hweidi]

{: .no_toc }
# **Data Model**

<details open markdown="block">
{: .text-delta }
<summary>Table of Contents</summary>

- TOC
{: toc }
</details>

## **1. Nutzer**
Speichert die Nutzer mit:  

- `id` *(Primärschlüssel, eindeutige ID)*
- `username` *(eindeutiger Benutzername)*
- `password` *(gespeichertes Passwort)*

---

## **2. Fragebögen**
Speichert die Fragebögen mit:  

- `id` *(Primärschlüssel)*
- `titel` *(Name des Fragebogens)*
- `beschreibung` *(optionale Beschreibung)*

---

## **3. Fragen**
Speichert die Fragen eines Fragebogens mit:  

- `id` *(Primärschlüssel)*
- `text` *(Fragentext)*
- `fragen_art` *(Art der Frage, z. B. Ja/Nein oder Skala)*
- `frageboegen_id` *(Fremdschlüssel → verbindet Frage mit einem Fragebogen)*

---

## **4. Antworten**
Speichert die Antworten der Nutzer mit:  

- `id` *(Primärschlüssel)*
- `nutzer_id` *(Fremdschlüssel → verweist auf Nutzer)*
- `frageboegen_id` *(Fremdschlüssel → verweist auf Fragebogen)*
- `fragen_id` *(Fremdschlüssel → verweist auf Frage)*
- `antwort` *(die abgegebene Antwort)*
- `erstellt_am` *(Zeitstempel der Antwort)*

---

## **5. Auswertungen**
Speichert die möglichen Auswertungen basierend auf der Antwort mit:  

- `id` *(Primärschlüssel)*
- `fragen_id` *(Fremdschlüssel → verweist auf eine Frage)*
- `auswahlmoeglichkeit` *(Antwortoption, die zu dieser Auswertung führt)*
- `auswertungs_text` *(Text der Interpretation)*
