---
title: Design Decisions
nav_order: 3
---

{: .label }
[Batuhan Selvi & Efe Kürsat Epik]

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## 01: How to access the database - SQL or SQLAlchemy

### Meta
**Status:** Decided  
**Updated:** 09.12.2025  

### Problem statement
Sollten wir Datenbank-Operationen (CRUD: Create, Read, Update, Delete) direkt mit SQL ausführen oder SQLAlchemy als Object-Relational Mapper (ORM) verwenden?  

Unsere Webanwendung ist in Python mit Flask geschrieben und nutzt SQLite. Das Projekt erfordert grundlegende Datenbankinteraktionen, während zukünftige Skalierung vorgesehen ist.

### Decision
Wir verwenden **SQLAlchemy**.  

Begründung:  
- Ermöglicht die Arbeit mit Python-Klassen anstelle von rohen SQL-Abfragen.  
- Erleichtert spätere Änderungen der Datenbankstruktur und Migration auf andere Datenbanksysteme.  
- Erhöht die Lesbarkeit und Wartbarkeit des Codes, besonders für Teammitglieder mit unterschiedlichem Kenntnisstand in SQL.  

**Entscheidung getroffen von:** Kürsat Efe Epik, Batuhan Selvi

### Regarded options
Wir haben zwei Optionen abgewogen:

| Criterion           | Plain SQL                                     | SQLAlchemy                                           |
|--------------------|-----------------------------------------------|----------------------------------------------------|
| Know-how            | ✔️ Wir kennen SQL                             | ❌ ORM & SQLAlchemy müssen erlernt werden         |
| Änderung DB-Schema  | ❌ SQL direkt im Code verteilt                | ✔️ Klassenmodell, Migrationswerkzeuge verfügbar   |
| Wechsel DB Engine   | ❌ Unterschiedliche SQL-Dialekte             | ✔️ ORM abstrahiert Datenbankengine                |

**Ergebnis:** SQLAlchemy wurde gewählt, da es zukünftige Änderungen erleichtert und besser zu unserem objektorientierten Python-Ansatz passt.

---

## 02: Sankey Diagram Generation

### Meta
**Status:** Decided  
**Updated:** 04.12.2025  

### Problem statement
Wie sollen Finanzflüsse visualisiert werden, um Einnahmen, Ausgaben und Sparziele verständlich darzustellen?  

### Decision
Wir verwenden **Plotly** zur Generierung von Sankey-Diagrammen direkt in Python.  

Begründung:  
- Interaktive Diagramme direkt als HTML-String einbettbar.  
- Kein zusätzlicher Frontend-Code notwendig.  
- Unterstützt dynamische Daten aus der Datenbank.  

**Entscheidung getroffen von:** Kürsat Efe Epik, Batuhan Selvi  

### Regarded options
| Criterion               | Static Chart (z.B. Matplotlib) | Plotly Interactive Sankey        |
|------------------------|--------------------------------|---------------------------------|
| Interaktivität          | ❌ Nicht interaktiv             | ✔️ Zoom, Hover, Links           |
| Einbettung in Templates | ❌ Nur als Bild                 | ✔️ Direkt als HTML einbettbar   |
| Dynamische Updates      | ❌ Schwer                       | ✔️ Einfach via Datenbindung     |

**Ergebnis:** Plotly ermöglicht klare und interaktive Darstellung der Finanzströme.

---

## 03: Access Control / Route Protection

### Meta
**Status:** Decided  
**Updated:** 02.12.2025  

### Problem statement
Wie verhindern wir, dass nicht eingeloggte Benutzer auf Dashboard, Sankey oder andere geschützte Seiten zugreifen?  

### Decision
Jede geschützte Route prüft `session['logged_in']` vor dem Rendern der Seite.  

Begründung:  
- Einfach umsetzbar ohne zusätzliche Libraries.  
- MVP-konform und ausreichend für derzeitige Nutzerbasis.  

**Entscheidung getroffen von:** Kürsat Efe Epik, Batuhan Selvi  

### Regarded options
| Criterion          | Flask Session Check      | Flask-Login Library          |
|-------------------|-------------------------|-----------------------------|
| Einfachheit         | ✔️ Direkt im Code        | ❌ Zusätzliche Installation |
| Flexibilität        | ❌ Weniger Features      | ✔️ Rollen, Remember-Me     |
| MVP-Aufwand         | ✔️ Schnell umsetzbar     | ❌ Mehr Setup nötig         |

**Ergebnis:** Session-Check in jeder Route reicht für MVP.

