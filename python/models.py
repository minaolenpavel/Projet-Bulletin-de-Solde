from utils import month_name_from_number

class SoldeMois:
    def __init__(self, amount:float, period:str, month:str, year:int, path:str):
        self.amount = amount
        self.period = period
        self.month = month
        self.month_text = month_name_from_number(month)
        self.year = year
        self.path = path # Path to original document
    
    def __repr__(self):
        return f"Pour la période du {self.period}, solde de {self.month_text}, payé {self.amount}€"