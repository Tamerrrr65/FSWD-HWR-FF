---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
[Mert Giousouf, Tamer Abu Hweidi]

{: .no_toc }
# Architecture

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview

Unsere Plattform ist eine webbasierte Anwendung, die Mode-Startups und kleine Modehersteller dabei unterstützt, nachhaltige Rohstoffbeschaffung und ESG-konforme Lieferketten zu optimieren. Durch interaktive Fragebögen, eine datengetriebene Evaluationslogik und eine intuitive Benutzeroberfläche bietet die Anwendung fundierte Handlungsempfehlungen und erleichtert den Zugang zu nachhaltigen Materialien sowie zertifizierten Lieferanten.

Technologisch basiert die Plattform auf einem modularen, skalierbaren Architekturansatz, der es Entwicklern ermöglicht, effizient neue Funktionen hinzuzufügen oder bestehende Komponenten zu optimieren. Die Kernfunktionen umfassen:

1. Interaktive Fragebögen zur Ermittlung des Nachhaltigkeitsstatus
2. Einfaches Empfehlungssystem für nachhaltige Materialien und Lieferanten
4. Eine benutzerfreundliche Web-Oberfläche für eine intuitive Navigation

Die Anwendung ist so konzipiert, dass sie leicht erweiterbar ist, um zukünftige Anforderungen an Nachhaltigkeitsstandards, neue Regulierungen oder sich wandelnde Bedürfnisse der Modebranche zu integrieren.

## Codemap

Unsere Anwendung folgt einer modularen Architektur, die eine klare Trennung zwischen Frontend, Backend und Datenbank gewährleistet. Dies ermöglicht eine flexible Weiterentwicklung und einfache Wartung.

Frontend
1. Besteht aus HTML und CSS für das grundlegende Design und die Benutzeroberfläche.
2. Enthält interaktive Formulare für die Fragebögen sowie Ergebnisdarstellungen.
3. Zielt auf eine intuitive und responsive Nutzung ab.

Backend
1. Entwickelt mit Python und Flask für die serverseitige Logik.
2. Verantwortlich für die Verarbeitung der Fragebögen
3. Enthält eine API-Schicht, die mit dem Frontend kommuniziert.

Datenbank
1. SQLite als relationale Datenbank, da dies für die initiale Entwicklung einfach und effizient war.
2. Speichert Nutzerantworten, Fragebögen, Fragen und die Auswertungen.

Admin Panel
1. Ermöglicht die Verwaltung von Fragebögen, Fragen und deren Inhalten.
2. Nutzt eine eigene API-Schicht für administrative Funktionen.

