from gspread import Spreadsheet
import pandas as pd
from fairpy import Allocation, AllocationMatrix, ValuationMatrix
import gspread
import numpy as np
from envy_free_approximation_division import envy_free_approximation_division


def run_algo1(url: str):
    from envy_freeness_and_equitability_with_payments import envy_freeness_and_equitability_with_payments
    account = gspread.service_account("credentials.json")
    spreadsheet = account.open_by_url(url)
    sheet1 = spreadsheet.worksheet('input')

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
    return res, spreadsheet


def create_output_layer(spreadsheet: Spreadsheet):
    sheet1 = spreadsheet.get_worksheet(0)
    worksheet_names = [ws.title for ws in spreadsheet.worksheets()]
    if "output" in worksheet_names:
        output_sheet = spreadsheet.worksheet("output")
    else:
        output_sheet = spreadsheet.add_worksheet(title="output", rows=sheet1.row_count, cols=sheet1.col_count)
    output_sheet.update_acell("A1", "שם הסוכן")
    output_sheet.update_acell("B1", "חבילות")
    output_sheet.update_acell("C1", "תשלום")
    return output_sheet


def output_sheets_algo1(result, spreadsheet):
    output_sheet = create_output_layer(spreadsheet)
    sheet1 = spreadsheet.get_worksheet(0)
    all_agent = sheet1.col_values(1)[1:]
    size_all_agents = len(all_agent)
    for i in range(size_all_agents):
        output_sheet.update_acell(f"A{i + 2}", all_agent[i])
    all_bundles = list(result["allocation"].values())
    for i in range(len(all_bundles)):
        output_sheet.update_acell(f"B{i + 2}", "".join(all_bundles[i]))
    all_payments = list(result["payments"].values())
    for i in range(len(all_payments)):
        output_sheet.update_acell(f"C{i + 2}", all_payments[i])
    return output_sheet.url

def run_algo2(url: str, eps: float):
    account = gspread.service_account("credentials.json")
    spreadsheet = account.open_by_url(url)
    sheet1 = spreadsheet.get_worksheet(0)
    df = pd.DataFrame(sheet1.get_all_records())
    df = df.set_index(df.columns[0]).to_numpy()
    allo = Allocation(agents=ValuationMatrix(df), bundles=AllocationMatrix(np.eye(len(df), len(df)).astype('int')))
    return envy_free_approximation_division(allo, eps), spreadsheet


def output_sheets_algo2(result: dict, spreadsheet: Spreadsheet):
    output_sheet = create_output_layer(spreadsheet)
    sheet1 = spreadsheet.get_worksheet(0)
    all_agent = sheet1.col_values(1)[1:]
    all_bundles = sheet1.row_values(1)[1:]
    size_all_agents = len(all_agent)

    for i in range(size_all_agents):
        output_sheet.update_acell(f"A{i + 2}", all_agent[i])
    for i in range(size_all_agents):
        if result["allocation"][i]:
            output_sheet.update_acell(f"B{i + 2}", all_bundles[result["allocation"][i][0]])
        else:
            output_sheet.update_acell(f"B{i + 2}", None)
    all_payments = result["payments"]
    for i in range(len(all_payments)):
        output_sheet.update_acell(f"C{i + 2}", all_payments[i])
    return output_sheet.url
# if __name__=="__main__":
#     run()
