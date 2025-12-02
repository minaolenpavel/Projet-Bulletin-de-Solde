from utils import month_name_from_number

class Bulletin:
    '''
    Class that is used to be written in Json for C# communications. 
    \nIn this matter, properties are written according to C# guidelines in order not to create any confusion for the parser.
    '''
    def __init__(self, amount:float, period:str, month:str, year:int, path:str):
        self.Amount = amount
        self.Period = period
        self.Month = month
        self.Year = year
        self.FilePath = path # Path to original document
    
    def __repr__(self):
        return f"Pour la période du {self.Period}, solde de {self.MonthText}, payé {self.Amount}€"