import os, json, time, datetime, calendar

class Stopwatch:
    def __init__(self):
        self._start_time = None
        self._end_time = None

    def start(self):
        self._start_time = time.time()
    
    def stop(self):
        self._end_time = time.time()

    @property
    def total_time(self):
        return self._end_time - self._start_time


def filename_without_extension(path:str) -> str:
    '''
    Give the name of a file without its extension
    \n Exemple : test.pdf -> test
    '''
    return os.path.splitext(os.path.basename(path))[0]

def month_name_from_number(month_num:int) -> str: # Is prob obsolete idk will keep it for now
    month_dict = {
                1 : "janvier",
                2 : "février",
                3 : "mars",
                4 : "avril",
                5 : "mai", 
                6 : "juin",
                7 : "juillet",
                8 : "août",
                9 : "septembre",
                10 : "octobre",
                11 : "novembre",
                12 : "décembre"}
    return month_dict[month_num]

def is_valid_json(data:str) -> bool:
    try:
        json_object = json.loads(data)
        return True
    except:
        return False

def write_json(filename:str, data:str, folder_path:str):
    if not is_valid_json(data):
        print("data is not json")
    else:
        json_path = add_backslash(folder_path) + filename_without_extension(filename) + ".json"
        with open(json_path, "w", encoding='utf8') as json_file:
            json_file.write(data)

def json_serialize_bulletin(bulletin) -> str:
    data = json.dumps(bulletin.__dict__, ensure_ascii=False, indent=4)
    return data

def json_serialize_list(liste:list) -> str:
    data = json.dumps(liste, ensure_ascii=False, indent=4)
    return data

def add_backslash(folder_path:str):
    if folder_path[-1] == "/":
        return folder_path
    else:
        return folder_path + "/"
    
def list_files(folder_path:str) -> list:
    folder = add_backslash(folder_path)
    dir_list = os.listdir(folder)
    return [add_backslash(folder) + b for b in dir_list]

def datetime_format() -> str: # is useless
    return "%a, %d %b %Y %H:%M:%S %z"

def str_to_datetime(string):
    return datetime.datetime.strptime(string, "%d/%m/%Y")

def last_month_date(date:datetime.datetime):
    return calendar.monthrange(date.year, date.month)[1]