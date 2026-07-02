CREATE TABLE runs(
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    filename            TEXT    NOT NULL,
    run_date            TEXT    NOT NULL,
    result              TEXT    NOT NULL,
    checks              INTEGER NOT NULL,
    overall_coverage    NUMERIC(5,2) NOT NULL,
    uploaded_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    uploaded_by         TEXT
);

CREATE TABLE coverpoints(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id      INTEGER NOT NULL,
    name        TEXT    NOT NULL,
    coverage    NUMERIC(5,2) NOT NULL,

    FOREIGN KEY (run_id) REFERENCES runs(id) ON DELETE CASCADE
);

CREATE TABLE bins(
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    coverpoint_id   INTEGER NOT NULL,
    name            TEXT NOT NULL,
    value           TEXT,
    hits            INTEGER NOT NULL,
    hit             BOOLEAN NOT NULL,

    FOREIGN KEY (coverpoint_id) REFERENCES coverpoints(id) ON DELETE CASCADE
);
