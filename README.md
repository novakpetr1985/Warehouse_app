# Warehouse API

Jednoduché REST API pro evidenci skladových materiálů a jejich pohybů. Aplikace je postavená na FastAPI, SQLAlchemy a SQLite.

## Co umí

- spravovat materiály: název, množství, QR kód, umístění a poznámku;
- evidovat příjem (`IN`) a výdej (`OUT`) a při pohybu automaticky upravit zásobu;
- odmítnout výdej nad dostupné množství;
- poskytovat health, liveness a readiness endpointy.

## Spuštění

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Dokumentace API je po spuštění na [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Důležité endpointy

| Oblast | Endpointy |
| --- | --- |
| Stav služby | `GET /`, `GET /health`, `GET /health/live`, `GET /health/ready` |
| Materiály | `GET/POST /materials/`, `GET/PUT/PATCH/DELETE /materials/{id}` |
| Pohyby | `GET/POST /movements/`, `GET/PUT/PATCH/DELETE /movements/{id}` |

Hromadné smazání je dostupné přes `DELETE /materials/all` a `DELETE /movements/all`. Vyžaduje hlavičku `X-API-Key` shodnou s proměnnou prostředí `WAREHOUSE_API_KEY`:

```powershell
$env:WAREHOUSE_API_KEY = "zvol-si-vlastni-klic"
```

## Databáze a ukázková data

Databáze `warehouse.db` je lokální soubor a není součástí Gitu. Při prvním spuštění API se automaticky vytvoří prázdná SQLite databáze v kořeni projektu, včetně tabulek `materials` a `movements`. Projekt proto lze spustit na jiném počítači i bez existující databáze.

Ukázkové JSON požadavky jsou v adresáři `_others`:

- `POST_FastAPI-Materials.json` pro vytvoření materiálů;
- `POST_FastAPI-Movements.json` pro vytvoření pohybů.

Odešli je přes Swagger nebo Postman. Při vytváření pohybů nejdříve vytvoř materiály a použij jejich skutečná ID.

Pro rychlou ruční kontrolu ve Swaggeru:

- ověř `GET /health/ready`;
- vytvoř nový materiál a ověř jeho zobrazení v seznamu i detailu;
- proveď `IN` a zkontroluj zvýšení zásoby;
- proveď `OUT` a zkontroluj snížení zásoby;
- zkus `OUT` nad dostupné množství — API vrátí `409`;
- zkus neplatný typ pohybu nebo nulové množství — validace vrátí `422`;
- ověř, že hromadné mazání bez správného klíče vrací `403`.

## Testy

```powershell
pytest
```

Testy používají oddělenou dočasnou SQLite databázi a nemění `warehouse.db`.

## Omezení prototypu

Úprava nebo smazání již zaúčtovaného pohybu zatím neupravuje množství materiálu zpět. V produkční verzi by pohyby měly být neměnným auditem, případně by se měly opravovat kompenzačním pohybem.
