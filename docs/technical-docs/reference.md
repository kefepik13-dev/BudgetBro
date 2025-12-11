---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
[Jane Dane]

{: .no_toc }
# Reference documentation


<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

# Reference Documentation

Diese Seite sammelt interne Funktionen, Routen und APIs der BudgetBro-App.

---

## User Management

### `register()`

**Route:** `/register/`  
**Methods:** `GET`, `POST`  

**Purpose:**  
Zeigt das Registrierungsformular. Erstellt einen neuen Benutzer, hasht das Passwort und startet eine Session.

**Sample output:**  
- Bei Erfolg: Weiterleitung zum Dashboard, Flash „Login erfolgreich“  
- Bei Fehler: Flash „Benutzername ist bereits vergeben“

---

### `login()`

**Route:** `/login/`  
**Methods:** `GET`, `POST`  

**Purpose:**  
Zeigt Login-Formular, prüft Benutzername + Passwort. Startet Session bei Erfolg.

**Sample output:**  
- Erfolg: Weiterleitung zum Dashboard, Flash „Login erfolgreich“  
- Fehler: Flash „Benutzername oder Passwort falsch!“

---

### `logout()`

**Route:** `/logout/`  
**Methods:** `GET`  

**Purpose:**  
Löscht die Session und loggt den Benutzer aus. Leitet zurück zum Login.

**Sample output:**  
- Flash: „Du wurdest ausgeloggt.“

---

## Dashboard & Visualisierung

### `dashboard()`

**Route:** `/dashboard/`  
**Methods:** `GET`  

**Purpose:**  
Zeigt das Dashboard für eingeloggte Benutzer. Beinhaltet Sankey-Diagramm, Tipps und Sparziele.

**Sample output:**  
- HTML-Seite mit Sankey-Diagramm, Sparziel-Karte und Tipps-Karte

---

### `sankey_full()`

**Route:** `/sankey/full/`  
**Methods:** `GET`  

**Purpose:**  
Zeigt Sankey-Diagramm im Vollbild. Nur für eingeloggte Benutzer.

**Sample output:**  
- Vollbild-Sankey-Diagramm mit Zurück-Link zum Dashboard

---

### `fluss()`

**Route:** `/fluss/`  
**Methods:** `GET`  

**Purpose:**  
Zeigt Detailansicht der Finanzströme (aktuell Platzhalter, noch in Bearbeitung)

**Sample output:**  
- HTML-Seite „Fluss“

---

### `berichte()`

**Route:** `/berichte/`  
**Methods:** `GET`  

**Purpose:**  
Zeigt Finanzberichte/Analysen (aktuell Platzhalter, noch in Bearbeitung)

**Sample output:**  
- HTML-Seite „Berichte“

---

### `ziele()`

**Route:** `/ziele/`  
**Methods:** `GET`  

**Purpose:**  
Zeigt Sparziele des Benutzers, Fortschrittsanzeige in Prozent.

**Sample output:**  
- HTML-Seite mit Zielkarten

---

## Sankey-Diagramm

### `build_financial_sankey()`

**Route:** NONE (Funktion, kein Endpoint)  
**Methods:** NONE  

**Purpose:**  
Generiert Sankey-Diagramm aus Einnahmen, Ausgaben und Sparzielen. Liefert HTML-String, direkt in Templates eingebettet.

**Sample output:**  
- HTML `<iframe>` mit Sankey-Diagramm
