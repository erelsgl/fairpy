from flask import Flask, request, render_template
import algorithm

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


@app.route('/play_algo1')
def run_the_algo1():
    url = request.args.get('url')
    result, spreadsheet = algorithm.run_algo1(url=url)
    print("Run complete")
    output = algorithm.output_sheets_algo1(result, spreadsheet)
    return render_template(f'answer.html', url=output, result=result, num_algo=1)


@app.route('/play_algo2')
def run_the_algo2():
    url = request.args.get('url')
    eps = float(request.args.get('eps'))
    result, spreadsheet = algorithm.run_algo2(url, eps)
    print("Run complete")
    output = algorithm.output_sheets_algo2(result, spreadsheet)
    return render_template(f'answer.html', url=output, result=result, num_algo=2)


@app.route('/previous_page')
def upload_file_prev():
    num = request.args.get('algo')
    if num == '1':
        return render_template(f'upload_sheets_algo1.html')
    else:
        return render_template(f'upload_sheets_algo2.html')


@app.route('/back_home_page')
def back_home():
    return render_template(f'home_page.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5200)

