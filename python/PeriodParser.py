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
    def __init__(self, folder:str, debug = False):
        self.folder = folder
        self.debug = debug

    # Could do the same func for years but it never happened so...
    def fix_months_mismatch(self, start, end) -> tuple:
        last_day = utils.last_month_date(start)
        period1 = ActivityPeriod()
        period1.start_date = start
        period1.end_date = datetime.datetime(start.year, start.month, last_day)
        period1.calc_days()

        period2 = ActivityPeriod()
        period2.start_date = datetime.datetime(end.year, end.month, 1)
        period2.end_date = end
        period2.calc_days()
        
        return (period1, period2)


    def extract_periods_data(self, filename) -> tuple:
        path = utils.filename_without_extension(filename)
        pattern = r'([0-3][0-9]/[0-3][0-9]/[0-9]*)'
        headers = []
        dates = []
        if self.debug:
            path = filename
        else:
            path = f"{self.folder}/{path}-page-1-table-2.csv"
        with open(path, mode="r", encoding='utf-8') as file:
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

    def create_periods(self, filename:str) -> list:
        dates, headers = self.extract_periods_data(filename)
        periods = []
        for i, element in enumerate(headers):
            if element.strip() == "Solde de base mensuelle":
                new_period = ActivityPeriod()
                start = utils.str_to_datetime(dates[i])
                end = utils.str_to_datetime(dates[i + (len(dates)//2)])
                if start == end:
                    if len(headers)%2 == 0:
                        end = utils.str_to_datetime(dates[i+1])
                    else:
                        pass
                if start.month != end.month:
                    fixed_periods = self.fix_months_mismatch(start, end)
                    periods.extend(fixed_periods)
                else:
                    new_period.start_date = start
                    new_period.end_date = end
                    new_period.calc_days()
                    periods.append(new_period)
        return periods
    
    def parse_folder(self) -> list:
        parsed_periods = []
        filenames = utils.list_files("bulletins_solde_pdf")
        for file in filenames:
            periods = self.create_periods(file)
            parsed_periods.extend(periods)
        return parsed_periods

if __name__ == "__main__":
    csv_folder = "bulletins_solde_csv"
    parser = PeriodParser(csv_folder, False)
    #periods = parser.create_periods("juin2.csv")
    #print(periods)
    all_periods = parser.parse_folder()
    all_days = 0
    for p in all_periods:
        all_days+=p.days_count
        print(p, p.days_count)
    print(all_days)
