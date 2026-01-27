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
    
    month_manager = MonthManager(config.csv_folder, config.pdf_folder)
    month_manager.create_months()
    for m in month_manager.months:
        m.calc_days_count()
    db = DB(config.db_path)
    bulletins_data = [(b.amount, b.arrival_day, b.filename, b.month, b.year) for b in bulletin_manager.bulletins]
    db.write_many("INSERT INTO Bulletins (Amount, ArrivalDay, FileName, Month, Year) VALUES (?, ?, ?, ?, ?)", bulletins_data)

    month_rows = [(m.year, m.month,m.calc_days_count()) for m in month_manager.months]
    db.write_many("INSERT INTO MonthActivities (Year, Month, DaysCount) VALUES (?, ?, ?)", month_rows)
    rows = db.fetch("SELECT Id, Year, Month FROM MonthActivities")
    month_id_map = {(year, month): id_ for id_, year, month in rows}
    period_rows = []
    for m in month_manager.months:
        month_id = month_id_map[(m.year, m.month)]
        for p in m.periods:
            period_rows.append((
                p.start_date.isoformat(),
                p.end_date.isoformat(),
                p.days_count,
                month_id
            ))
    db.write_many(
    """
    INSERT INTO ActivityPeriod
    (StartDate, EndDate, DaysCount, MonthActivityId)
    VALUES (?, ?, ?, ?)
    """,
    period_rows)

    db.close()

if __name__ == "__main__":
    stopwatch = Stopwatch()
    stopwatch.start()

    config = Config()

    get_all(config)
    stopwatch.stop()
    print(f"{stopwatch.total_time} secondes pour éxecuter tout le script")
