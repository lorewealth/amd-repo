# amd-repo
Acest proiect are scop de fi un Functional Coverage Dashboard.
Va fi o aplicatie web in care utilizator se logheaza si incarca fisiere logs daca are privilegiul de acest.
Backend va parsa datele de pe log: date, procentaj de acoperire si status de bin-uri(HIT/MISS)
Si datele vor fi pastrate in baza de date si ulterior afisate in UI.
## Structura
- `db/` - stratul de persistenta (Base, engine, sesiuni, get_db, modele ORM, Alembic, seed).
- `backend/app/` - API-ul FastAPI (routers / services / repositories / schemas / parser).

## Rulare (din radacina proiectului)
- App:       `uvicorn backend.app.main:app --reload`
- Seed:      `python -m db.seed`
- Migratii:  `alembic -c db/alembic.ini upgrade head`
- Teste:     `cd backend && pytest`

## Politica pentru fisiere duplicate
Daca un fisier cu acelasi nume ca si cel prezent in db este incercat sa fie incarcat, va fi apelat
un error code 409, adica "Conflict", fara sa salveze in db
Scopul: pentru a evita garbage-ing db-ului
