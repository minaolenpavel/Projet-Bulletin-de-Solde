import camelot.io as camelot
import re
from utils import filename_without_extension, add_backslash
from models import Bulletin
import gc

def create_csv(path:str, export_folder:str) -> None:
    '''
    Takes the path of a PDF and gives out one or several CSV tables out of it
    '''
    data = camelot.read_pdf(path)
    export_path = add_backslash(export_folder) + filename_without_extension(path) + ".csv"
    data.export(export_path, f = "csv", compress=False)
    # Ensures the files are not still opened and used
    del data
    gc.collect()
    return export_folder

def get_period(path:str, csv_folder:str)-> tuple:
    '''
    Input is the original filename, example : '2025_11.pdf'. 
    \nOutput is a tuple as (period, month, year)
    '''
    pattern = r"[0-3][0-9]\/([0-3][0-9])\/(\d+) au [0-3][0-9]\/[0-3][0-9]\/\d+"
    with open(f"{add_backslash(csv_folder)}{filename_without_extension(path)}-page-1-table-1.csv", mode = "r", encoding='utf8') as file:
        first_line = file.readline().strip() # Unused line just passing it
        second_line = file.readline().strip() # Relevant info is line 2
        #breakpoint()
        m = re.search(pattern, second_line)
        period = m.group()
        month = m.group(1)
        year = m.group(2)
        return (period, int(month), int(year))
    
def get_amount(path:str, csv_folder:str) -> float:
    '''
    Input is the original filename, example : '2025_11.pdf'.
    '''
    #pattern = r'(Montant : (\d+(,\d+)?))'
    pattern = r'(Montant : (\d+(\s)?\d+(,\d+)?))'
    with open(f"{add_backslash(csv_folder)}{filename_without_extension(path)}-page-1-table-4.csv", mode = "r",  encoding='utf8') as file:
        content = file.read()
        m = re.search(pattern, content)
        amount = m.group(2) # Capture group 2 is the total amount, other capture groups aren't relevant
        amount = amount.replace(" ","") # Will not be able to convert to float if there is a white space between the thousand and the rest
        return float(amount.replace(",",".")) # Caprice

if __name__ == "__main__":
    path = "test.pdf"
    print(get_amount(path))
    #create_csv(path)
    #get_period(path)
    #test = SoldeMois()
