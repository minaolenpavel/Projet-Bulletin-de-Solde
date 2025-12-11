from Models import ActivityPeriod, MonthActivity
from PeriodParser import *

months = []

def month_exist(p) -> int:
    y = p.start_date.year
    m = p.start_date.month
    for i, month in enumerate(months):
        if month.month == m and month.year == y:
            return i
    else:
        return None


csv_folder = "bulletins_solde_csv"
filenames = utils.list_files("bulletins_solde_pdf")
all_periods = []
for file in filenames:
    parser = PeriodParser(file, csv_folder)
    periods = parser.create_periods()
    all_periods.extend(periods)

for p in all_periods:
    if month_exist(p):
        i = month_exist(p)
        months[i].periods.append(p)
    else:
        month = MonthActivity(p.start_date.year, p.start_date.month)
        month.periods.append(p)
        months.append(month)

total = 0
for m in months:
    total += m.CalcDaysCount()
    print(m.CalcDaysCount(), m)
    #print(m.days_count)

print(total)







