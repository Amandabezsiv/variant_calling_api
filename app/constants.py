import os

ANNOVAR_URL = os.getenv(
    "ANNOVAR_URL",
    "http://www.openbioinformatics.org/annovar/download/annovar.latest.tar.gz",
)
DATA_DIR = "./data/"
ANNOVAR_UNZIP_DIR = os.path.join(DATA_DIR, "annovar_unzip/")
ANNOVAR_DIR = os.path.join(ANNOVAR_UNZIP_DIR, "annovar/")
HUMAN_DB_DIR = os.path.join(ANNOVAR_DIR, "humandb/")
UPLOAD_FOLDER = os.path.join(ANNOVAR_DIR, "uploads/")
SNAKEFILE_PATH = "./Snakefile"
RESULTS = os.path.join("./results/")
OUTPUT_FILE_PATH = os.path.join(RESULTS)
# Download hashs
DOWNLOAD_HASHS_FILE = "./data/record.json"
