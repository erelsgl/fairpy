import csv
import io

from flask import Flask, request, render_template
from fairpy.items.fair_course_allocation_implementation import general_course_allocation
from fairpy.items.fair_course_allocation_implementation import *
from fairpy.items.valuations import ValuationMatrix

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/allocation', methods=['POST'])
def allocation():

    file_name = request.files['file_name']
    if file_name:
        stream = io.StringIO(file_name.stream.read().decode("UTF8"), newline=None)
        data = list(csv.reader(stream))
        allocate = list(find_allocation(data))
        return render_template('allocation.html', allocate=allocate)


def find_allocation(data):

    placement_matrix = []

    try:

        num_of_courses: int = int(data[0][0])
        print(num_of_courses)
        capacity = list(map(int, data[1]))
        print(capacity)
        utilities_matrix = [list(map(int, row)) for row in data[2:]]
        print(utilities_matrix)

        placement_matrix = general_course_allocation(ValuationMatrix(utilities_matrix), capacity, num_of_courses)
        print(placement_matrix)

    except:

        pass

    return placement_matrix

# https://stackoverflow.com/questions/33070395/not-able-to-parse-a-csv-file-uploaded-using-flask


