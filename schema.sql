DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  pictureURL TEXT,
  fullName TEXT,
  address TEXT,
  birthday TEXT,
  linkedIn TEXT,
  socialMedia TEXT
);