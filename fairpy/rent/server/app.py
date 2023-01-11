# app.py
from flask import Flask, request, render_template, redirect, jsonify, url_for, flash
from fairpy.rent.Algorithms import optimal_envy_free
from fairpy.agentlist import AgentList
import ast

app = Flask(__name__)
total_rent = 0
num_room = 0


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        rooms = request.form.get('rooms')
        rent = request.form.get('rent')

        if not rooms or not rent:
            flash('Please fill in the required fields')
            return redirect('/')
        else:
            # form is filled, do something
            pass

    return render_template('index.html')


@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST' and request.form["rooms"] != '' and request.form["rent"] != '':
        rooms_input = int(request.form["rooms"])
        rent_input = int(request.form["rent"])
        return redirect(url_for("new_page", user_input=[rooms_input, rent_input]))
    return render_template('index.html')


@app.route("/table/<user_input>")
def new_page(user_input: str):
    global total_rent, num_room
    print("user input ", user_input)
    print(type(user_input))
    s = ''
    res = []
    for i in user_input:
        if i != '[' and i != ']' and i != ',':
            s += i
        elif len(s) > 0:
            res.append(int(s))
            s = ''

    print(res)
    num_room = int(res[0])
    total_rent = int(res[1])
    return render_template("table.html", rooms=num_room, rents=total_rent)


@app.route("/home", methods=['POST'])
def home():
    print("yesss")
    global total_rent, num_room
    total_rent = 0
    num_room = 0
    return redirect(url_for("index"))


@app.route("/res", methods=['GET', 'POST'])
def res():
    global total_rent, num_room
    data = {}
    for key, value in request.form.to_dict(flat=False).items():
        data[key] = value

    rooms = [key for key in data.keys() if key.startswith('room')]
    values = {name: {room: int(data[room][i]) for room in rooms} for i, name in enumerate(data['name'])}
    budgets = {name: int(budget) for name, budget in zip(data['name'], data['budget'])}
    for i in values.values():
        sum_value = 0
        for j in i.values():
            sum_value += j
        if total_rent != sum_value:
            return render_template("table.html", rooms=num_room, rents=total_rent)
    res_algo = optimal_envy_free(AgentList(values), float(total_rent), budgets)
    return redirect(url_for("page_result", user_input=res_algo))


@app.route("/result/<user_input>")
def page_result(user_input):
    print(type(user_input))
    tuple_of_lists = ast.literal_eval(user_input)
    dict1 = dict(tuple_of_lists[0])
    dict2 = dict(tuple_of_lists[1])
    print(dict1)
    print(dict2)
    s = []
    for i in dict1:
        s.append(f"'{i}' get room '{dict1[i]}' for price $ {dict2[dict1[i]]} \n")
    print("the result is : \n", s)
    return render_template("result.html", string_res=s)


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5001)
