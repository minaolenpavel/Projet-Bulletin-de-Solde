from models import ActivityPeriod, MonthActivity
from PeriodParser import *
import json

class MonthManager:
    def __init__(self, csv_folder:str, pdf_folder:str, filename:str, export_path:str):
        self.filename_export = filename
        self.export_path = export_path 
        self.csv_folder = csv_folder
        self.filenames = utils.list_files(pdf_folder)
        self.months = []
        self.periods = []
        self.days_count = 0

    def month_exist(self, p) -> int:
        y = p.start_date.year
        m = p.start_date.month
        for i, month in enumerate(self.months):
            if month.month == m and month.year == y:
                return i
        else:
            return None

    def create_months(self):
        for file in self.filenames:
            parser = PeriodParser(self.csv_folder)
            periods = parser.create_periods(file)
            self.periods.extend(periods)
        for p in self.periods:
            if self.month_exist(p):
                i = self.month_exist(p)
                self.months[i].periods.append(p)
            else:
                month = MonthActivity(p.start_date.year, p.start_date.month)
                month.periods.append(p)
                self.months.append(month)
    
    def calc_days(self):
        total = 0
        for m in self.months:
            total += m.calc_days_count()
        self.days_count = total
        return total
    
    def export_months_json(self):
        json_list = [m.to_dict() for m in self.months]
        json_str = json.dumps(json_list, indent=2, ensure_ascii=False)
        filename = self.filename_export
        export_path = self.export_path
        utils.write_json(filename, json_str, export_path)

    
    def __str__(self):
        return f"{self.calc_days()} jours effectués du {self.periods[0].start_date.strftime('%A %d %B %Y')} au {self.periods[-1].end_date.strftime('%A %d %B %Y')}"


