---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
[Batuhan Selvi]

{: .no_toc }
# Reference documentation


<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

# Reference Documentation

Diese Seite dokumentiert interne Routen, Funktionen und Logik der BudgetBro-WebApp.
BudgetBro unterstützt Nutzer:innen beim Verständnis ihrer monatlichen Finanzflüsse mithilfe von Sankey-Diagrammen, Sparzielen und einem Budget-Health-Score.

---

## User Management

### `register()`
**Route:** `/register`  
**Methods:** `GET`, `POST`

**Purpose:**  
Zeigt das Registrierungsformular. Erstellt einen neuen Benutzer, hasht das Passwort und loggt den Nutzer automatisch ein. Nach erfolgreicher Registrierung wird direkt das Onboarding gestartet.

**Sample output:**  
- Erfolg: Weiterleitung zu `/onboarding`, Flash: *„Registrierung erfolgreich! Lass uns mit dem Onboarding starten.“*  
- Fehler: Flash: *„Benutzername ist bereits vergeben.“*

---

### `login()`
**Route:** `/login`  
**Methods:** `GET`, `POST`

**Purpose:**  
Authentifiziert bestehende Benutzer anhand von Benutzername und Passwort. Startet eine Session bei Erfolg.

**Sample output:**  
- Erfolg:  
  - Onboarding nicht abgeschlossen → Weiterleitung zu `/onboarding`  
  - Onboarding abgeschlossen → Weiterleitung zu `/dashboard`  
  - Flash: *„Login erfolgreich!“*  
- Fehler: Flash: *„Benutzername oder Passwort falsch!“*

---

### `logout()`
**Route:** `/logout`  
**Methods:** `GET`

**Purpose:**  
Beendet die Session und loggt den Benutzer aus.

**Sample output:**  
- Weiterleitung zu `/login`  
- Flash: *„Du wurdest ausgeloggt.“*

---

## Onboarding

### `onboarding()`
**Route:** `/onboarding`  
**Methods:** `GET`, `POST`

**Purpose:**  
Erfasst die grundlegenden finanziellen Daten des Nutzers (Einnahmen, Fixkosten, variable Kosten, Sparen, Schulden).  
Das Onboarding ist verpflichtend und Voraussetzung für die Nutzung aller weiteren App-Funktionen.

**Sample output:**  
- Erfolg: Weiterleitung zu `/dashboard`, Flash: *„Onboarding gespeichert. Willkommen!“*  
- Bereits abgeschlossen: Weiterleitung zum Dashboard

---

## Dashboard & Visualisierung

### `dashboard()`
**Route:** `/dashboard`  
**Methods:** `GET`

**Purpose:**  
Zentrale Übersichtsseite für eingeloggte Benutzer. Zeigt das Sankey-Diagramm, das aktuelle Sparziel sowie eine Zusammenfassung der Finanzdaten.

**Sample output:**  
- HTML-Seite mit eingebettetem Sankey-Diagramm  
- Sparziel-Karte (falls vorhanden)

---

### `sankey_full()`
**Route:** `/sankey/full`  
**Methods:** `GET`

**Purpose:**  
Zeigt das Sankey-Diagramm im Vollbildmodus für eine detailliertere Betrachtung der Finanzströme.

**Sample output:**  
- Vollbild-Sankey-Diagramm mit Navigationsmöglichkeit zurück zum Dashboard

---

## Finanzflüsse & Kategorien

### `fluss()`
**Route:** `/fluss`  
**Methods:** `GET`, `POST`

**Purpose:**  
Ermöglicht das Bearbeiten der Basis-Finanzdaten sowie das Hinzufügen benutzerdefinierter Kategorien für Einnahmen, Kosten, Sparen und Schulden.

**Funktionen:**  
- Aktualisieren der Onboarding-Werte  
- Hinzufügen eigener Kategorien  
- Anzeigen bestehender Kategorien

**Sample output:**  
- HTML-Seite mit Formularen für Basiswerte und Custom-Kategorien  
- Flash-Meldungen bei Änderungen

---

### `delete_category()`
**Route:** `/fluss/delete/<cat_id>`  
**Methods:** `GET`

**Purpose:**  
Löscht eine benutzerdefinierte Kategorie des eingeloggten Benutzers.

**Sample output:**  
- Erfolg: Flash *„Kategorie gelöscht.“*  
- Fehler: Flash *„Kategorie nicht gefunden.“*

---

## Sparziele

### `ziele()`
**Route:** `/ziele`  
**Methods:** `GET`, `POST`

**Purpose:**  
Erstellt oder aktualisiert ein Sparziel des Nutzers inklusive Zielbetrag und bereits gespartem Betrag.

**Sample output:**  
- HTML-Seite mit Zielkarte  
- Flash: *„Ziel gespeichert.“*

---

## Budget Health

### `budget_health()`
**Route:** `/budget-health`  
**Methods:** `GET`

**Purpose:**  
Berechnet und visualisiert den Budget-Health-Score (0–100) des Nutzers auf Basis von Einnahmen, Fixkosten und Sparquote.  
Benutzerdefinierte Kategorien werden in die Berechnung einbezogen.

**Sample output:**  
- HTML-Seite mit Gesamt-Score, Subscores und erklärenden Texten  
- Weiterleitung zum Onboarding, falls keine Finanzdaten vorhanden sind

---

## Sankey-Diagramm

### `build_financial_sankey()`
**Route:** *keine (interne Funktion)*  
**Methods:** *keine*

**Purpose:**  
Erstellt ein personalisiertes Sankey-Diagramm aus Onboarding-Daten und Custom-Kategorien.  
Visualisiert monatliche Einnahmen, Ausgaben, Sparen und Schulden.

**Return:**  
- HTML-String mit eingebettetem Plotly-Diagramm  
- Dictionary mit aggregierten Summen:
  - `income_total`
  - `fix_total`
  - `var_total`
  - `save_total`
  - `debt_total`

---

## Budget-Health-Berechnung

### `calculate_budget_health_score()`
**Route:** *keine (Utility-Funktion)*  
**Methods:** *keine*

**Purpose:**  
Berechnet einen Budget-Health-Score (0–100) anhand von drei gewichteten Faktoren:

- **Sparquote** (40 %)  
- **Fixkosten-Anteil** (33 %)  
- **Monatlicher Überschuss** (27 %)

---
