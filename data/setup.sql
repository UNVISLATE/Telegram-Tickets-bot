CREATE TABLE IF NOT EXISTS Users (
    ID INTEGER NOT NULL UNIQUE,
    username TEXT,
    ticketID INTEGER,
    language TEXT
);

CREATE TABLE IF NOT EXISTS AdminRate (
    id INTEGER,
    rate INTEGER,
    date TEXT,
    uid INTEGER
);

CREATE TABLE IF NOT EXISTS Messages (
    ID INTEGER,
    ticketID INTEGER,
    content TEXT,
    date TEXT,
    uid INTEGER
);

CREATE TABLE IF NOT EXISTS BlackList (
    ID INTEGER,
    AddedBy INTEGER,
    Reason TEXT
);