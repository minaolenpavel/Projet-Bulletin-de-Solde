from MailRetriever import *
from PdfExtractor import *
from csv_parser import *
from models import *
from utils import *
from MonthManager import *
from config import Config
import os
from BulletinManager import BulletinManager
from DB import *


def get_all(config:Config):
    mailRetriever = MailRetriever(
        config.username,
        config.password,
        config.imap_ssl_host,
        config.mail_subject,
        config.debug
    )

    #mailRetriever.export_emails_date()
    mailRetriever.download_payslips(config.pdf_folder)
    extractor = PdfExtractor(config.csv_folder)
    bulletin_manager = BulletinManager(
        config.csv_folder, 
        config.pdf_folder
        )
    bulletins_pdf_paths = list_files(config.pdf_folder)
    for bulletin_pdf_path in bulletins_pdf_paths:
        parse_pdf_to_csv(
            bulletin_pdf_path,
            config.csv_folder
        )
        basename_path = os.path.basename(bulletin_pdf_path)
        amount = extractor.get_amount(basename_path)
        period = extractor.get_period(basename_path)
        bulletin_manager.create_bulletin(
            amount, 
            period, 
            bulletin_pdf_path)
    
    db = DB(config.db_path)
    bulletins_data = [(b.amount, b.arrival_day, b.file_path, b.month, b.year) for b in bulletin_manager.bulletins]
    db.write_many("INSERT INTO Bulletins (Amount, ArrivalDay, FileName, Month, Year) VALUES (?, ?, ?, ?, ?)", bulletins_data)
    db.close()

if __name__ == "__main__":
    stopwatch = Stopwatch()
    stopwatch.start()

    config = Config()

    get_all(config)
    stopwatch.stop()
    print(f"{stopwatch.total_time} secondes pour éxecuter tout le script")
