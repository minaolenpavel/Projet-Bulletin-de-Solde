import re
from utils import filename_without_extension, add_backslash

class PdfExtractor:
    def __init__(self, csv_folder:str):
        self.csv_folder = csv_folder

    def get_period(self, path:str)-> tuple:
        '''
        Input is the original filename, example : '2025_11.pdf'. 
        \nOutput is a tuple as (period, month, year)
        '''
        pattern = r"[0-3][0-9]\/([0-3][0-9])\/(\d+) au [0-3][0-9]\/[0-3][0-9]\/\d+"
        with open(f"{add_backslash(self.csv_folder)}{filename_without_extension(path)}-page-1-table-1.csv", mode = "r", encoding='utf8') as file:
            first_line = file.readline().strip() # Unused line just passing it
            second_line = file.readline().strip() # Relevant info is line 2
            #breakpoint()
            m = re.search(pattern, second_line)
            period = m.group()
            month = m.group(1)
            year = m.group(2)
            return (int(month), int(year))
        
    def get_amount(self, path:str) -> float:
        '''
        Input is the original filename, example : '2025_11.pdf'.
        '''
        try: 
            pattern = r'(Montant : (\d+(\s)?\d+(,\d+)?))'
            with open(f"{add_backslash(self.csv_folder)}{filename_without_extension(path)}-page-1-table-4.csv", mode = "r",  encoding='utf8') as file:
                content = file.read()
                m = re.search(pattern, content)
                amount = m.group(2) # Capture group 2 is the total amount, other capture groups aren't relevant
                amount = amount.replace(" ","") # Will not be able to convert to float if there is a white space between the thousand and the rest
                return float(amount.replace(",",".")) # Caprice
        except:
            amount = 0
            with open(f"{add_backslash(self.csv_folder)}{filename_without_extension(path)}-page-2-table-1.csv", mode = "r",  encoding='utf8') as file:
                content = file.readlines()
                amount = content[5].strip().replace('"', "")
                amount = amount.replace(" ", "")
                amount = amount.replace(",", ".")
                file.close()
            return float(amount)

