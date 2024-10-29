FROM python:3.12

ENV ANNOVAR_URL=https://www.openbioinformatics.org/annovar/download/0wgxR2rIVP/annovar.latest.tar.gz

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY app/ .

ENV FLASK_APP=__init__.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
