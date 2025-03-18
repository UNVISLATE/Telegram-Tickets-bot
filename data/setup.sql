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
    ID INTEGER NOT NULL,
    AddedBy INTEGER,
    Reason TEXT
);

CREATE INDEX IF NOT EXISTS idx_blacklist_id ON BlackList (ID);
CREATE INDEX IF NOT EXISTS idx_users_id ON Users (ID);