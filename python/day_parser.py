import re, utils
from datetime import datetime
from Models import ActivityPeriod

def period_already_exists(new_period, periods):
    """
    Check if new_period is fully contained in any period in periods list.
    new_period: ActivityPeriod
    periods: list of ActivityPeriod
    Returns True if contained, False otherwise
    """
    for period in periods:
        if period.start_date <= new_period.start_date and new_period.end_date <= period.end_date:
            return True
    return False



pattern = r'([0-3][0-9]/[0-3][0-9]/[0-9]*)'
data = []

all_filenames = utils.list_files("bulletins_solde_pdf")
for file in all_filenames:
    breakpoint()
    with open(f"{utils.add_backslash('bulletins_solde_csv')}{utils.filename_without_extension(file)}-page-1-table-2.csv", mode = "r", encoding='utf8') as file:
        sub_data = []
        for l in file:
            m = re.match(pattern, l)
            if m and l!="":
                sub_data.append(m.group(1).strip())
        if sub_data is not None:
            data.append(list(set(sub_data)))

datetime_list = sorted([sorted(list(map(utils.str_to_datetime, x))) for x in data])

