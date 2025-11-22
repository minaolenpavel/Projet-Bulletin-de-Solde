import camelot.io as camelot
import os, re
from utils import filename_without_extension

def create_csv(path:str) -> None:
    '''
    Takes the path of a PDF and gives out one or several CSV tables out of it
    '''
    data = camelot.read_pdf(path)
    export_path = filename_without_extension(path) + ".csv"
    data.export(export_path, f = "csv", compress=False)

def get_period(path:str)-> tuple:
    '''
    Output is a tuple as (period, month, year)
    '''
    pattern = r"[0-3][0-9]\/([0-3][0-9])\/(\d+) au [0-3][0-9]\/[0-3][0-9]\/\d+"
    with open(f"{filename_without_extension(path)}-page-1-table-1.csv", encoding='utf8') as file:
        first_line = file.readline().strip()
        second_line = file.readline().strip()
        #breakpoint()
        m = re.search(pattern, second_line)
        period = m.group()
        month = m.group(1)
        year = m.group(2)
        return (period, month, year)


if __name__ == "__main__":
    path = "test.pdf"
    create_csv(path)
    get_period(path)