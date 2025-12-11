import re, utils, datetime
from Models import ActivityPeriod

class PeriodParser:
    """
    This module parses irregular CSV files containing datetime data.  
    The structure of these files follows an implicit pattern: for every
    descriptive entry (e.g., "solde mensuelle"), there are always twice
    as many date entries (start date - end date).

    To reliably extract periods, we first collect all descriptions and all
    dates into separate lists. Because of the consistent 2:1 ratio, the
    period associated with a given description can be retrieved using:

        periods[index_in_description_list + len(periods) // 2]

    This logic allows us to reconstruct the mapping between descriptions
    and their corresponding date periods, despite the inconsistent CSV
    format.
    """
    def __init__(self, filename:str, folder:str):
        self.filename = utils.filename_without_extension(filename)
        self.folder = folder

    # Could do the same func for years but it never happened so...
    def fix_months_mismatch(self, start, end) -> tuple:
        last_day = utils.last_month_date(start)
        period1 = ActivityPeriod()
        period1.start_date = start
        period1.end_date = datetime.datetime(start.year, start.month, last_day)

        period2 = ActivityPeriod()
        period2.start_date = datetime.datetime(end.year, end.month, 1)
        period2.end_date = end
        return (period1, period2)


    def extract_periods_data(self) -> tuple:
        path = self.filename
        pattern = r'([0-3][0-9]/[0-3][0-9]/[0-9]*)'
        headers = []
        dates = []
        with open(f"{self.folder}/{path}-page-1-table-2.csv", mode="r", encoding='utf-8') as file:
            detected_header = False
            detected_date = False
            for l in file:
                # When the trigger word is detected it starts to register these entries
                # In the logic of the file each header has two periods associated
                if l.strip() == "Solde de base mensuelle":
                    detected_header = True
                # When we stop detecting headers and we start detecting dates we start registering them too
                elif re.match(pattern, l):
                    detected_header = False
                    detected_date = True
                if detected_header :
                    headers.append(l.strip())
                    date_desc = re.search(pattern, l)
                    # It does happen we have dates within the line of a header it's important to keep it
                    if date_desc:
                        date = date_desc.group(1)
                        dates.append(date)
                elif detected_date : 
                    date = re.match(pattern, l)
                    if date :
                        # Sometimes we can also find two dates on the same line we have to keep them both
                        if len(l.strip()) > 10 and " " not in l:
                            ok_date = l.replace('"', "").strip().split(",")
                            dates.extend(ok_date)
                        else:
                            # But in the general case it's one line = one date
                            ok_date = date.group(1)
                            dates.append(ok_date.replace(" ", ""))
        # Some noise is left even after parsing
        final_dates = [d for d in dates if re.match(pattern, d)]
        return (final_dates, headers)

    def create_periods(self) -> list:
        dates, headers = self.extract_periods_data()

        index_solde_mensuelle = []
        for i, element in enumerate(headers):
            if element.strip() == "Solde de base mensuelle":
                index_solde_mensuelle.append(i)

        periods = []
        for i in index_solde_mensuelle:
            period = ActivityPeriod()
            start = dates[i]
            end_index = int(i + len(dates)/2)
            end = dates[end_index]

            start_date = utils.str_to_datetime(start)
            end_date = utils.str_to_datetime(end)

            if start_date.month != end_date.month:
                fixed_periods = self.fix_months_mismatch(start_date, end_date)
                for p in fixed_periods:
                    p.calc_days()
                periods.append(fixed_periods[0])
                periods.append(fixed_periods[1])
            else:
                period.start_date = start
                period.end_date = end
                period.calc_days()
                periods.append(period)
        return periods

if __name__ == "__main__":
    csv_folder = "bulletins_solde_csv"
    filenames = utils.list_files("bulletins_solde_pdf")
    all_periods = []
    for file in filenames:
        parser = PeriodParser(file, csv_folder)
        periods = parser.create_periods()
        all_periods.extend(periods)
    all_days = 0
    for p in all_periods:
        all_days+=p.days_count
        print(p, p.days_count)
    print(all_days)

# What's done in here is parsing of the messy csv files
# I noticed there was some sort of "logic" if we can call it this way
# The lines that interest me are the periods
# But it's very difficult to understand what is what
# Unless there is a logic in this
# In that case there is always x*2 more dates than description such as "solde mensuelle"
# From this we just have to put in a list all descriptions and all dates
# Then we're sure that the period that matches the description is always periods[posInDescList + len(periods)/2]