import gspread
from flask import render_template


def run_algo(url: str):
    from envy_freeness_and_equitability_with_payments import envy_freeness_and_equitability_with_payments
    account = gspread.service_account("credentials.json")
    spreadsheet = account.open_by_url(url)
    sheet1 = spreadsheet.worksheet("טבלת הערכות")

    # Open sheet by index:
    sheet1 = spreadsheet.get_worksheet(0)  # Same as above

    list_of_dicts = sheet1.get_all_records()
    mydict = {}
    for dict in list_of_dicts:
        key = dict.pop("name")
        value = dict
        mydict[key] = value
    val = sheet1.get_all_values()
    bundles = [item for item in val[0][1:] if len(item) == 1]
    agents = [item for item in sheet1.col_values(1) if item][1:]

    allo = {}
    for agent in agents:
        allo[agent] = []
    while bundles:
        for agent in agents:
            if bundles:
                allo[agent].append(bundles.pop(0))
    res = envy_freeness_and_equitability_with_payments(mydict, allo)
    print(res)
    return res


# if __name__=="__main__":
#     run()
