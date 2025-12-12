from MailRetriever import *
from PdfExtractor import *
from csv_parser import *
from Models import *
from utils import *
from MonthManager import *
from config import Config
import os

def create_bulletin(amount:float, period:tuple, pdf_path:str) -> Bulletin:
    bulletin = Bulletin(amount, period[0], period[1], os.path.abspath(pdf_path))
    return bulletin

def main(config:Config):
    mailRetriever = MailRetriever(
        config.username,
        config.password,
        config.imap_ssl_host,
        config.mail_subject,
        config.debug)

    #mailRetriever.export_emails_date()
    mailRetriever.download_payslips(config.pdf_folder)
    
    extractor = PdfExtractor(config.csv_folder)

    bulletins_pdf_paths = list_files(config.pdf_folder)
    for bulletin_pdf_path in bulletins_pdf_paths:
        parse_pdf_to_csv(
            bulletin_pdf_path,
            config.csv_folder)
        basename_path = os.path.basename(bulletin_pdf_path)
        amount = extractor.get_amount(
            basename_path)
        period = extractor.get_period(
            basename_path)
        bulletin = create_bulletin(amount, period, bulletin_pdf_path)
        json_data = json_serialize_bulletin(bulletin)
        write_json(
            bulletin_pdf_path, 
            json_data,
            config.json_folder)

def get_months(config:Config):
    month_manager = MonthManager(config.csv_folder, config.pdf_folder, "exported_activity", "./")
    month_manager.create_months()
    for m in month_manager.months:
        m.calc_days_count()
    print(month_manager)
    month_manager.export_months_json()

if __name__ == "__main__":
    stopwatch = Stopwatch()
    stopwatch.start()
    
    config = Config()


    #main(config)
    get_months(config)

    stopwatch.stop()
    print(f"{stopwatch.total_time} secondes pour éxecuter tout le script")

