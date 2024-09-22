# Budget App - FastAPI
### FastAPI

<https://wiki.qt.io/Main>

Contains:
 - FastAPI
 - SQLAlchemy

## Installation

```
apt update; apt install \
 python3 \
 python3-pip \
 python3-dotenv \
 python3-sqlalchemy \
 python3-bcrypt \
 python3-multipart \
 python3-jose \
 python3-passlib \
 python3-fastapi \
 uvicorn \
 sqlite3
# OPTIONAL:
# gunicorn (manages uvicorn)
# postgresql
# (pip) psycopg2
```

### Run Application:

```
uvicorn webapp.main:app \
 --env-file $ENVFILE \
 --host 0.0.0.0 \
 --port 8000 \
 --reload &
```

### Models

> Budget
> - name
> - description
> - currency
> - ownerid
> - owner
> - budgetitems

> BudgetItem
> - name
> - description
> - amount
> - category
> - recurrence
> - duedate
> - budgetid
> - owner

> Account
> - name
> - description
> - accounttype
> - currency
> - ownerid
> - owner

> Transaction
> - datetimestamp
> - amount
> - convertedvalue
> - category
> - currency
> - name
> - description
> - accountid

> User
> - username
> - email
> - password
> - budgets
> - accounts

> Weblist
> - name
> - value

> ExchangeRate
> - currency_from
> - currency_to
> - rate