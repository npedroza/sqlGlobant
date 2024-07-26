## Dockerfile created by NPM jul 15 2024 ###
FROM python:3.11

WORKDIR /app

COPY requirements.txt /app
RUN pip install --requirement /app/requirements.txt

COPY . /app

COPY script.sh /app/script

CMD ["sh", "script"]
