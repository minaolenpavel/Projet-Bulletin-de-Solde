import camelot.io as camelot
import os, re

def get_filename_without_extension(path:str) -> str:
    return os.path.splitext(os.path.basename(path))[0]

def create_csv(path:str) -> None:
    data = camelot.read_pdf(path)
    export_path = get_filename_without_extension(path) + ".csv"
    data.export(export_path, f = "csv", compress=False)

def get_month(path:str)-> tuple:
    pattern = r"[0-3][0-9]\/([0-3][0-9])\/\d+ au [0-3][0-9]\/[0-3][0-9]\/\d+"
    with open(f"{get_filename_without_extension(path)}-page-1-table-1.csv", encoding='utf8') as file:
        first_line = file.readline().strip()
        second_line = file.readline().strip()
        #breakpoint()
        m = re.search(pattern, second_line)
        period = m.group()
        month = m.group(1)
        return (month, period)


if __name__ == "__main__":
    path = "test.pdf"
    create_csv(path)
    get_month(path)