DROP TABLE IF EXISTS users;

CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    maiden_name TEXT,
    mothers_name TEXT NOT NULL,
    pob TEXT NOT NULL,
    dob TEXT NOT NULL,
    address TEXT NOT NULL,
    tax_num TEXT UNIQUE NOT NULL,
    taj_number TEXT UNIQUE NOT NULL,
    job_title TEXT NOT NULL,
    base_pay INTEGER NOT NULL
)