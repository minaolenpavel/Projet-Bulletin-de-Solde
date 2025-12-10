import os, re, utils, datetime
class Bulletin:
    '''
    Class that is used to be written in Json for C# communications. 
    \nIn this matter, properties are written according to C# guidelines in order not to create any confusion for the parser.
    '''
    def __init__(self, amount:float, month:int, year:int, path:str):
        self.Amount = amount
        self.Month = month
        self.Year = year
        self.FilePath = path # Path to original document
        self.ArrivalDay = self.get_receving_day()

    def get_receving_day(self) -> int:
        filename = os.path.basename(self.FilePath)
        pattern = r'([0-9]{6})([1-2][0-9])' # First group is year and month 
        d = re.search(pattern, filename)
        return int(d.group(2)) # Second group is the day of arrival  and that's what we want

    
    def __repr__(self):
        return f"Pour la période du {self.Period}, solde de {self.MonthText}, payé {self.Amount}€"
    
class ActivityPeriod:
    def __init__(self):
        self._start_date = None
        self._end_date = None
        self.days_count = 0

    def calc_days(self) -> int:
        delta = self.end_date - self.start_date
        if delta.days == 0:
            self.days_count = 1
        else:
            self.days_count = delta.days

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, date):
        if isinstance(date, datetime.date):
            self._start_date = date
        else:
            new_date = utils.str_to_datetime(date)
            self.start_date = new_date

    @property
    def end_date(self):
        return self._end_date
    
    @end_date.setter
    def end_date(self, date):
        if isinstance(date, datetime.date):
            self._end_date = date
        else:
            new_date = utils.str_to_datetime(date)
            self._end_date = new_date

    def __lt__(self, other):
        return self.end_date < other.start_date
    def __repr__(self):
        return f"periode du {self.start_date} au {self.end_date}"
    
class MonthActivity:
    def __init__(self, year:int, month:int):
        self.year = year
        self.month = month
        self.periods = []
        self.days_count = 0 