#syntax=docker/dockerfile:1
FROM python:3.11

WORKDIR /user_ms

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

#CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
#CMD ["python3", "-m", "gunicorn", "-w", "4", "-b", "0.0.0.0:4000", "app:app"]