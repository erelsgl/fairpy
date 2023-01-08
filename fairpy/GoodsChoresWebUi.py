import csv
import json

from flask import Flask, request, render_template
from goods_chores import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/algorithm1')
def algorithm1():
    return render_template('algorithm1.html')


@app.route('/algorithm2')
def algorithm2():
    return render_template('algorithm2.html')


@app.route('/algorithm3')
def algorithm3():
    return render_template('algorithm3.html')


@app.route('/results', methods=['POST'])
def results():
    # Get the form data from the request
    form_data = request.form
    algorithm = form_data.get('algorithm')
    # Get the file from the request
    file = request.files['input_file']

    # Read the contents of the file
    file_contents = file.read().decode('utf-8')

    # Convert the contents of the file to a list of rows
    reader = csv.reader(file_contents.splitlines())
    rows = list(reader)
    print(rows)
    # Perform the calculation using the rows and the desired algorithm
    result = perform_calculation(rows, algorithm)

    # Render the results template, passing the result as a variable
    return render_template('results.html', result=result)


def validate_input(data):
    agents = {}
    try:
        items = json.loads(data[1][1])
    except:
        return False
    for a in range(1, len(data)):
        agent = data[a]
        try:
            name = agent[0]
            evaluations = json.loads(agent[1])
            if len(evaluations) != len(items):
                return False
            for i in evaluations.keys():
                if type(i) != str:
                    return False
            for i in evaluations.values():
                if type(i) != float and type(i) != int:
                    return False
            agents[name] = evaluations
        except:
            return False
    print(AgentList(agents))
    return AgentList(agents)


def perform_calculation(data, algorithm):
    result = None
    # validate correct structure of the input and parse it to AgentList
    inp = validate_input(data)
    if algorithm == 'algorithm1':
        if inp:
            result = Double_RoundRobin_Algorithm(inp)
        else:
            raise 'Invalid Input'
    elif algorithm == 'algorithm2':
        inp = validate_input(data)
        if inp:
            result = Generalized_Adjusted_Winner_Algorithm(inp)
    elif algorithm == 'algorithm3':
        inp = validate_input(data)
        if inp:
            result = Generalized_Moving_knife_Algorithm(inp, list(inp[0].all_items()))
    else:
        raise ValueError('Invalid algorithm')
    return result


if __name__ == '__main__':
    app.run(debug=True)
