from fairpy.rent.Algorithms import optimal_envy_free as optimal
from fairpy.rent.Algorithms_Thread import optimal_envy_free as thread_optimal
import doctest
import networkx as nx
import numpy as np
from fairpy.rent.Calculation_Assistance import *
from fairpy.agentlist import AgentList
import logging
from concurrent.futures import ThreadPoolExecutor
import time
import matplotlib.pyplot as plt


def draw_graph(arr_num_agent:list,result_optimal: list, result_thread: list):
    """
    I take the code of plot form this web
    https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html
    :param res:
    :return: plot of apx graph
    """
    arr_num_agent = [i*10 for i in arr_num_agent]
    x = np.arange(len(arr_num_agent))  # the label locations
    width = 0.33  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, result_optimal, width, label='result_optimal')
    rects2 = ax.bar(x + width / 2, result_thread, width, label='result_thread')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Time')
    ax.set_xlabel('Agent')
    ax.set_title('Comparison of thread between without thread')
    ax.set_xticks(x)
    ax.set_xticklabels(arr_num_agent, rotation=270)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', rotation=270)

    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    counter = 1
    result_optimal = []
    result_thread = []
    arr_num_agent = []
    while counter < 16:
        num_agents = 10 * counter
        num_items = 10 * counter
        agents = {f"Agent{i}": {f"Item{j}": (i + j) * 10 for j in range(num_items)} for i in range(num_agents)}
        rent = num_agents * num_items * 10
        budgets = {f"Agent{i}": (i + 1) * 100 for i in range(num_agents)}
        ex = AgentList(agents)
        t2 = 0
        t1 = time.time()
        res = optimal(ex, rent, budgets)
        t2 = time.time() - t1
        print(f"Optimal ,number of agent is {num_agents} , time : {round(t2, 4)} , result : {res}")
        result_optimal.append(round(t2, 4))
        t2 = 0
        t1 = time.time()
        res = thread_optimal(ex, rent, budgets)
        t2 = time.time() - t1
        print(f"Thread ,number of agent is {num_agents} , time : {round(t2, 4)} , result : {res}")
        result_thread.append(round(t2, 4))
        arr_num_agent.append(counter)
        counter += 1

    draw_graph(arr_num_agent,result_optimal, result_thread)
