

from fairpy.items.proportional_borda_allocations.proportional_borda_allocations import *
import matplotlib.pyplot as plt
import improvingPreformance.utilsCpp as utilsCpp
import utils as utilsPython
from timeit import default_timer as timer
from typing import Callable
from typing import Iterable
FILE_OF_RESULTS = 'fairpy/items/proportional_borda_allocations/results_of_times/'


def time_calculation_of_function(func:Callable,*arg, **args):
    start = timer()
    func(*arg, **args)
    end = timer()
    return end - start

def drawing_results_of_times(cTimes, pyTimes, file_name):
    cTimes = sorted(cTimes, key=lambda tup: tup[0])
    pyTimes = sorted(pyTimes, key=lambda tup: tup[0])
    y_c = list(map(lambda tup: tup[1], cTimes))
    num_items = list(map(lambda tup: tup[0], cTimes))
    y_py = list(map(lambda tup: tup[1], pyTimes))
    plt.clf()
    plt.plot(num_items, y_c , num_items, y_py)
    plt.legend(['cTime','pyTime'])
    plt.savefig(FILE_OF_RESULTS + file_name)

def calculate_times_in_c_and_python_and_draw_them(f:Callable, it_n:Iterable, it_p:Iterable, file_name:str):
    cTimes = []
    pyTimes = []
    for n in it_n:
        for p in it_p:
            k = n*p
            agentsI = utilsPython.get_agents_with_permutations_of_valuations(n, k) 
            time_c = time_calculation_of_function(f,agentsI, improvingPerformance=True)
            cTimes.append((k, time_c))
            time_py = time_calculation_of_function(f, agentsI)
            pyTimes.append((k, time_py))

    drawing_results_of_times(cTimes, pyTimes, file_name=file_name)


if __name__ == "__main__":
    calculate_times_in_c_and_python_and_draw_them(f=proportional_division_equal_number_of_items_and_players, 
        it_n=range(1,1000,10),it_p=range(1,2), file_name='equal_number_of_items_and_players')
    calculate_times_in_c_and_python_and_draw_them(f=proportional_division_with_p_even,
        it_n=range(3,500,10),it_p=range(2,10,2), file_name='p_is_even')
    calculate_times_in_c_and_python_and_draw_them(f=proportional_division_with_number_of_agents_odd, 
        it_n=range(3,500,50),it_p=range(3,5), file_name='number_of_agents_odd2')
    calculate_times_in_c_and_python_and_draw_them(f=proportional_division, 
        it_n=range(2,500,50),it_p=range(2,4), file_name='proportional_division3')
