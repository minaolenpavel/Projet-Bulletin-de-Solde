import os, re

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