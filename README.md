# Warehouse API

Warehouse API je REST API pro základní skladovou evidenci. Umožňuje spravovat materiály, evidovat příjem a výdej a automaticky přepočítat aktuální množství na skladě.

Verze: **1.0.0**

## Funkce

- evidence materiálů: název, množství, QR kód, umístění a poznámka;
- příjem (`IN`) a výdej (`OUT`) materiálu;
- automatická změna zásoby při vytvoření pohybu;
- ochrana proti výdeji nad dostupné množství;
- health, liveness a readiness endpointy;
- interaktivní OpenAPI dokumentace a Postman kolekce.

## Technologie

- Python a FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- pytest

## Rychlý start

Vyžadován je Python 3.10 nebo novější.

```powershell
git clone <url-repozitare>
cd Warehouse_app
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API bude dostupné na [http://127.0.0.1:8000](http://127.0.0.1:8000) a Swagger UI na [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Terminál s příkazem `uvicorn` musí během práce s Postmanem zůstat spuštěný.

## Lokální databáze

Aplikace používá SQLite soubor `warehouse.db` v kořeni projektu. Soubor není verzovaný a je uvedený v `.gitignore`.

Při prvním spuštění se databáze a tabulky `materials` a `movements` vytvoří automaticky. Stažený repozitář proto lze spustit na novém počítači i bez databáze; začne pouze s prázdnými daty.

Ukázkové JSON požadavky pro ruční vložení dat jsou v adresáři `_others`:

- `POST_FastAPI-Materials.json` — materiály;
- `POST_FastAPI-Movements.json` — pohyby.

Nejprve vytvoř materiály a až poté pohyby s jejich skutečnými ID.

## API endpointy

| Oblast | Metoda a cesta | Účel |
| --- | --- | --- |
| Služba | `GET /` | Základní stav aplikace. |
| Služba | `GET /health` | Dostupnost API. |
| Služba | `GET /health/live` | Liveness probe procesu. |
| Služba | `GET /health/ready` | Readiness probe databáze a tabulek. |
| Materiály | `GET /materials/` | Seznam materiálů včetně počtu položek. |
| Materiály | `POST /materials/` | Vytvoření materiálu. |
| Materiály | `GET /materials/{id}` | Detail materiálu. |
| Materiály | `PUT /materials/{id}` | Úplná změna materiálu. |
| Materiály | `PATCH /materials/{id}` | Částečná změna materiálu. |
| Materiály | `DELETE /materials/{id}` | Smazání materiálu. |
| Materiály | `DELETE /materials/all` | Hromadné smazání materiálů. |
| Pohyby | `GET /movements/` | Seznam pohybů. |
| Pohyby | `POST /movements/` | Vytvoření pohybu a přepočet zásoby. |
| Pohyby | `GET /movements/{id}` | Detail pohybu. |
| Pohyby | `PUT /movements/{id}` | Úplná změna pohybu. |
| Pohyby | `PATCH /movements/{id}` | Částečná změna pohybu. |
| Pohyby | `DELETE /movements/{id}` | Smazání pohybu. |
| Pohyby | `DELETE /movements/all` | Hromadné smazání pohybů. |

Kompletní požadavky a schémata jsou dostupné ve Swagger UI.

## Pravidla skladových pohybů

Při `POST /movements/` je nutné zadat existující `material_id`, typ pohybu `IN` nebo `OUT` a kladné `quantity`.

- `IN` zvýší množství materiálu.
- `OUT` sníží množství materiálu.
- Výdej nad dostupné množství je odmítnut.

Příklad příjmu:

```json
{
  "material_id": 1,
  "movement_type": "IN",
  "quantity": 10,
  "to_location": "RECEIVING",
  "note": "Příjem zboží"
}
```

## Chybové odpovědi

| HTTP stav | Význam |
| --- | --- |
| `403` | Chybí nebo nesouhlasí API klíč pro hromadné mazání. |
| `404` | Požadovaný materiál nebo pohyb neexistuje. |
| `409` | Výdej převyšuje aktuální zásobu. |
| `422` | Neplatný vstup, například typ pohybu jiný než `IN`/`OUT` nebo nečíselné ID v URL. |
| `503` | Databáze či požadované tabulky nejsou připravené. |

## Hromadné mazání

Hromadné mazání je záměrně chráněné. Před spuštěním serveru nastav API klíč:

```powershell
$env:WAREHOUSE_API_KEY = "zvol-si-vlastni-klic"
uvicorn app.main:app --reload
```

Do požadavku přidej hlavičku:

```text
X-API-Key: zvol-si-vlastni-klic
```

Bez klíče API vrátí `403 Forbidden`.

## Postman

Importuj [Postman/Warehouse API.postman_collection.json](Postman/Warehouse%20API.postman_collection.json). Kolekce má výchozí hodnotu `baseUrl` nastavenou na `http://127.0.0.1:8000`.

Pro automatický průchod spusť v tomto pořadí složky `Health`, `Materials`, `Movements` a `Cleanup`. Kolekce vytvoří testovací materiál a pohyb, předá jejich ID do dalších požadavků a na konci je smaže.

Složku `Dangerous - run manually` při běžném běhu nevybírej. Obsahuje hromadná mazání a vyžaduje proměnnou `apiKey` se stejnou hodnotou jako `WAREHOUSE_API_KEY` serveru.

## Testy

```powershell
pytest -q
```

Testy používají samostatnou dočasnou SQLite databázi v paměti. Nemění lokální `warehouse.db`.

## Omezení verze 1.0.0

Úprava nebo smazání již zaúčtovaného pohybu zatím nepřepočítá množství materiálu. Pro korekci zásoby proto v této verzi vytvářej nový kompenzační pohyb `IN` nebo `OUT`. Budoucí verze může pohyby změnit na neměnný auditní záznam.
