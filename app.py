import gspread
from flask import Flask, request, render_template, redirect, url_for

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
    sheet1 = spreadsheet.worksheet("טבלת הערכות")

    sheet1 = spreadsheet.get_worksheet(0)

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


@app.route('/play_algo1')
def run_the_algo1():
    url = request.args.get('url')
    result = run_algo1(url=url)
    print("Run complete")
    return render_template(f'answer.html', result=result)


def run_algo2(url: str, eps: float):
    # ---fill in the implement for algo2----
    pass


@app.route('/play_algo2')
def run_the_algo2():
    url = request.args.get('url')
    eps = float(request.args.get('eps'))
    print("this is algo2")
    result = run_algo2(url, eps)
    return render_template(f'answer.html', result=result)


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