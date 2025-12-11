---
title: Data Model
parent: Technical Docs
nav_order: 2
---

{: .label }
[Jane Dane]

{: .no_toc }
# Data model

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

Data Model

Die Anwendung BudgetBro verwendet eine relationale Datenstruktur, die mit SQLAlchemy umgesetzt wird.

1. User

Repräsentiert registrierte Benutzer der App.

Enthält:

username (einzigartig)

password_hash zur sicheren Speicherung von Passwörtern

onboarding_done als Boolean, um zu prüfen, ob der Nutzer das Onboarding abgeschlossen hat

Hinweis: Dieses Modell ist vollständig implementiert und in Nutzung.

2. Income & Expense

Repräsentieren Einnahmen und Ausgaben eines Benutzers.

Enthalten Felder für Beschreibung, Kategorie, Betrag und Datum.

Status: Diese Modelle befinden sich noch in Bearbeitung und werden in kommenden Updates vollständig integriert.

3. OnboardingData

Speichert initiale Finanzinformationen während des Onboarding-Prozesses.

Unterteilt in verschiedene Kategorien (Einnahmen, Fixkosten, Variable Kosten, Sparen & Anlegen, Schulden).

Status: Noch in Bearbeitung.

4. CustomCategory

Ermöglicht Benutzern, eigene Kategorien zu definieren.

Status: Noch in Bearbeitung.

5. MonthlySummary

Speichert aggregierte Monatsdaten für jeden Benutzer.

Status: Noch in Bearbeitung.

Beziehungen zwischen den Modellen

User ist die zentrale Entität, die mit allen anderen Modellen verknüpft wird.

Status: Verknüpfungen werden mit den anderen Modellen umgesetzt, sobald diese vollständig implementiert sind.
<img width="1254" height="708" alt="image" src="https://github.com/user-attachments/assets/2085ef80-581d-4c51-af32-fb8140dfe1b5" />

