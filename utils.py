import os

def filename_without_extension(path:str) -> str:
    '''
    Give the name of a file without its extension
    \n Exemple : test.pdf -> test
    '''
    return os.path.splitext(os.path.basename(path))[0]

def month_name_from_number(month_num:int):
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