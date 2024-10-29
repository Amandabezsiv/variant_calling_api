FROM python:3.10-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

COPY Snakefile .

ENV FLASK_APP=main.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
