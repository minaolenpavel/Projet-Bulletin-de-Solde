import camelot.io as camelot
import os, re

def get_filename_without_extension(path:str) -> str:
    return os.path.splitext(os.path.basename(path))[0]

def create_csv(path:str) -> None:
    data = camelot.read_pdf(path)
    export_path = get_filename_without_extension(path) + ".csv"
    data.export(export_path, f = "csv", compress=False)

def get_month(path:str)-> None:
    pattern = r'^Période du \d{2}/\d{2}/\d{4} au \d{2}/\d{2}/\d{4}$'
    with open(f"{get_filename_without_extension(path)}-page-1-table-1.csv", encoding='utf8') as file:
        for line in file:
            if re.match(pattern, line):
                print(line.strip())
                break


if __name__ == "__main__":
    path = "test.pdf"
    create_csv(path)
    get_month(path)