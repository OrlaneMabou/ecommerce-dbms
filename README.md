# E-Commerce Datenbank (DBMS) 🗄️

Relationales Datenbankschema für einen Online-Shop, implementiert mit SQLite und Python.

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
- ✅ 7 normalisierte Tabellen (3NF) mit FK- und CHECK-Constraints
- ✅ 10 analytische SQL-Abfragen (JOINs, Aggregationen, Subqueries)
- ✅ CRUD-Operationen demonstriert
- ✅ Performance-Indizierung

---
*Projekt von Orlane Nono Mabou — BSc Wirtschaftsinformatik, HRW*
