import csv
import json
from flask import render_template
from flask_organize import app
from fairpy.goods_chores import *



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
    file_contents = file.read().decode('utf-8')
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
        print(items.keys())
    except:
        return False
    for a in range(1, len(data)):
        agent = data[a]
        try:
            name = agent[0]
            evaluations = json.loads(agent[1])
            # validate the length of the items list
            if len(evaluations) != len(items):
                return False
            # validate the items names is string , and validate that the items equals to the items list
            for i in evaluations.keys():
                if type(i) != str or i not in items:
                    return False
            # validate the evaluations is a numeric value
            for i in evaluations.values():
                if type(i) != float and type(i) != int:
                    return False
            agents[name] = evaluations
        except:
            return False
    return AgentList(agents)


def perform_calculation(data, algorithm):
    result = None
    # validate correct structure of the input and parse it to AgentList
    try:
        inp = validate_input(data)
        if algorithm == 'algorithm1':
            if inp:
                result = Double_RoundRobin_Algorithm(inp)
            else:
                result =  'Error - Invalid Input'
        elif algorithm == 'algorithm2':
            inp = validate_input(data)
            if inp and len(inp) == 2:
                result = Generalized_Adjusted_Winner_Algorithm(inp)
            else:
                result =  'Error - Invalid Input'
        elif algorithm == 'algorithm3':
            inp = validate_input(data)
            if inp:
                result = Generalized_Moving_knife_Algorithm(inp, list(inp[0].all_items()))
            else:
                result =  'Error - Invalid Input'
    except:
        result = 'Error - Invalid Input'
    return result
