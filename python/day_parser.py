import re, utils
from datetime import datetime
from models import ActivityPeriod

def is_between(date:datetime, start_date:datetime, end_date:datetime):
    if start_date <= date <= end_date:
        return True
    else:
        return False

def already_exist(date:datetime, periods:list):
    for period in periods:
        if is_between(date, period.start_date, period.end_date):
            return True
    else:
        return False

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
    with open(f"{utils.add_backslash('bulletins_solde_csv')}{utils.filename_without_extension(file)}-page-1-table-2.csv", mode = "r", encoding='utf8') as file:
        sub_data = []
        for l in file:
            m = re.match(pattern, l)
            if m and l!="":
                sub_data.append(m.group(1).strip())
        if sub_data is not None:
            data.append(list(set(sub_data)))

datetime_list = sorted([sorted(list(map(utils.str_to_datetime, x))) for x in data])



periods = []

print(len(datetime_list))

test = len([x for x in datetime_list if len(x)%2])
print(test)

periods = []  # list of existing ActivityPeriod objects

for sublist in datetime_list:
    i = 0
    while i < len(sublist):
        period = ActivityPeriod()
        period.start_date = sublist[i]
        if i+1 < len(sublist):
            period.end_date = sublist[i+1]
        else:
            # single leftover: use the same date as end
            period.end_date = sublist[i]
        if not period_already_exists(period, periods):
            periods.append(period)
        i += 2

        
print(len(periods))
for p in sorted(periods):
    print(p)



