#from imap_solde_retriever import *
from pdf_extract import *
from models import *
import json

if __name__ == "__main__":
    path = "test.pdf"
    period = get_period(path)
    amount = get_amount(path)
    bulletin = SoldeMois(amount, period[0], period[1], period[2], path)
    print(bulletin)
    res = json.dumps(bulletin.__dict__, ensure_ascii=False)
    print(res)

