from flask import (
    Flask,
    request,
    jsonify,
    send_file,
    send_from_directory,
    render_template,
)
import time
import os
from dotenv import load_dotenv
from .utils import (
    download_url,
    extract_tar_gz,
    download_annotation_database,
    generate_unix_timestamp,
)
from .constants import (
    ANNOVAR_URL,
    DATA_DIR,
    ANNOVAR_UNZIP_DIR,
    HUMAN_DB_DIR,
    DOWNLOAD_HASHS_FILE,
    UPLOAD_FOLDER,
    SNAKEFILE_PATH,
    RESULTS,
)
import json
import subprocess
import pandas as pd
import zipfile
import io

load_dotenv(".env")


def create_app():
    # Download annovar
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
        download_url(
            ANNOVAR_URL,
            os.path.join(DATA_DIR, "annovar.lastest.tar.gz"),
            "annovar.gz",
        )

    # Unzip annovar
    if not os.path.isdir(ANNOVAR_UNZIP_DIR):
        os.makedirs(ANNOVAR_UNZIP_DIR, exist_ok=True)
        extract_tar_gz(
            os.path.join(DATA_DIR, "annovar.lastest.tar.gz"),
            ANNOVAR_UNZIP_DIR,
            "annovar.lastest.tar.gz",
        )

    # Download db's
    if os.path.isfile(DOWNLOAD_HASHS_FILE):
        with open(DOWNLOAD_HASHS_FILE, "r") as file:
            download_hashs = json.load(file)
    else:
        download_hashs = {}

    dbs_ids = ["gnomad211_exome", "avsnp138"]

    for db_id in dbs_ids:

        if not download_hashs.get(db_id, False):
            download_annotation_database("hg19", db_id, HUMAN_DB_DIR)
            download_hashs[db_id] = generate_unix_timestamp()

    with open(DOWNLOAD_HASHS_FILE, "w") as file:
        json.dump(download_hashs, file, indent=4)

    app = Flask(__name__)

    if not os.path.isdir(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    if not os.path.isdir(RESULTS):
        os.makedirs(RESULTS, exist_ok=True)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/upload-vcf-gz", methods=["POST"])
    def upload_vcf_gz():
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if file and file.filename.endswith(".vcf.gz"):
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            if os.listdir(RESULTS):
                return send_results()

            start_time = time.time()
            try:
                subprocess.run(
                    [
                        "snakemake",
                        "--snakefile",
                        SNAKEFILE_PATH,
                        "--cores",
                        "3",
                    ],
                    check=True,
                )
                end_time = time.time()  # Marca o tempo final
                elapsed_time = end_time - start_time  # Calcula o tempo decorrido
                print(f"Pipeline concluído em {elapsed_time:.2f} segundos")
                return send_results()

            except subprocess.CalledProcessError as e:
                return jsonify({"error": f"Snakemake execution failed: {str(e)}"}), 500

        return (
            jsonify({"error": "Invalid file format. Please upload a .vcf.gz file."}),
            400,
        )

    def send_results():

        txt_file = None
        vcf_file = None

        for file_name in os.listdir(RESULTS):
            if file_name.endswith(".txt"):
                txt_file = os.path.join(RESULTS, file_name)
            elif file_name.endswith(".vcf"):
                vcf_file = os.path.join(RESULTS, file_name)

        if txt_file and vcf_file:
            memory_file = io.BytesIO()
            try:
                with zipfile.ZipFile(memory_file, "w") as zf:
                    zf.write(txt_file, arcname=os.path.basename(txt_file))
                    zf.write(vcf_file, arcname=os.path.basename(vcf_file))
                memory_file.seek(0)

                if memory_file.getbuffer().nbytes == 0:
                    return jsonify({"error": "ZIP file is empty"}), 500

                return send_file(
                    memory_file,
                    as_attachment=True,
                    download_name="output_files.zip",
                    mimetype="application/zip",
                )
            except Exception as e:
                return jsonify({"error": f"Error creating ZIP file: {str(e)}"}), 500

        elif txt_file:
            return send_file(
                txt_file,
                as_attachment=True,
                download_name="output.txt",
                mimetype="text/plain",
            )
        elif vcf_file:
            return send_file(
                vcf_file,
                as_attachment=True,
                download_name="output.vcf",
                mimetype="text/plain",
            )
        else:
            return jsonify({"error": "No .txt or .vcf files found"}), 500

    if __name__ == "__main__":
        app.run(debug=True)

    return app
