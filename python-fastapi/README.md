# Budget App 
## based on Python FastAPI Template
<https://github.com/joshroche1/projects/tree/master/templates/>

<http://fastapi.tiangolo.com>

Contains:
 - FastAPI
 - SQLAlchemy
 - Uvicorn

## Directory Structure

- .env
- db.sqlite
- /webapp/
- - __init__.py
- - main.py
- - auth.py
- - config.py
- - database.py
- - models.py
- - schema.py
- /templates/
- - base.html
- - index.html
- - login.html
- - settings.html
- /static/
- - CSS, JS, IMG, ect...

## Web/REST Endpoints:

<http://localhost:8000/>

<http://localhost:8000/login>

## To Run in Developer Mode:

> uvicorn webapp.main:app --reload

### Build

> uvicorn
