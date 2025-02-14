---
title: Design Decisions
nav_order: 3
---

{: .label }
[Jane Dane]

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## 01: [Design]

### Meta

Status
: **Work is done**

Updated
: 14-02-2025

- **Problemstellung:**  

  Ein ansprechendes Design und eine gut strukturierte Benutzeroberfläche sind essenziell, um die Verweildauer der Nutzer auf der Webseite zu erhöhen und eine intuitive Nutzung zu ermöglichen.


- **Entscheidung:**  

  Die erste Designentscheidung wurde von Tamer getroffen, da er zu Beginn über größere Grundkenntnisse in HTML verfügte. Das Layout entwickelte sich schrittweise weiter – von einem einfachen Grundlayout über ein Comic-Design bis hin zur finalen Version. Das Endprodukt wurde durch kontinuierliche Abstimmung und iterative Verbesserungen gemeinsam festgelegt.

---

## 02: [Login]

### Meta

Status
: **Work is done**

Updated
: 14-02-2025

- **Problemstellung:** 

  Eine Anmeldefunktion war erforderlich, um sicherzustellen, dass die ausgefüllten Fragebögen für die jeweiligen Nutzer gespeichert werden können und eine individuelle Nachverfolgung der Ergebnisse möglich ist.


- **Entscheidung:**  

  Die Implementierung des Logins wurde von Mert übernommen. Dabei orientierte er sich an den Erklärungen von Herrn Eck und setzte die Authentifizierung mithilfe von SQLite um.

---

## 02: [Fragebögen, Fragen und Auswertung]

### Meta

Status
: **Work is done**

Updated
: 14-02-2025

- **Problemstellung:**  

  Es war notwendig, mehrere kleinere Fragebögen mit entsprechenden Fragen und Auswertungen zu erstellen, um sie sinnvoll in die Webseite zu integrieren.


- **Entscheidung:**  

  Die Erstellung der Fragebögen wurde hauptsächlich von Tamer übernommen, jedoch mit Unterstützung von Mert. Durch gemeinsame Fragerunden konnten die ersten zehn Fragebögen mit jeweils fünf Fragen finalisiert werden.  
  
  Die Fragen sind entweder als Ja/Nein-Fragen oder über eine Skala von 1 bis 5 beantwortbar. Jede der fünf Skalenwerte hat eine eigene, individuell definierte Auswertung. Ursprünglich gab es die Überlegung, die Skalenwerte zu summieren und auf Basis der Gesamtpunktzahl eine umfassendere Analyse zu erstellen. Allerdings erwies sich diese Methode als komplexer als zunächst angenommen, weshalb letztlich eine einfachere Lösung gewählt wurde.

---

## 04: [Beantworten der Fragebögen]

### Meta

Status
: **Work is done**

Updated
: 14-02-2025

- **Problemstellung:**  

  Nutzer müssen die Möglichkeit haben, die Fragebögen direkt auf der Webseite auszufüllen und ihre Antworten zu speichern.

- **Entscheidung:**  

  Die Implementierung dieses Features wurde hauptsächlich von Mert übernommen, da Tamer zu diesem Zeitpunkt mit anderen Projekten beschäftigt war. Ursprünglich war geplant, die ausgefüllten Fragebögen im Nutzerprofil zu speichern. Allerdings wurde später entschieden, diese stattdessen auf einer separaten Seite abzulegen, da die Fragebögen beliebig oft ausgefüllt werden können. Dies führte jedoch dazu, dass die Übersichtlichkeit mit der Zeit nachließ. Um dem entgegenzuwirken, wurde mit Unterstützung von Tamer eine Funktion ergänzt, die es ermöglicht, gespeicherte Fragebögen über einen zusätzlichen Button zu löschen, falls sie fehlerhaft oder nicht relevant sind.

---

## 05: [Admin-Panel]

### Meta

Status
: **Work is done**

Updated
: 14-02-2025

- **Problemstellung:**  

  Das manuelle Hinzufügen neuer Fragen oder Fragebögen durch das Erstellen einer neuen Datenbank und das Ersetzen der alten Version erwies sich als unpraktisch. Daher wurde eine Lösung benötigt, die es Administratoren ermöglicht, Fragebögen direkt über die Benutzeroberfläche zu verwalten.


- **Entscheidung:**  

  Zur effizienten Verwaltung der Inhalte wurde ein Admin-Account eingeführt. Über diesen können Fragebögen hinzugefügt, gelöscht und bearbeitet werden.  
  Beim Bearbeiten eines Fragebogens besteht die Möglichkeit, neue Fragen hinzuzufügen oder bestehende zu entfernen. Ursprünglich war geplant, eine Funktion zu integrieren, die es erlaubt, einzelne Fragen direkt zu bearbeiten, anstatt sie zu löschen und neu zu erstellen. Allerdings traten dabei wiederholt Fehlermeldungen auf, weshalb diese Funktion letztlich entfernt wurde.

---