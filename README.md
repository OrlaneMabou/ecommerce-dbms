# E-Commerce Datenbank (DBMS) 

Relationales Datenbankschema für einen Online-Shop, implementiert mit SQLite und Python.
A relational database project built with Python and SQLite, developed as part of my Database & Management Systems coursework at Hochschule Ruhr West. I designed a normalized schema (3NF) with 7 tables — customers, products, categories, orders, order items, reviews, and payments — including foreign keys, CHECK constraints, and performance indexes. I then wrote 10 analytical SQL queries covering JOINs, aggregations, subqueries, and filtering, plus a full CRUD demonstration. This project gave me hands-on experience translating a real-world business model into a database structure.

## Technologien / Technologies
- Python 3.10+
- SQLite3 — relationale Datenbank
- SQL — DDL, DML, analytische Abfragen

## Datenbankstruktur / Structure BDD
| Tabelle | Beschreibung |
|---------|-------------|
| Kunden | Kundenstammdaten |
| Produkte | Produktkatalog mit Lagerbestand |
| Kategorien | Produktkategorien |
| Bestellungen | Bestellkopfdaten |
| Bestellpositionen | Bestellzeilen (N:M Auflösung) |
| Bewertungen | Kundenbewertungen (1–5 Sterne) |
| Zahlungen | Zahlungsinformationen |

## Ausführen / Exécution

```bash
python ecommerce.py
```

## Funktionen / Fonctionnalités
-  7 normalisierte Tabellen (3NF) mit FK- und CHECK-Constraints
-  10 analytische SQL-Abfragen (JOINs, Aggregationen, Subqueries)
-  CRUD-Operationen demonstriert
-  Performance-Indizierung

---
*Projekt von Orlane Nono Mabou — BSc Wirtschaftsinformatik, HRW*
