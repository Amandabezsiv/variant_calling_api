# Usa uma imagem base do Python
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos da aplicação para o diretório de trabalho
COPY app/ .

# Copia o Snakefile para o diretório de trabalho
COPY Snakefile .

# Define a variável de ambiente para o Flask
ENV FLASK_APP=main.py

# Expõe a porta que o Flask irá usar
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["flask", "run", "--host=0.0.0.0"]
