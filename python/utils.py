import os, json

def filename_without_extension(path:str) -> str:
    '''
    Give the name of a file without its extension
    \n Exemple : test.pdf -> test
    '''
    return os.path.splitext(os.path.basename(path))[0]

def month_name_from_number(month_num:int) -> str:
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

def write_json(filename:str, data:str, folder_path:str = "./bulletins_solde_json"):
    if not is_valid_json(data):
        print("data is not json")
    else:
        json_path = add_backslash(folder_path) + filename_without_extension(filename) + ".json"
        with open(json_path, "w", encoding='utf8') as json_file:
            json_file.write(data)

def json_serialize(bulletin) -> str:
    data = json.dumps(bulletin.__dict__, ensure_ascii=False, indent=4)
    return data

def add_backslash(folder_path:str):
    if folder_path[-1] == "/":
        return folder_path
    else:
        return folder_path + "/"
    
def list_files(folder_path:str) -> list:
    dir_list = os.listdir(folder_path)
    return [add_backslash(folder_path) + b for b in dir_list]