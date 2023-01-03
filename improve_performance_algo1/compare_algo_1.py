import random
import itertools
import time
from envy_freeness_and_equitability_with_payments import envy_freeness_and_equitability_with_payments
from improve_performance_algo1.envy_freeness_and_equitability_with_payments_cython import envy_freeness_and_equitability_with_payments_cython
import matplotlib.pyplot as plt
import pyximport

pyximport.install()


def make_agent_list(size):
    """
    A function to create a list of agents of size 'size'
    """

    return ["agent_" + str(i) for i in range(1, size + 1)]


def make_eval_dict(size):
    """
    A function to generate random values for each possible bundle
    """
    random_dict = {}
    for i in range(97, size + 97):
        key = f"{chr(i)}"
        value = random.randint(1, 100)
        random_dict[key] = value
    keys = list(random_dict.keys())
    for i in range(2, size + 1):
        for combination in itertools.combinations(keys, i):
            key = ''.join(combination)
            value = random.randint(1, 100)
            random_dict[key] = value
    return random_dict


def make_allo_dict(size):
    """
    A function to create the initial allocation
    """
    allo_dict = {}
    i = 97
    for agent in make_agent_list(size):
        temp = []
        temp.append(f"{chr(i)}")
        allo_dict[agent] = temp
        i = i + 1
    return allo_dict


def match_agent_to_eval(size: int):
    """
    A function to create a dictionary of values for each agent
    """
    eval_dict = {}
    for agent in make_agent_list(size):
        eval_dict[agent] = make_eval_dict(size)
    return eval_dict

#Creating lists of running times for comparison
py_run = []
cy_run = []
for i in range(2, 21):
    eval_func = match_agent_to_eval(i)
    allocation = make_allo_dict(i)
    t1 = time.time()
    envy_freeness_and_equitability_with_payments(eval_func, allocation)
    py_run.append(time.time() - t1)
    t2 = time.time()
    envy_freeness_and_equitability_with_payments_cython(eval_func, allocation)
    cy_run.append(time.time() - t2)
print(py_run)
print(cy_run)


plt.title("python vs cython")
plt.plot(py_run, 'g', cy_run, 'r')
plt.xlabel("number of agents and objects")
plt.ylabel("time (in sec)")
plt.legend(["python", "cython"])
plt.figure(figsize=(8,10))
plt.show()