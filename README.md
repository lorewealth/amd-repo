# amd-repo
Acest proiect are scop de fi un Functional Coverage Dashboard.
Va fi o aplicatie web in care utilizator se logheaza si incarca fisiere logs daca are privilegiul de acest.
Backend va parsa datele de pe log: date, procentaj de acoperire si status de bin-uri(HIT/MISS)
Si datele vor fi pastrate in baza de date si ulterior afisate in UI.
## Structura
- `db/` - stratul de persistenta (Base, engine, sesiuni, get_db, modele ORM, Alembic, seed).
- `backend/app/` - API-ul FastAPI (routers / services / repositories / schemas / parser).
- `frontend/` - aplicatie Vue (api / assets / components / router / stores / views)
## Rulare (din radacina proiectului)
- App:       `uvicorn backend.app.main:app --reload`
- Seed:      `python -m db.seed`
- Migratii:  `alembic -c db/alembic.ini upgrade head`
- Teste:     `cd backend && pytest`
- Frontend:  `cd frontend && npm install && npm run dev`
## Politica pentru fisiere duplicate
Daca un fisier cu acelasi nume ca si cel prezent in db este incercat sa fie incarcat, va fi apelat
un error code 409, adica "Conflict", fara sa salveze in db
Scopul: pentru a evita garbage-ing db-ului
## Get-urile deschise
Le-am lasat deschise fiind faptu ca user sa poate sa vada
simularile, nu este nici un beneficiu de a le proteja, pecand
pentru upload cat de cat sens mai este fiind avem nevoie de
identitatea reala a userului
## Allowlist pentru upload
Upload-ul nu este deschis oricarui care se logheaza prin Google.
Email-ul numaidecat trebuie sa fie in allowed_email_list (.env),
astfel primesti 403 chiar daca token e valid.
Am ales asa abordare din cauza ca login prin Google valideaza 
identitatea unui cont, dar nu se increde daca contul acel
nu este un cont bot, sau un cont cu itentii rele.
## Autentificare in Swagger (doar pentru dev)
1. Completeaza `GOOGLE_CLIENT_ID` si `GOOGLE_CLIENT_SECRET` in `.env`.
2. Deschide  http://localhost:8000/docs, apoi butonul **Authorize** din modal.
3. Alege contul Google.

Campul `client_id` e precompletat (`fcd-swagger-ui` - identificator intern, nu e un client Google),
iar campul `client_secret` **se lasa gol**: endpoint-ul `/auth/token` nu il foloseste,
secretul real sta doar in `.env`.
