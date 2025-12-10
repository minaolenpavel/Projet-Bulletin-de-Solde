import re, utils
from Models import ActivityPeriod

pattern = r'([0-3][0-9]/[0-3][0-9]/[0-9]*)'

headers = []
dates = []
with open("test2.csv", mode="r", encoding='utf-8') as file:
    detected_header = False
    detected_date = False
    for l in file:
        if l.strip() == "Solde de base mensuelle":
            detected_header = True
        elif re.match(pattern, l):
            detected_header = False
            detected_date = True
        if detected_header :
            headers.append(l.strip())
            date_desc = re.search(pattern, l)
            if date_desc:
                date = date_desc.group(1)
                dates.append(date)
        elif detected_date : 
            date = re.match(pattern, l)
            if date :
                if len(l.strip()) > 10 and " " not in l:
                    ok_date = l.replace('"', "").strip().split(",")
                    dates.extend(ok_date)
                else:
                    ok_date = date.group(1)
                    dates.append(ok_date.replace(" ", ""))

# Some noise is left even after parsing
final_dates = [d for d in dates if re.match(pattern, d) ]


index_solde_mensuelle = []
for i, element in enumerate(headers):
    if element.strip() == "Solde de base mensuelle":
        index_solde_mensuelle.append(i)

periods = []
for i in index_solde_mensuelle:
    period = ActivityPeriod()
    start = final_dates[i]
    end_index = int(i + len(final_dates)/2)
    end = final_dates[end_index]
    period.start_date = start
    period.end_date = end
    period.calc_days()
    periods.append(period)





# What's done in here is parsing of the messy csv files
# I noticed there was some sort of "logic" if we can call it this way
# The lines that interest me are the periods
# But it's very difficult to understand what is what
# Unless there is a logic in this
# In that case there is always x*2 more dates than description such as "solde mensuelle"
# From this we just have to put in a list all descriptions and all dates
# Then we're sure that the period that matches the description is always periods[posInDescList + len(periods)/2]