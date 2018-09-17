CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key INTEGER UNIQUE NOT NULL,
    title TEXT NOT NULL,
    ref TEXT,
    ref_old TEXT,
    lang TEXT,
    topic TEXT,
    area TEXT,
    width TEXT,
    height TEXT,
    existent BOOLEAN NOT NULL,
    material TEXT,
    author TEXT
);

CREATE TABLE IF NOT EXISTS listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key INTEGER UNIQUE NOT NULL,
    code TEXT UNIQUE NOT NULL,
    title TEXT,
    year INTEGER
);

CREATE TABLE IF NOT EXISTS mentions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    pos INTEGER NOT NULL,
    title TEXT NOT NULL,

    FOREIGN KEY(listing_id) REFERENCES listings(id),
    FOREIGN KEY(book_id) REFERENCES books(id)
);
