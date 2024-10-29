import requests
from tqdm import tqdm
import tarfile
import os
import zipfile
import subprocess
from .constants import ANNOVAR_DIR
import time


def download_url(url, output_path, file_description=""):

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get("content-length", 0))
        chunk_size = 8192

        desc = "Download"
        if file_description:
            desc += f" {file_description}"

        with open(output_path, "wb") as file, tqdm(
            desc=desc,
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                file.write(chunk)
                progress_bar.update(len(chunk))

        print("Download concluído com sucesso!")
    else:
        print(f"Falha ao fazer download. Status code: {response.status_code}")


def extract_tar_gz(tar_path, output_dir, file_description=""):

    desc = "Unziping"
    if file_description:
        desc += f" {file_description}"

    with tarfile.open(tar_path, "r:gz") as tar_ref:
        members = tar_ref.getmembers()
        with tqdm(total=len(members), desc=desc, unit="arquivo") as progress_bar:
            for member in members:
                tar_ref.extract(member, output_dir)
                progress_bar.update(1)

    print("Arquivo descompactado com sucesso!")


def download_annotation_database(build_version, database_name, output_dir):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    command = [
        "perl",
        os.path.join(ANNOVAR_DIR, "annotate_variation.pl"),
        "-buildver",
        build_version,
        "-downdb",
        "-webfrom",
        "annovar",
        database_name,
        output_dir,
    ]

    try:
        subprocess.run(command, check=True)
        print(
            f"Banco de dados '{database_name}' baixado com sucesso na pasta '{output_dir}'."
        )
    except subprocess.CalledProcessError as e:
        print(f"Erro ao baixar o banco de dados: {e}")


def generate_unix_timestamp():
    return int(time.time())
