import os, re, utils, datetime
class Bulletin:
    '''
    Class that is used to be written in Json for C# communications. 
    \nIn this matter, properties are written according to C# guidelines in order not to create any confusion for the parser.
    '''
    def __init__(self, amount:float, month:int, year:int, filename:str):
        self.amount = amount
        self.month = month
        self.year = year
        self.filename = filename # Path to original document
        self.arrival_day = self.get_receving_day()

    def get_receving_day(self) -> int:
        filename = os.path.basename(self.filename)
        pattern = r'([0-9]{6})([1-2][0-9])' # First group is year and month 
        d = re.search(pattern, filename)
        return int(d.group(2)) # Second group is the day of arrival  and that's what we want

    def to_dict(self):
        return {
            "Amount" : self.amount,
            "Month" : self.month,
            "Year" : self.year,
            "FilePath" : self.filename,
            "ArrivalDay" : self.arrival_day
        }

    def __repr__(self):
        return f"Pour la période du {self.Period}, solde de {self.MonthText}, payé {self.amount}€"
    
class ActivityPeriod:
    def __init__(self):
        self._start_date = None
        self._end_date = None
        self.days_count = 0

    def calc_days(self) -> int:
        delta = self.end_date - self.start_date
        self.days_count = delta.days + 1
        return delta.days

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

    def to_dict(self):
        return{
            "StartDate" : self.start_date.isoformat(),
            "EndDate" : self.end_date.isoformat(),
            "DaysCount": self.calc_days()
        }

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
    
    def calc_days_count(self):
        count = 0
        for p in self.periods:
            count+=p.days_count
        self.days_count = count
        return count
    
    def to_dict(self):
        return{
            "Year": self.year,
            "Month": self.month,
            "DaysCount": self.calc_days_count(),
            "Periods": [p.to_dict() for p in self.periods]
        }

    def __str__(self):
        return f"{self.calc_days_count()} jours sur le mois de {utils.month_name_from_number(self.month)} {self.year}"

    def __repr__(self):
        return f"{self.calc_days_count()} jours sur le mois du {self.month}/{self.year}"