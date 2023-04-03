### Budget Application
#
# Python 3 based using FastAPI, SQLAlchemy, Uvicorn
#
###

FROM python:3.9

WORKDIR /python-fastapi

COPY ./requirements.txt /python-fastapi/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /python-fastapi/requirements.txt

COPY ./python-fastapi /python-fastapi

CMD ["uvicorn", "webapp.main:app", "--host", "0.0.0.0", "--port", "8000"]
