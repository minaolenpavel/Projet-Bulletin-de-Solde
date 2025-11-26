from imap_solde_retriever import *
from pdf_extract import *
from models import *
from utils import *
import os

def create_bulletin(amount:float, period:tuple, pdf_path:str) -> Bulletin:
    bulletin = Bulletin(amount, period[0], period[1], period[2], os.path.abspath(pdf_path))
    return bulletin

def main(debug:bool):
    stopwatch = Stopwatch()
    stopwatch.start()
    dl_bulletins(debug)
    bulletins_pdf_paths = list_files("./bulletins_solde_pdf")
    for bulletin_pdf_path in bulletins_pdf_paths:
        csv_folder = create_csv(bulletin_pdf_path)
        pure_path = os.path.basename(bulletin_pdf_path)
        amount = get_amount(pure_path, csv_folder)
        period = get_period(pure_path, csv_folder)
        bulletin = create_bulletin(amount, period, bulletin_pdf_path)
        json_data = json_serialize(bulletin)
        write_json(bulletin_pdf_path, json_data)
    stopwatch.stop()
    print(f"{stopwatch.total_time} secondes pour éxecuter tout le script")

if __name__ == "__main__":
    # Boolean to print some more logs, it's not perfect at all !
    debug = False
    main(debug)

