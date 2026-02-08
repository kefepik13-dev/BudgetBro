# BudgetBro - Finanzplaner App

Eine Flask-basierte Webanwendung zur Budgetplanung für Studenten, junge Erwachsene und Einpersonenhaushalte.

## Features

- 📊 **Finanzfluss-Visualisierung**: Interaktive Sankey-Diagramme zur Darstellung von Einnahmen und Ausgaben
- 🎯 **Budget Health Score**: Bewertung der finanziellen Gesundheit (0-100) basierend auf Sparquote, Fixkostenanteil und monatlichem Überschuss
- 🎯 **Zielverfolgung**: Setze Sparziele und verfolge deinen Fortschritt
- 📝 **Kategorienverwaltung**: Erstelle eigene Einnahmen- und Ausgabenkategorien
- 🔐 **Benutzerauthentifizierung**: Sichere Registrierung und Login

## Voraussetzungen

- Python 3.7 oder höher
- pip (Python Package Manager)

## Installation

1. **Repository klonen oder herunterladen**
   ```bash
   cd BudgetBro
   ```

2. **Virtuelle Umgebung erstellen (empfohlen)**
   ```bash
   python3 -m venv venv
   ```

3. **Virtuelle Umgebung aktivieren**
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```

4. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```
   
   Oder manuell:
   ```bash
   pip install Flask Flask-SQLAlchemy Flask-WTF Plotly WTForms Werkzeug
   ```

## Ausführung

1. **Stelle sicher, dass die virtuelle Umgebung aktiviert ist** (falls verwendet)

2. **App starten**
   ```bash
   python3 app.py
   ```
   
   Oder:
   ```bash
   python app.py
   ```

3. **Im Browser öffnen**
   
   Die App läuft standardmäßig auf: **http://localhost:5001**
   
   Öffne diese URL in deinem Webbrowser.

4. **App stoppen**
   
   Drücke `Ctrl + C` im Terminal, um den Server zu beenden.

## Erste Schritte

1. **Registrierung**: Erstelle einen neuen Benutzeraccount
2. **Onboarding**: Gib deine monatlichen Einnahmen, Fixkosten, variable Kosten, Sparbeträge und Schulden ein
3. **Dashboard**: Sieh dir deine Finanzübersicht mit dem Sankey-Diagramm an
4. **Budget Health**: Prüfe deinen Budget Health Score und die detaillierte Analyse
5. **Ziele**: Setze Sparziele und verfolge deinen Fortschritt
6. **Finanzfluss**: Bearbeite deine Kategorien und füge eigene hinzu

## Projektstruktur

```
BudgetBro/
├── app.py                 # Hauptanwendung (Routes, Models, Forms)
├── budget_health.py       # Budget Health Score Berechnung
├── instance/
│   └── budgetbro.db      # SQLite Datenbank (wird automatisch erstellt)
├── templates/             # HTML-Templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── onboarding.html
│   ├── dashboard.html
│   ├── budget_health.html
│   ├── fluss.html
│   ├── ziele.html
│   └── sankey_full.html
└── static/
    ├── css/
    │   └── main.css      # Styling
    └── images/
        └── favicon.png
```

## Technologien

- **Backend**: Flask (Python Web Framework)
- **Datenbank**: SQLite mit SQLAlchemy ORM
- **Formulare**: Flask-WTF / WTForms
- **Visualisierung**: Plotly (Sankey-Diagramme)
- **Frontend**: HTML, CSS, Jinja2 Templates

## Datenbank

Die SQLite-Datenbank wird automatisch beim ersten Start erstellt und befindet sich im `instance/` Verzeichnis.

**Wichtig**: Die Datenbank wird beim ersten Start automatisch initialisiert. Alle Daten werden lokal gespeichert.

## Entwicklung

### Debug-Modus

Die App läuft standardmäßig im Debug-Modus (`debug=True`). Dies ermöglicht:
- Automatisches Neuladen bei Code-Änderungen
- Detaillierte Fehlermeldungen

### Port ändern

Um einen anderen Port zu verwenden, ändere in `app.py`:
```python
app.run(debug=True, port=5001)  # Port hier ändern
```

## Fehlerbehebung

### "ModuleNotFoundError"
- Stelle sicher, dass alle Abhängigkeiten installiert sind: `pip install Flask Flask-SQLAlchemy Flask-WTF Plotly WTForms`
- Prüfe, ob die virtuelle Umgebung aktiviert ist

### "Port already in use"
- Der Port 5001 ist bereits belegt. Ändere den Port in `app.py` oder beende den anderen Prozess

### Datenbank-Probleme
- Lösche die Datei `instance/budgetbro.db` und starte die App neu (⚠️ Alle Daten gehen verloren!)

## Lizenz

Dieses Projekt wurde für akademische Zwecke entwickelt.

## Autoren

Entwickelt als Gruppenprojekt von Batuhan Selvi und Kürsat Efe Epik.
