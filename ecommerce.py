# ecommerce.py
# Base de données e-commerce avec SQLite / E-Commerce-Datenbank mit SQLite

import sqlite3
import os

# --- Connexion / Verbindung aufbauen ---
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = "ecommerce.db"

def connexion():
    """Ouvre la connexion SQLite / SQLite-Verbindung öffnen"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row   # résultats accessibles par nom de colonne
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Crée les tables depuis schema.sql / Tabellen aus schema.sql erstellen"""
    conn = connexion()
    with open("schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("✅ Datenbank initialisiert")

# ── Données de test / Testdaten ───────────────────────────────────────────
def seed_data():
    conn = connexion()
    cur = conn.cursor()

    # Kategorien
    kategorien = [("Elektronik",), ("Kleidung",), ("Sport",), ("Bücher",)]
    cur.executemany("INSERT OR IGNORE INTO Kategorien(bezeichnung) VALUES(?)", kategorien)

    # Kunden
    kunden = [
        ("Orlane",  "Mabou",    "orlane@example.com",  "Deutschland"),
        ("Sophie",  "Müller",   "sophie@example.com",  "Deutschland"),
        ("Liam",    "Martin",   "liam@example.com",    "Frankreich"),
        ("Amina",   "Diallo",   "amina@example.com",   "Belgien"),
        ("Jonas",   "Schmidt",  "jonas@example.com",   "Deutschland"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO Kunden(vorname,nachname,email,land) VALUES(?,?,?,?)", kunden)

    # Produkte
    produkte = [
        ("Laptop Pro",      "Leistungsstarker Laptop",  899.99, 50, 1),
        ("Smartphone X",    "Flaggschiff-Smartphone",   699.99, 80, 1),
        ("Laufschuhe",      "Laufschuhe Größe 42",       79.99,120, 3),
        ("T-Shirt Bio",     "100% Bio-Baumwolle",        24.99,200, 2),
        ("Python lernen",   "Einführung in Python",      29.99, 60, 4),
        ("Kopfhörer BT",    "Bluetooth Kopfhörer",      149.99, 90, 1),
        ("Yoga-Matte",      "rutschfest, 6mm",           39.99, 75, 3),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO Produkte(name,beschreibung,preis,lagerbestand,kategorie_id) VALUES(?,?,?,?,?)",
        produkte)

    # Bestellungen
    bestellungen = [
        (1, "2024-01-15", "geliefert"),
        (2, "2024-02-10", "geliefert"),
        (3, "2024-03-05", "versendet"),
        (1, "2024-04-20", "offen"),
        (4, "2024-05-01", "geliefert"),
        (5, "2024-06-12", "storniert"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO Bestellungen(kunden_id,bestell_datum,status) VALUES(?,?,?)",
        bestellungen)

    # Bestellpositionen
    positionen = [
        (1, 1, 1, 899.99), (1, 6, 2, 149.99),
        (2, 3, 1,  79.99), (2, 4, 3,  24.99),
        (3, 2, 1, 699.99),
        (4, 5, 2,  29.99), (4, 7, 1,  39.99),
        (5, 1, 1, 899.99),
        (6, 4, 5,  24.99),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO Bestellpositionen(bestell_id,produkt_id,menge,einzelpreis) VALUES(?,?,?,?)",
        positionen)

    # Bewertungen
    bewertungen = [
        (1, 1, 5, "Exzellenter Laptop!"),
        (2, 3, 4, "Sehr bequem"),
        (3, 2, 5, "Tolles Smartphone"),
        (4, 5, 4, "Gut erklärt"),
        (5, 1, 3, "Preis-Leistung ok"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO Bewertungen(kunden_id,produkt_id,sterne,kommentar) VALUES(?,?,?,?)",
        bewertungen)

    # Zahlungen
    zahlungen = [
        (1, 1199.97, "Kreditkarte"),
        (2,  154.96, "PayPal"),
        (3,  699.99, "Überweisung"),
        (4,   89.97, "PayPal"),
        (5,  899.99, "Kreditkarte"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO Zahlungen(bestell_id,betrag,methode) VALUES(?,?,?)",
        zahlungen)

    conn.commit()
    conn.close()
    print("✅ Testdaten eingefügt")

# ── 10 Requêtes analytiques / 10 Analytische Abfragen ────────────────────
def run_queries():
    conn = connexion()
    cur = conn.cursor()

    print("\n" + "="*60)
    print("📊 ANALYTISCHE SQL-ABFRAGEN")
    print("="*60)

    # Q1 — CA total par produit / Umsatz pro Produkt
    print("\n📌 Q1 — Umsatz pro Produkt (absteigend)")
    cur.execute("""
        SELECT p.name,
               SUM(bp.menge * bp.einzelpreis) AS umsatz
        FROM Bestellpositionen bp
        JOIN Produkte p ON p.produkt_id = bp.produkt_id
        GROUP BY p.produkt_id
        ORDER BY umsatz DESC
    """)
    for r in cur.fetchall(): print(f"   {r['name']:<20} {r['umsatz']:>10.2f} €")

    # Q2 — Nombre de commandes par client / Bestellungen pro Kunde
    print("\n📌 Q2 — Bestellungen pro Kunde")
    cur.execute("""
        SELECT k.vorname || ' ' || k.nachname AS kunde,
               COUNT(b.bestell_id) AS anzahl
        FROM Kunden k
        LEFT JOIN Bestellungen b ON b.kunden_id = k.kunden_id
        GROUP BY k.kunden_id
        ORDER BY anzahl DESC
    """)
    for r in cur.fetchall(): print(f"   {r['kunde']:<22} {r['anzahl']} Bestellung(en)")

    # Q3 — Produits avec note moyenne / Durchschnittsbewertung
    print("\n📌 Q3 — Durchschnittsbewertung pro Produkt")
    cur.execute("""
        SELECT p.name,
               ROUND(AVG(bw.sterne), 1) AS bewertung,
               COUNT(bw.bewertung_id) AS anzahl_bewertungen
        FROM Produkte p
        JOIN Bewertungen bw ON bw.produkt_id = p.produkt_id
        GROUP BY p.produkt_id
        ORDER BY bewertung DESC
    """)
    for r in cur.fetchall():
        print(f"   {r['name']:<20} ⭐ {r['bewertung']} ({r['anzahl_bewertungen']} Bewertung(en))")

    # Q4 — CA total par catégorie / Umsatz nach Kategorie
    print("\n📌 Q4 — Umsatz nach Kategorie")
    cur.execute("""
        SELECT k.bezeichnung AS kategorie,
               SUM(bp.menge * bp.einzelpreis) AS umsatz
        FROM Bestellpositionen bp
        JOIN Produkte p  ON p.produkt_id  = bp.produkt_id
        JOIN Kategorien k ON k.kategorie_id = p.kategorie_id
        GROUP BY k.kategorie_id
        ORDER BY umsatz DESC
    """)
    for r in cur.fetchall(): print(f"   {r['kategorie']:<15} {r['umsatz']:>10.2f} €")

    # Q5 — Commandes livrées / Gelieferte Bestellungen
    print("\n📌 Q5 — Gelieferte Bestellungen")
    cur.execute("""
        SELECT b.bestell_id,
               k.vorname || ' ' || k.nachname AS kunde,
               b.bestell_datum,
               z.betrag
        FROM Bestellungen b
        JOIN Kunden k   ON k.kunden_id = b.kunden_id
        JOIN Zahlungen z ON z.bestell_id = b.bestell_id
        WHERE b.status = 'geliefert'
        ORDER BY b.bestell_datum
    """)
    for r in cur.fetchall():
        print(f"   #{r['bestell_id']} {r['kunde']:<20} {r['bestell_datum']}  {r['betrag']:.2f} €")

    # Q6 — Produits jamais commandés / Nie bestellte Produkte
    print("\n📌 Q6 — Nie bestellte Produkte")
    cur.execute("""
        SELECT name FROM Produkte
        WHERE produkt_id NOT IN (SELECT DISTINCT produkt_id FROM Bestellpositionen)
    """)
    rows = cur.fetchall()
    print(f"   {[r['name'] for r in rows] if rows else 'Alle Produkte wurden bestellt'}")

    # Q7 — Panier moyen par méthode de paiement / Durchschnittsbetrag pro Zahlungsmethode
    print("\n📌 Q7 — Durchschnittlicher Betrag pro Zahlungsmethode")
    cur.execute("""
        SELECT methode,
               ROUND(AVG(betrag), 2) AS avg_betrag,
               COUNT(*) AS anzahl
        FROM Zahlungen
        GROUP BY methode
    """)
    for r in cur.fetchall():
        print(f"   {r['methode']:<15} Ø {r['avg_betrag']:>8.2f} €  ({r['anzahl']} Zahlung(en))")

    # Q8 — Top client / Top-Kunde nach Gesamtumsatz
    print("\n📌 Q8 — Top-Kunden nach Gesamtumsatz")
    cur.execute("""
        SELECT k.vorname || ' ' || k.nachname AS kunde,
               SUM(z.betrag) AS gesamt
        FROM Zahlungen z
        JOIN Bestellungen b ON b.bestell_id = z.bestell_id
        JOIN Kunden k       ON k.kunden_id  = b.kunden_id
        GROUP BY k.kunden_id
        ORDER BY gesamt DESC
        LIMIT 3
    """)
    for i, r in enumerate(cur.fetchall(), 1):
        print(f"   #{i} {r['kunde']:<22} {r['gesamt']:.2f} €")

    # Q9 — Produits en stock faible / Produkte mit niedrigem Lagerbestand
    print("\n📌 Q9 — Produkte mit niedrigem Lagerbestand (< 70)")
    cur.execute("""
        SELECT name, lagerbestand
        FROM Produkte
        WHERE lagerbestand < 70
        ORDER BY lagerbestand
    """)
    for r in cur.fetchall(): print(f"   {r['name']:<20} {r['lagerbestand']} Stück")

    # Q10 — Sous-requête : clients ayant dépensé plus que la moyenne
    print("\n📌 Q10 — Kunden mit überdurchschnittlichem Umsatz (Subquery)")
    cur.execute("""
        SELECT k.vorname || ' ' || k.nachname AS kunde,
               SUM(z.betrag) AS gesamt
        FROM Zahlungen z
        JOIN Bestellungen b ON b.bestell_id = z.bestell_id
        JOIN Kunden k       ON k.kunden_id  = b.kunden_id
        GROUP BY k.kunden_id
        HAVING gesamt > (
            SELECT AVG(sub.total) FROM (
                SELECT SUM(z2.betrag) AS total
                FROM Zahlungen z2
                JOIN Bestellungen b2 ON b2.bestell_id = z2.bestell_id
                GROUP BY b2.kunden_id
            ) sub
        )
    """)
    for r in cur.fetchall(): print(f"   {r['kunde']:<22} {r['gesamt']:.2f} €")

    conn.close()

# ── CRUD Démonstration / CRUD-Demo ────────────────────────────────────────
def crud_demo():
    conn = connexion()
    cur = conn.cursor()
    print("\n" + "="*60)
    print("🔧 CRUD-DEMO")
    print("="*60)

    # CREATE
    cur.execute(
        "INSERT INTO Kunden(vorname,nachname,email,land) VALUES(?,?,?,?)",
        ("Test","Kunde","test@example.com","Österreich"))
    new_id = cur.lastrowid
    print(f"\n✅ CREATE — Neuer Kunde eingefügt (ID={new_id})")

    # READ
    cur.execute("SELECT * FROM Kunden WHERE kunden_id=?", (new_id,))
    row = cur.fetchone()
    print(f"✅ READ   — {row['vorname']} {row['nachname']} / {row['email']}")

    # UPDATE
    cur.execute("UPDATE Kunden SET land=? WHERE kunden_id=?", ("Schweiz", new_id))
    print(f"✅ UPDATE — Land auf 'Schweiz' geändert")

    # DELETE
    cur.execute("DELETE FROM Kunden WHERE kunden_id=?", (new_id,))
    print(f"✅ DELETE — Kunde ID={new_id} gelöscht")

    conn.commit()
    conn.close()

# ── Point d'entrée / Einstiegspunkt ──────────────────────────────────────
if __name__ == "__main__":
    init_db()
    seed_data()
    run_queries()
    crud_demo()
    print("\n🎉 Projekt abgeschlossen!")
