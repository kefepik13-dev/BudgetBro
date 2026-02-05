---
title: Contributions
parent: Team Evaluation
nav_order: 4
---

{: .label }
[Batuhan Selvi] [Efe Kürsat Epik]

{: .no_toc }
# Summary of individual contributions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## [Batuhan Selvi]

Contributions
:### Backend-Entwicklung und Systemarchitektur

Für die Finanzmanagement-Applikation übernahm ich die vollständige Konzeption und Implementierung des Backends auf Basis des Python-Microframeworks Flask. Meine Verantwortung umfasste den Entwurf einer skalierbaren Anwendungsarchitektur sowie die Datenmodellierung mittels SQLAlchemy. Dabei designte ich ein relationales Datenbankschema, das Nutzerdaten, Onboarding-Prozesse, variable Finanzkategorien und Sparziele effizient abbildet und konsistent in einer SQLite-Datenbank persistiert.

Ein Schwerpunkt lag auf der Implementierung sicherer Authentifizierungsmechanismen. Hierfür entwickelte ich ein Session-Management-System inklusive Passwort-Hashing (via Werkzeug Security) und Zugriffskontrollen für geschützte Routen. Für die Gewährleistung der Datenintegrität setzte ich auf Flask-WTF, um Nutzereingaben serverseitig streng zu validieren und Fehleingaben abzufangen.
### Konzeption und Entwicklung des Financial-Analysis-Algorithmus

Zusätzlich zu den Kernfunktionen entwickelte und implementierte ich ein proprietäres Analyse-Modul zur Bewertung der finanziellen Stabilität der Nutzer. Das Herzstück bildet der „Budget Health Score“, ein gewichteter Algorithmus, der eine quantitative Bewertung der finanziellen Gesundheit auf einer Skala von 0 bis 100 liefert.

Die wichtigsten Aspekte dieser Implementierung umfassen:

* **Multifaktorielle Bewertungslogik:** Entwicklung eines mathematischen Modells, das drei kritische Finanzkennzahlen isoliert betrachtet und bewertet:
    1.  Savings Rate Score: Analyse der Sparquote.
    2.  Fixed Cost Ratio Score: Bewertung des Fixkostenanteils.
    3.  Monthly Surplus Score: Berechnung des frei verfügbaren Cashflows (Puffer) nach Abzug aller Fixkosten und Sparraten zur Messung der finanziellen Resilienz.


## [Efe Kürsat Epik]

Contributions
### Frontend-Design und User Experience (UX)

Im Rahmen des Projekts verantwortete Efe die vollständige Konzeption und Umsetzung des Frontend-Designs. Ziel war es, eine hochgradig nutzerfreundliche und visuell klare Benutzeroberfläch zu schaffen, die komplexe Finanzdaten für den Endanwender intuitiv zugänglich macht.

Hierbei entwarf und implementierte Efe eine modulare Template-Struktur auf Basis von Jinja2. Durch den Einsatz von Vererbungstechniken stellte er eine konsistente visuelle Identität über alle Unterseiten hinweg sicher – vom ersten Onboarding über das zentrale Dashboard bis hin zu den Detailseiten für Budget-Kennzahlen.

Zu Efes Kernaufgaben in der Frontend-Entwicklung gehörten:
* **Layout & Styling:** Entwicklung eines modernen, responsiven CSS-Designs unter Verwendung von Flexbox und CSS-Grid. Besonderen Wert legte er auf die Gestaltung funktionaler Komponenten, wie der eines konsistenten Navigationssystems und responsiver „Form-Grids“ für eine effiziente Dateneingabe.
* **Dynamische Datenvisualisierung:** Die nahtlose Integration und das Styling von komplexen Plotly-Diagrammen (insbesondere Sankey-Flows). Hierbei optimierte er die Einbettung via Iframes und Wrapper-Klassen, um eine flüssige Darstellung in verschiedenen Ansichtsmodi (Widget vs. Vollbild) zu ermöglichen.
* **Visuelle Nutzerführung:** Entwicklung eines intuitiven Farbsystems zur Kategorisierung von Finanzströmen (z. B. durch Status-Pills für Einnahmen, Fixkosten und Schulden) sowie die Gestaltung interaktiver Fortschrittsbalken für Sparziele.
* **UI-Logik & Feedback:** Implementierung eines dynamischen Flash-Messaging-Systems zur Anzeige von Statusmeldungen sowie das Design eines SVG-basierten Gauges für den „Budget Health Score“, um dem Nutzer sofortiges visuelles Feedback zu seiner finanziellen Lage zu geben.

Durch die enge Abstimmung mit der Backend-Logik stellte er sicher, dass Formulare, Diagramme und personalisierte Nutzerinformationen jederzeit technisch korrekt und ästhetisch ansprechend gerendert werden, wobei Usability und visuelle Konsistenz stets im Vordergrund standen.
