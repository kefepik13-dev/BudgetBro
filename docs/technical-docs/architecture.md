---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
[Jane Dane]

{: .no_toc }
# Architecture

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview

BudgetBro ist eine leichtgewichtige webbasierte Budgeting-App, die sich auf drei Kernaspekte fokussiert:

1. Benutzerverwaltung (Registrierung & Login)

2. Visualisierung von Finanzströmen über ein interaktives Sankey-Diagramm

3. Übersichtliche Aufbereitung von finanziellen Kennzahlen wie Ausgaben, Kategorien und Sparzielen

Die Anwendung nutzt Flask als Backend-Framework, SQLAlchemy als lokale persistente Datenbank und Jinja2-Templates mit eigenem CSS für das Frontend.
Das zentral generierte Sankey-Diagramm wird über Plotly serverseitig erzeugt und nahtlos in das Dashboard integriert.

Die App ist bewusst modular aufgebaut, sodass Entwickler problemlos:

- weitere Routen ergänzen,

- zusätzliche Datenmodelle integrieren,

- oder grafische Auswertungen erweitern können.

BudgetBro legt seinen Fokus nicht auf eine komplette Buchhaltungsfunktion, sondern auf einfache Nachvollziehbarkeit der persönlichen Geldflüsse und eine klar strukturierte, minimalistische Benutzeroberfläche.

## Codemap

1. app.py – Anwendungskern

Hier laufen alle zentralen Funktionen zusammen:

- Flask-App Initialisierung

- Datenbankkonfiguration via SQLAlchemy
  
- Definition der Models (User)

- Definition der Forms (LoginForm, RegisterForm)

- Registrierung aller Routen (Login, Register, Dashboard, Sankey Fullscreen, usw.)

- Generierung des Sankey-Diagramms per Plotly

- Session-Handling für Authentifizierung

- App-Start (app.run())


2. Templates (Jinja2)

Alle HTML-Seiten folgen einer klaren Hierarchie:

- base.html
  Enthält Navigation, Layout und globale Styles.

- dashboard.html
  Bindet das generierte Sankey-Diagramm ein und zeigt Zusatzkarten (Tipps, Sparziele).

- login.html / register.html
  Formulare für Authentifizierung; nutzen Flask-WTF für CSRF-Schutz und Validierung.

- sankey_full.html
  Zeigt die Finanzvisualisierung im Vollbild.

Weiter Seiten wie berichte.html, fluss.html oder ziele.html werden noch vorbereitet und dienen als Erweiterungsflächen.

3. static/css/main.css

Zentrales Stylesheet, u. a. für:

- Navigationsleiste

- Login-Formulare

- Dashboard-Grid

- Cards

- Buttons

- Responsive Verhalten

Das CSS ist clean, übersichtlich und komplett ohne externe Frameworks wie Bootstrap gehalten.

4. Datenbank (SQLite)

Derzeit existiert ein einzelnes Datenmodell:

User

- Speicherung von Benutzername & Passwort (gehasht mit Werkzeug)

- Erweiterbar für weitere Modelle wie

  - Transactions

  - Goals

  - Categories

  - Budgets

Die Datenbank wird beim ersten Start automatisch erzeugt.

5. Plotly-Integration

Der Code erzeugt ein vollständiges Sankey-Diagramm mit:

- Label-, Farb- und Strukturdefinition

- Sources, Targets und Values für Flüsse

- HTML-Einbettung über pio.to_html()

Dadurch wird kein zusätzliches JavaScript benötigt.

## Cross-cutting concerns

- Session Management:
  Die App nutzt Flask-Sessions, um den Login-Zustand der Benutzer zu verwalten. Dadurch wird sichergestellt, dass nur eingeloggte Benutzer auf geschützte Bereiche wie Dashboard, Fluss oder Berichte zugreifen können.

- Security & Passwortschutz:
  Passwörter werden mit Werkzeugs generate_password_hash verschlüsselt gespeichert und beim Login mit check_password_hash überprüft. Dies schützt sensible Benutzerdaten.

- Datenpersistenz:
  SQLAlchemy wird als ORM verwendet, um die Datenbankzugriffe zu abstrahieren. Dadurch wird der Umgang mit Datenbanktabellen, Abfragen und Transaktionen vereinfacht und sicherer gestaltet.

- Template-Struktur:
  Die Anwendung verwendet Jinja2-Templates mit einer base.html, die von allen anderen Seiten geerbt wird. Dadurch ist das Layout konsistent und Änderungen an der Navigation oder Styles müssen nur einmal angepasst werden.

- UI/UX Konsistenz:
  Styles und Layouts werden zentral über main.css gepflegt. Karten, Buttons, Formulare und Diagramme folgen einheitlichen Designrichtlinien.

- Fehler- und Validierungsmanagement:
  Benutzerformulare verwenden WTForms mit Validierungen, um Eingaben zu prüfen und Fehlermeldungen sauber im Frontend anzuzeigen.
