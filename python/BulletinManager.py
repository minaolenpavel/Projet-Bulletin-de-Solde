import utils, os, json
from MailRetriever import MailRetriever
from models import Bulletin


class BulletinManager:
    def __init__(self, csv_folder:str, pdf_folder:str, export_path:str, export_filename:str):
        self.export_filename = export_filename
        self.export_path = export_path
        self.csv_folder = csv_folder
        self.pdf_folder = pdf_folder
        self.pdf_filenames = utils.list_files(pdf_folder)
        self.bulletins = []
    
    def create_bulletin(self, amount:float, period:tuple, pdf_path:str) -> Bulletin:
        bulletin = Bulletin(amount, period[0], period[1], os.path.abspath(pdf_path))
        self.bulletins.append(bulletin)

    def export_bulletins_json(self):
        json_list = [b.to_dict() for b in self.bulletins]
        json_str = json.dumps(json_list, indent=2, ensure_ascii=False)
        filename = self.export_filename
        export_path = self.export_path
        utils.write_json(filename, json_str, export_path)

