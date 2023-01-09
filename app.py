import gspread
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('home_page.html')


@app.route('/first_algo')
def upload_file():
    return render_template(f'upload_sheets.html')

@app.route('/proceed')
def move_to_calculate():
    url = request.args.get('url')
    # error = None
    # try:
    #     import gspread
    #     account = gspread.service_account("credentials.json")
    #     spreadsheet = account.open_by_url(url)
    # except gspread.exceptions.APIError:
    #     error = "Google Spreadsheet API error! Please verify that you shared your spreadsheet with the above address."
    # except gspread.exceptions.NoValidUrlKeyFound:
    #     error = "Google Spreadsheet could not find a key in your URL! Please check that the URL you entered points to a valid spreadsheet."
    # except gspread.exceptions.SpreadsheetNotFound:
    #     error = "Google Spreadsheet could not find the spreadsheet you entered! Please check that the URL points to a valid spreadsheet."
    # except Exception as e:
    #     error = type(e).__name__ + "! Please check your URL and try again."
    # if error is not None:
    #     print("error=", error)
    #     return render_template(f'upload_sheets.html', error=error)
    # else:
    return render_template(f'move_to_calculate.html', url=url)


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


# @app.route('/run_the_algorithm')
@app.route('/run')
def run_the_algorithm(url: str):
    # import run
    # url = request.args.get('url')
    # print(url)
    run_algo(url=url)
    print("Run complete")
    return render_template(f'try.html')


if __name__ == "__main__":
    app.run(debug=True)












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