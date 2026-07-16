# amd-repo
Acest proiect are scop de fi un Functional Coverage Dashboard.
Va fi o aplicatie web in care utilizator se logheaza si incarca fisiere logs daca are privilegiul de acest.
Backend va parsa datele de pe log: date, procentaj de acoperire si status de bin-uri(HIT/MISS)
Si datele vor fi pastrate in baza de date si ulterior afisate in UI.
## Structura
- `db/` - stratul de persistenta (Base, engine, sesiuni, get_db, modele ORM, Alembic, seed).
- `backend/app/` - API-ul FastAPI (routers / services / repositories / schemas / parser).
- `frontend/` - aplicatie Vue (api / assets / components / router / stores / views)
## Dependinte
- Python 3.14 (testat cu 3.14.6)
- Node.js ^22.18.0 || >=24.12.0 
## Rulare (din radacina proiectului)
1. Mediu Virtual:
- Linux / macOS:
  `python3 -m venv .venv && source .venv/bin/activate`
- Linux (fish):
  `python3 -m venv .venv && source .venv/bin/activate.fish`
- Windows (PowerShell):
  `python -m venv .venv && .venv\Scripts\Activate.ps1`
- Windows (cmd):
  `python -m venv .venv && .venv\Scripts\activate.bat`
2. Instalarea dependentelor `pip install -r requirements.txt`
2. Crearea `.env` dupa modelul `.env.example`  dor cu parametrii completate
3. Migratii:            `alembic -c db/alembic.ini upgrade head`
4. Backend:          `uvicorn backend.app.main:app --reload`
5. Frontend:         ` cd frontend && npm install && npm run dev`
6. Deschide http://localhost:5173 (aplicatia) sau http://localhost:8000/docs (Swagger UI, pentru dev)

Optional:
- Seed:                  `python -m db.seed`
    * De mentionat ca in logs sunt prezente txt eronate/modificate intentionat, deci daca nu este necesar, puteti sterge pana la rularea seed
    * in caz rularii va fi prezente aceste simboluri:
    * [!] - ceea ce zice despre o eroare la incarcarea fisierului
    * [-] - zice ca fisier deja exista
    * [+] - fisier incarcat cu succes

- Teste:                 `cd backend && pytest`

## Politica pentru fisiere duplicate
Daca un fisier cu acelasi nume ca si cel prezent in db este incercat sa fie incarcat, va fi apelat
un error code 409, adica "Conflict", fara sa salveze in db
Scopul: pentru a evita garbage-ing db-ului
## Protejarea GET-urilor
Initial am lasat listarea si detaliile deschise, ca oricine sa poata
vedea simularile - pentru citire nu vedeam un beneficiu clar in logare.
Am schimbat decizia deoarece in context real datele de coverage sunt
confidentiale (arata starea verificarii unui proiect intern), asa ca
acum toate endpoint-urile de citire cer autentificare, atat in frontend
(route guards) cat si in backend (get_current_user).

Diferenta fata de upload: pentru citire e suficient orice cont Google
valid, pe cand upload-ul cere in plus ca emailul sa fie pe allowlist
(vezi sectiunea urmatoare).
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
## Stocharea tokenului
Pentru acest proiect vom utiliza Pinia + localStorage
Se intalege ca riscul utilizand localStorage fiind faptul ca
ea este vulnerabila de injectarea codului, deci se poate de citit,
iar daca vom utiliza dor Pinia, e o soluita la aceasta dar la refresh
datele se pierd.
## Ce am invatat
La acest proiect am invat sa gandesc un sistem pe straturi (router -> service ->
repository in backend, component -> store -> api in frontend) si de ce separarea
aia conteaza, nu doar cum se scrie.

**Sursa unica de adevar nu e doar o regula de stil.** 
Am dat de acelasi bug de doua ori sub forme diferite: 
/api hardcodat separat de baseURL in client.js, si DATABASE_URL 
din .env vs sqlalchemy.url din alembic.ini care puteau sa arate 
spre baze diferite. A doua oara am recunoscut tiparul din prima.

**Cand muti stare dintr-o componenta intr-un store, valorile initiale
conteaza la fel de mult ca logica.** 
Am mutat fetch-ul din RunDetail.vue in store si pagina a ramas alba - v-else 
citea proprietati dintr-un obiect inca null, pentru ca ordinea randare/fetch 
nu mai era aceeasi ca inainte.

**/runs public sau privat?**
Inital am avut pe gand de a lasa partea `/runs` public pentru a permite utilizatorilor
de a observa un tabel cu date incarcate. Problema a aparut cand m-am gandit
despre diferente in drepturi, fiind faptul ca utilizator nelogat si cel logat, dar nu
prezent in allowlist are aproape ca aceeasi drepturi, ceea ce pune sub intrebare abordarea aceasta,
din aceasta am dat seama de a limita accesarea detaliilor a unei rulari selectate din tabel  
pentru cei nelogati, dar apoi am dat seama ca defapt denumirea fisierilor poate zice multe
unui utilizator cu itentii rai, pentru o companie aceasta nu este permisibil, din aceasta cauza
am facut ca accesarea oricarei pagine sa fie permisa dor prin logarea. Daca imaginam un grup/team
care utilizeaza aceasta aplicatie, defapt nu e rau de a avea o logare peste tot si nici nu strica

## Arhitectura
### Backend (FastAPI), stratificat pe 4 nivele:
- `routers/` - definesc endpoint-urile HTTP (validare input, coduri de status, documentatie OpenAPI)
- `services/` - logica de business (ex. `run_service.py` transforma un log parsat intr-un `RunDetail`, calculeaza total_bins/missed_bins)
- `repositories/` - singurul loc care comunica cu baza de date prin SQLAlchemy (query-uri, filtre, paginare)
- `schemas/` - modele Pydantic pentru shape-ul request-urilor si raspunsurilor care sunt separate de modele ORM
Pe langa acestea:
- `parser/` - citeste fisierele .txt de log VCS si le transforma in structuri (coverpoints, bins, rezultat)
- `auth/` - OAuth cu Google + JWT; `get_current_user` verifica doar daca tokenul e valid, `check_email` verifica in plus allowlist-ul (folosit doar pentru upload)
### Baza de date (`db/`):
- Modele SQLAlchemy: `Run` -> `Coverpoint` -> `Bin`
- Migratii cu Alembic; schema se construieste din migratii (`alembic upgrade head`), nu se transporta prin git
- `seed.py` populeaza db-ul din `logs/*.txt`, cu feedback per fisier: `[+]` `[-]` `[!]` fisier invalid.
### Frontend (Vue + Pinia), stratificat similar:
- `views/` - pagini, doar afiseaza UI-ul si cheama store-urile.
- `stores/` (Pinia) - stare + logica de afisare (ex. `auth.js` are `handleCallback(code)`, `runs.js` are `fetchRuns`/`fetchRun`).
- `api/` - apeluri HTTP prin axios (`client.js`, `runs.js`, `auth.js`), fara nicio logica de business.
- `utils/` - help-uri pure (formatare, decodare JWT).
- `router/` - defineste rutele si un guard `beforeEach` care redirectioneaza la `/login` orice ruta cu `meta: {requiresAuth: true}`.
### Fluxul de autentificare
Login cu Google -> `code` -> schimb pe `/auth/token` -> JWT salvat in Pinia + localStorage.
`client.js` ataseaza automat tokenul pe fiecare request si face logout automat la 401.
Protectia e dubla: route guards in frontend + `get_current_user`/`check_email` in backend.
### Fluxul de upload
Fisier .txt -> `parser` il valideaza si extrage datele -> `run_service` verifica daca sunt duplicate (409 daca da) -> salvat in db prin `repository` -> raspuns `RunDetail` cu coverpoints si bins.
