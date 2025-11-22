from utils import month_name_from_number

class SoldeMois:
    def __init__(self, amount:float, period:str, month:str, year:int):
        self.amount = amount
        self.period = period
        self.month = month
        self.month_text = month_name_from_number(month)
        self.year = year