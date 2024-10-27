import os

# Definindo as entradas e saídas
VCF_FILE = os.path.join("data", "NIST.vcf.gz")  
ANNOTATED_VCF = os.path.join("results", "annotated_variants") #todo test only annotatedvariantes
TABLE_ANNOVAR = os.path.join('annovar',"table_annovar.pl")  
HUMAN_DB = os.path.join("annovar", "humandb")

# Regra para anotar variantes
rule annotate_variants:
    input:
        vcf=VCF_FILE
    output:    
        annotated_vcf=ANNOTATED_VCF
    shell:
        """
        perl {TABLE_ANNOVAR} {VCF_FILE} {HUMAN_DB} \
        -buildver hg19 -out {ANNOTATED_VCF} -remove \
        -protocol refGeneWithVer,avsnp138,gnomad211_exome -operation g,f,f -nastring . -vcfinput
        """
