import re, utils

pattern = r'([0-3][0-9]/[0-3][0-9]/[0-9]*)'

desc = []
start_dates = []
with open("test3.csv", mode="r", encoding='utf-8') as file:
    ok = False
    detected_date = False
    for l in file:
        if l.strip() == "Solde de base mensuelle":
            ok = True
        elif re.match(pattern, l):
            ok = False
            detected_date = True

        if ok :
            desc.append(l.strip())
            date_desc = re.search(pattern, l)
            if date_desc:
                date = date_desc.group(1)
                start_dates.append(date)
                #breakpoint()
        elif detected_date : 
            date = re.match(pattern, l)
            if date :
                if len(l.strip()) > 10 and " " not in l:
                    #breakpoint()
                    ok_date = l.replace('"', "").strip().split(",")
                    start_dates.extend(ok_date)
                else:
                    ok_date = date.group(1)
                    start_dates.append(ok_date.replace(" ", ""))

final_dates = [d for d in start_dates if re.match(pattern, d) ]
breakpoint()
print()



# What's done in here is parsing of the messy csv files
# I noticed there was some sort of "logic" if we can call it this way
# The lines that interest me are the periods
# But it's very difficult to understand what is what
# Unless there is a logic in this
# In that case there is always x*2 more dates than description such as "solde mensuelle"
# From this we just have to put in a list all descriptions and all dates
# Then we're sure that the period that matches the description is always periods[posInDescList + len(periods)/2]