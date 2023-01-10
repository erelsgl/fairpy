from flask import Flask, send_from_directory, request, jsonify
from fairpy.rent.Algorithms import optimal_envy_free
from fairpy.agentlist import AgentList

app = Flask(__name__, static_folder='rent-react/build', static_url_path='/')


@app.route('/')
def serve():
    return send_from_directory('rent-react/build', 'index.html')


@app.route('/submit', methods=['POST'])
def handle_submit():
    data = request.get_json()
    agents = data['agents']
    rent = data['rent']

    print(agents, rent)
    values_dict = {agent['name']: {f'Room{index + 1}': int(value) for index, value in enumerate(agent['values'])} for agent
                   in agents}
    print("values", values_dict)
    print("rent", float(rent))
    budget_dict = {agent['name']: int(agent['budget']) for agent in agents}
    print(budget_dict)
    result = optimal_envy_free(AgentList(values_dict), float(rent), budget_dict)
    print(result)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
