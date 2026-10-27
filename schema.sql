-- schema.sql
-- Schéma relationnel e-commerce (3NF) / Relationales E-Commerce-Schema (3NF)

-- Clients / Kunden
CREATE TABLE IF NOT EXISTS Kunden (
    kunden_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    vorname     TEXT NOT NULL,
    nachname    TEXT NOT NULL,
    email       TEXT UNIQUE NOT NULL,
    land        TEXT NOT NULL DEFAULT 'Deutschland',
    erstellt_am TEXT NOT NULL DEFAULT (DATE('now'))
);

-- Kategorien / Kategorien
CREATE TABLE IF NOT EXISTS Kategorien (
    kategorie_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    bezeichnung    TEXT UNIQUE NOT NULL
);

-- Produkte / Produkte
CREATE TABLE IF NOT EXISTS Produkte (
    produkt_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL,
    beschreibung TEXT,
    preis        REAL NOT NULL CHECK(preis > 0),
    lagerbestand INTEGER NOT NULL DEFAULT 0 CHECK(lagerbestand >= 0),
    kategorie_id INTEGER NOT NULL,
    FOREIGN KEY (kategorie_id) REFERENCES Kategorien(kategorie_id)
);

-- Bestellungen / Commandes
CREATE TABLE IF NOT EXISTS Bestellungen (
    bestell_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    kunden_id   INTEGER NOT NULL,
    bestell_datum TEXT NOT NULL DEFAULT (DATE('now')),
    status      TEXT NOT NULL DEFAULT 'offen'
                CHECK(status IN ('offen','versendet','geliefert','storniert')),
    FOREIGN KEY (kunden_id) REFERENCES Kunden(kunden_id)
);

-- Bestellpositionen / Lignes de commande
CREATE TABLE IF NOT EXISTS Bestellpositionen (
    position_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    bestell_id   INTEGER NOT NULL,
    produkt_id   INTEGER NOT NULL,
    menge        INTEGER NOT NULL CHECK(menge > 0),
    einzelpreis  REAL NOT NULL CHECK(einzelpreis > 0),
    FOREIGN KEY (bestell_id) REFERENCES Bestellungen(bestell_id),
    FOREIGN KEY (produkt_id) REFERENCES Produkte(produkt_id)
);

-- Bewertungen / Avis
CREATE TABLE IF NOT EXISTS Bewertungen (
    bewertung_id INTEGER PRIMARY KEY AUTOINCREMENT,
    kunden_id    INTEGER NOT NULL,
    produkt_id   INTEGER NOT NULL,
    sterne       INTEGER NOT NULL CHECK(sterne BETWEEN 1 AND 5),
    kommentar    TEXT,
    datum        TEXT NOT NULL DEFAULT (DATE('now')),
    FOREIGN KEY (kunden_id) REFERENCES Kunden(kunden_id),
    FOREIGN KEY (produkt_id) REFERENCES Produkte(produkt_id),
    UNIQUE(kunden_id, produkt_id)
);

-- Zahlungen / Paiements
CREATE TABLE IF NOT EXISTS Zahlungen (
    zahlung_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    bestell_id   INTEGER NOT NULL UNIQUE,
    betrag       REAL NOT NULL CHECK(betrag > 0),
    methode      TEXT NOT NULL CHECK(methode IN ('Kreditkarte','PayPal','Überweisung')),
    datum        TEXT NOT NULL DEFAULT (DATE('now')),
    FOREIGN KEY (bestell_id) REFERENCES Bestellungen(bestell_id)
);

-- Index pour les performances / Indizes für Performance
CREATE INDEX IF NOT EXISTS idx_produkte_kategorie ON Produkte(kategorie_id);
CREATE INDEX IF NOT EXISTS idx_bestellungen_kunde ON Bestellungen(kunden_id);
CREATE INDEX IF NOT EXISTS idx_positionen_bestell ON Bestellpositionen(bestell_id);
