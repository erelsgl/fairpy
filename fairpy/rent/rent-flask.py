from flask import *
from flask_cors import CORS
from fairpy.rent.Algorithms import optimal_envy_free

app = Flask(__name__)
CORS(app)


@app.route('/submit', methods=['POST'])
def handle_submit():
    data = request.get_json()
    agents = data['agents']
    # do something with the agents data
    print(agents)
    return agents


if __name__ == '__main__':
    app.run()
