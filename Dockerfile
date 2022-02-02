FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt

COPY /app/ /app/

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:5000", "--timeout", "600", "app:app" ]
