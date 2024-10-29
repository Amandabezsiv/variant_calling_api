import os
from app import constants

UPLOADS_FOLDER = os.path.join("data", "annovar_unzip", "annovar", "uploads")
RESULTS_FOLDER = "results"
TABLE_ANNOVAR = os.path.join("data", "annovar_unzip", "annovar", "table_annovar.pl")
HUMAN_DB = os.path.join("data", "annovar_unzip", "annovar", "humandb")
SAMPLE_NAME = "NIST"

VCF_FILE_PATH = os.path.join(UPLOADS_FOLDER, f"{SAMPLE_NAME}.vcf.gz")
ANNOTATED_VCF = os.path.join(RESULTS_FOLDER, f"{SAMPLE_NAME}.hg19_multianno.txt")
ANNOTATED_VCF_INPUT = os.path.join(RESULTS_FOLDER, f"{SAMPLE_NAME}.avinput")
ANNOTATED_VCF_VCF = os.path.join(RESULTS_FOLDER, f"{SAMPLE_NAME}.hg19_multianno.vcf")

rule annotate_variants:
    input:
        vcf=VCF_FILE_PATH
    output:
        annotated_vcf=ANNOTATED_VCF,
        annotated_vcf_input=ANNOTATED_VCF_INPUT,
        annotated_vcf_vcf=ANNOTATED_VCF_VCF
    shell:
        """
        perl {TABLE_ANNOVAR} {input.vcf} {HUMAN_DB} \
        -buildver hg19 -out {RESULTS_FOLDER}/{SAMPLE_NAME} -remove \
        -protocol refGeneWithVer,avsnp138,gnomad211_exome -operation g,f,f -nastring . -vcfinput
        """

rule all:
    input:
        ANNOTATED_VCF,
        ANNOTATED_VCF_INPUT,
        ANNOTATED_VCF_VCF
