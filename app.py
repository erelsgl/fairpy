import gspread
import numpy as np
from flask import Flask, request, render_template
import pandas as pd
from fairpy import Allocation, AllocationMatrix, ValuationMatrix
from envy_free_approximation_division import envy_free_approximation_division
# from gspread_utils import get_worksheet_by_list_of_possible_names
app = Flask(__name__)


@app.route('/')
def root():
    return render_template('home_page.html')


@app.route('/first_algo')
def upload_file1():
    return render_template(f'upload_sheets_algo1.html')


@app.route('/second_algo')
def upload_file2():
    return render_template(f'upload_sheets_algo2.html')


@app.route('/proceed')
def move_to_calculate_algo1():
    url = request.args.get('url')
    return render_template(f'calculate_algo1.html', url=url)


@app.route('/proceed2')
def move_to_calculate_algo2():
    url = request.args.get('url')
    eps = request.args.get('eps')
    return render_template(f'calculate_algo2.html', url=url, eps=eps)


def run_algo1(url: str):
    from envy_freeness_and_equitability_with_payments import envy_freeness_and_equitability_with_payments
    account = gspread.service_account("credentials.json")
    spreadsheet = account.open_by_url(url)
    sheet1 = spreadsheet.worksheet('input')

    # sheet1 = spreadsheet.get_worksheet(0)

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


def output_sheets_algo1(url: str, result):
    account = gspread.service_account("credentials.json")
    spreadsheet = account.open_by_url(url)
    sheet1 = spreadsheet.worksheet('input')
    all_agent = sheet1.col_values(1)[1:]
    size_all_agents = len(all_agent)
    worksheet_names = [ws.title for ws in spreadsheet.worksheets()]
    if "output" in worksheet_names:
        output_sheet = spreadsheet.worksheet("output")
    else:
        output_sheet = spreadsheet.add_worksheet(title="output", rows=sheet1.row_count, cols=sheet1.col_count)
    output_sheet.update_acell("A1", "שם הסוכן")
    output_sheet.update_acell("B1", "חבילות")
    output_sheet.update_acell("C1", "תשלום")
    for i in range(size_all_agents):
        output_sheet.update_acell(f"A{i + 2}", all_agent[i])
    all_bundles = list(result["allocation"].values())
    for i in range(len(all_bundles)):
        output_sheet.update_acell(f"B{i+2}", "".join(all_bundles[i]))
    all_payments = list(result["payments"].values())
    for i in range(len(all_payments)):
        output_sheet.update_acell(f"C{i + 2}", all_payments[i])
    return output_sheet.url

@app.route('/play_algo1')
def run_the_algo1():
    url = request.args.get('url')
    result = run_algo1(url=url)
    print("Run complete")
    output = output_sheets_algo1(url, result)
    return render_template(f'answer.html', url=output, result=result)


def run_algo2(url: str, eps: float):
    account = gspread.service_account("credentials.json")
    spreadsheet = account.open_by_url(url)
    sheet1 = spreadsheet.get_worksheet(0)
    df = pd.DataFrame(sheet1.get_all_records())
    df = df.set_index(df.columns[0]).to_numpy()
    allo = Allocation(agents=ValuationMatrix(df), bundles=AllocationMatrix(np.eye(len(df), len(df)).astype('int')))
    return envy_free_approximation_division(allo,eps)


@app.route('/play_algo2')
def run_the_algo2():
    url = request.args.get('url')
    eps = float(request.args.get('eps'))
    result = run_algo2(url, eps)
    # output = output_sheets_algo1(url, result)
    # ---need insert the 'output' to 'url' in next line----
    return render_template(f'answer.html', url=url, result=result)


def get_worksheet_by_list_of_possible_names(spreadsheet:gspread.Spreadsheet, possible_names:list)->gspread.Worksheet:
	"""
	Searches the given spreadsheet for a worksheet with a name from the given list.
	If none is found, return None.
	"""
	worksheet_names = [ws.title for ws in spreadsheet.worksheets()]
	for name in possible_names:
		if name in worksheet_names:
			return spreadsheet.worksheet(name)
	return None



def worksheet(spreadsheet:gspread.Spreadsheet)->gspread.Worksheet:
    output_sheet = get_worksheet_by_list_of_possible_names(spreadsheet, "input")
    print(type(output_sheet))
    return output_sheet


if __name__ == "__main__":
    app.run(debug=True)
    # account = gspread.service_account("credentials.json")
    # spreadsheet = account.open_by_url()
    # print(worksheet(spreadsheet))
    # app.run(debug=True, host="0.0.0.0", port=5200)

# rendering the HTML page which has the button
# @app.route('/log')
# def log():
#     with open("app.log") as logfile:
#         logtext = logfile.read()
#     return Response(logtext, mimetype='text/plain')
#
# @app.route('/background_process_test')
# def background_process_test():
#     print ("Hello")
#     return "Test complete"
