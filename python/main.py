from MailRetriever import *
from PdfExtractor import *
from csv_parser import *
from models import *
from utils import *
from MonthManager import *
from config import Config
import os
from BulletinManager import BulletinManager

def retrieve_processed_files(processed_files_path: str):
    if not os.path.exists(processed_files_path):
        return None
    with open(processed_files_path, 'r', encoding='utf-8') as file:
        processed_files_list = json.load(file)
    return processed_files_list

def write_processed(processed_files_path:str, processed_files:list):
    processed_files_list = retrieve_processed_files(processed_files_path)
    if not processed_files_list:
        processed_files_list = processed_files
    else:
        processed_files_list.extend(processed_files)
    
    json_data = json.dumps(processed_files_list)
    write_json(filename='processed_files', data=json_data)

def main(config:Config):
    processed_files = retrieve_processed_files(config.processed_files_list_path)
    mailRetriever = MailRetriever(
        config.username,
        config.password,
        config.imap_ssl_host,
        config.mail_subject,
        config.debug)

    mailRetriever.download_missing_payslips(config.pdf_folder, processed_files)
    extractor = PdfExtractor(config.csv_folder)

    bulletin_manager = BulletinManager(config.csv_folder, config.pdf_folder, "./")
    bulletins_pdf_paths = list_files(config.pdf_folder)
    bulletins_pdf_paths = [p for p in bulletins_pdf_paths if os.path.basename(p) not in processed_files]
    if len(bulletins_pdf_paths) == 0:
        if config.debug:
            print("Nothing new")
    else:
        for bulletin_pdf_path in bulletins_pdf_paths:
            parse_pdf_to_csv(bulletin_pdf_path, config.csv_folder)
            basename_path = os.path.basename(bulletin_pdf_path)
            amount = extractor.get_amount(basename_path)
            period = extractor.get_period(basename_path)
            bulletin_manager.create_bulletin(amount, period, bulletin_pdf_path)
        bulletins_pdf_paths = [os.path.basename(f) for f in bulletins_pdf_paths]
        write_processed(config.processed_files_list_path, bulletins_pdf_paths)

def get_months(config:Config):
    month_manager = MonthManager(config.csv_folder, config.pdf_folder)
    month_manager.create_months()
    for m in month_manager.months:
        m.calc_days_count()
    print(month_manager)
    month_manager.export_months_json()

if __name__ == "__main__":
    stopwatch = Stopwatch()
    stopwatch.start()
    
    config = Config()


    main(config)
    #get_months(config)

    stopwatch.stop()
    print(f"{stopwatch.total_time} secondes pour éxecuter tout le script")

