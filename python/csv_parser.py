from utils import *
import camelot.io as camelot
import gc

def parse_pdf_to_csv(path:str, export_folder:str) -> None:
    '''
    Takes the path of a PDF and gives out one or several CSV tables out of it
    '''
    data = camelot.read_pdf(path, pages='all') # Important to set, otherwise 2 page long pdfs are ignored
    export_path = add_backslash(export_folder) + filename_without_extension(path) + ".csv"
    data.export(export_path, f = "csv", compress=False)
    # Ensures the files are not still opened and used
    del data
    gc.collect()
    return export_folder