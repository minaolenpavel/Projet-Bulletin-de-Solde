import secret
from dataclasses import dataclass

@dataclass
class Config:
    username = secret.username
    password = secret.password

    pdf_folder:str = "bulletins_solde_pdf"
    mail_subject:str = 'SUBJECT "RH-TERRE/AIDDA - BMS"'

    csv_folder = "bulletins_solde_csv"

    json_folder  = "bulletins_solde_json"
    debug = False
