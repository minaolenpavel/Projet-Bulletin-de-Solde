from imap_solde_retriever import *
from pdf_extract import *
from models import *
from utils import *
from config import Config
import os

def create_bulletin(amount:float, period:tuple, pdf_path:str) -> Bulletin:
    bulletin = Bulletin(amount, period[0], period[1], period[2], os.path.abspath(pdf_path))
    return bulletin

def main(debug:bool):
    config = Config()

    dl_bulletins(
        config.pdf_folder,
        config.debug, 
        config.mail_subject)
    
    bulletins_pdf_paths = list_files(config.pdf_folder)
    for bulletin_pdf_path in bulletins_pdf_paths:
        csv_folder = create_csv(
            bulletin_pdf_path,
            config.csv_folder)
        basename_path = os.path.basename(bulletin_pdf_path)
        amount = get_amount(
            basename_path, 
            config.csv_folder)
        period = get_period(
            basename_path, 
            config.csv_folder)
        bulletin = create_bulletin(amount, period, bulletin_pdf_path)
        json_data = json_serialize_bulletin(bulletin)
        write_json(
            bulletin_pdf_path, 
            json_data,
            config.json_folder)


if __name__ == "__main__":
    stopwatch = Stopwatch()
    stopwatch.start()
    # Boolean to print some more succinct logs
    debug = False
    main(debug)
    stopwatch.stop()
    print(f"{stopwatch.total_time} secondes pour éxecuter tout le script")

