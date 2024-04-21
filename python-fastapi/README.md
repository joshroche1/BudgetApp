# BudgetApp
# from Python 3 Uvicorn/FastAPI Web Application Template

###

NOTE: Use user-management.py to fix users in db after updating repo.

## Dependencies:

- python3
- python3-pip
- python3-dotenv
- python3-sqlalchemy
- python3-bcrypt
- python3-fastapi
- sqlite3 (unless using a different database)
- uvicorn
- gunicorn (manages uvicorn)

To use PostgreSQL:
- postgresql
- (pip) psycopg2

### To run:

uvicorn webapp.main:app \
  --app-dir /home/josh/github/BudgetApp/python-fastapi \
  --env-file /home/josh/github/BudgetApp/python-fastapi/.env \
  --host 0.0.0.0 \
  --port 8000 \
  --log-level info \
  --access-log \
  --use-colors \
  --reload


> gunicorn webapp.main:app -D \
>   --workers 1 \
>   --worker-class uvicorn.workers.UvicornWorker \
>   --chdir /opt/smc/fastapi/ \
>   --bind 0.0.0.0:8000 \
>   --log-level INFO \
>   --log-file /opt/smc/fastapi/gunicorn.log

### Docker

> docker build --tag smc:latest .

> docker container create smc:latest --name smc-py

> docker exec -it --rm NAME/CONTAINERID
