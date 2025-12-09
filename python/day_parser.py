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
for dt in datetime_list:
    print(dt)


periods = []

print(len(datetime_list))

test = len([x for x in datetime_list if len(x)%2])
print(test)

periods = []  # list of existing ActivityPeriod objects

for sublist in datetime_list:
    # iterate two by two
    for i in range(0, len(sublist) - 1, 2):
        start = sublist[i]
        end = sublist[i+1]

        # skip if start or end is already in an existing period
        if already_exist(start, periods) or already_exist(end, periods):
            continue

        # create new period
        period = ActivityPeriod()
        period.start_date = start
        period.end_date = end
        periods.append(period)
    
    # handle leftover if odd-length
    if len(sublist) % 2 == 1:
        leftover = sublist[-1]
        if not already_exist(leftover, periods):
            period = ActivityPeriod()
            period.start_date = leftover
            period.end_date = leftover
            periods.append(period)

for p in sorted(periods):
    print(p)

print(len(periods))

exit()

for p in datetime_list:
    if len(p) != 2:
        period = ActivityPeriod()
        for date in p:
            if already_exist(date, periods):
                pass
            else:
                if period.start_date is None:
                    period.start_date = date
                else:
                    period.end_date = date
                #breakpoint()
        if period.end_date is None:
            period.end_date = period.start_date
        periods.append(period)
    elif len(p) == 2:
        if p[0].month != p[1].month:
            # Will create a datetime object for the first day of the month and the last day of the month
            # This way we can have properly cut months even if the activity period is throughout two months
            last_day = utils.last_month_date(p[0])
            end_date = datetime(p[0].year, p[0].month, last_day)
            
            period1 = ActivityPeriod()
            period1.start_date = p[0]
            period1.end_date = end_date

            start_date = datetime(p[1].year, p[1].month, 1)
            period2 = ActivityPeriod()
            period2.start_date = start_date
            period2.end_date = p[1]

            periods.append(period1)
            periods.append(period2)





for p in periods:
    print(p)