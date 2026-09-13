# virsh-card-shop

Flask API for [virshop](https://github.com/HTJin/virshop): turns a TCGplayer pull-sheet CSV
into a sorted, flagged sheet a card shop can work from, and stores the sheets per user.

## Endpoints

All routes are under `/api` and require a bearer token (`x-access-token`) checked by
`token_required` in `helpers.py`.

| Method | Route | What it does |
|---|---|---|
| `POST` | `/upload` | Accepts a pull-sheet CSV, runs `process_pullsheet`, stores the rows |
| `GET` | `/upload/<csv_name>` | Returns the processed sheet |
| `PUT` | `/upload/<csv_name>/edit` | Updates rows in a stored sheet |
| `DELETE` | `/upload/<csv_name>/remove` | Deletes a sheet |

`process_pullsheet` reads the TCGplayer export, keeps product name, set, number and rarity,
adds an `in_stock` flag from the quantity, and sorts by set, rarity and name so the physical
pull runs in shelf order.

The `Inventory` model keeps every TCGplayer column (market price, direct low, low with
shipping, marketplace price, quantities, photo URL) so later views can price a sheet.

## Also included

Server-rendered pages under `site/` (index, about, profile) and form-based login and
registration under `authentication/`, using Flask-Login and Flask-WTF.

## Stack

Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-WTF, Flask-Cors, gunicorn.

## Run it

```bash
python -m venv .venv && . .venv/Scripts/activate
pip install -r requirements.txt
flask db upgrade
gunicorn -c gunicorn.conf.py "virsh_card_shop:create_app()"
```

Set `DATABASE_URL` and `SECRET_KEY` in the environment (see `config.py`).

Capstone project from my software engineering program, built for a real card shop.
