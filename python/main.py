#from imap_solde_retriever import *
from pdf_extract import *
from models import *
from utils import *
import json

if __name__ == "__main__":
    path = "test2.pdf"
    period = get_period(path)
    amount = get_amount(path)
    bulletin = SoldeMois(amount, period[0], period[1], period[2], path)
    print(bulletin)
    data = json_serialize(bulletin)
    write_json(path, data)

