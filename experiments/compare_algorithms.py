#!python3

"""
Compare the performance of several algorithms for fair item allocation.

AUTHOR: Moriya Elgrabli and Liad Nagi
SINCE:  27 Apr 2022
"""

from typing import  List
from copy import deepcopy
from spliddit import spliddit_instances # file that get data from data file
from fairpy.agents import  AdditiveAgent
from fairpy import Allocation, agents_from
from fairpy.items.max_welfare import *
from fairpy.items import  (
    approximation_maximin_share as ams,
    leximin as lexi,
    propm_allocation as promp,
)
import matplotlib.pyplot as plt
import numpy as np



def min_and_sum(alloc: Allocation,multiply=1):
    """
    Return sum of agents utilities and the minimum utility for given allocation.
    if multiply is given (which means valuations were normelized and need to be re-valuated)
    multiply by the value
    """
    sum_all_sher = multiply*sum(alloc.utility_profile())
    min_val_agent =multiply*min(alloc.utility_profile())
    return min_val_agent, sum_all_sher



# def convert_valuation_matrix_to_dict(valuation_matrix):
#     """
#     convert values in given as a valuation matrix - rows are agents, colomes are item valuations
#     to dict with names to agents ang items for easier use.
#     >>> val_matrix=    [[ 500,0,0,125,375],[0,500,167,83,250],[0,1000,0,0,0]]
#     >>> convert_valuation_matrix_to_dict(val_matrix)
#     {'agent0': {'x0': 500, 'x1': 0, 'x2': 0, 'x3': 125, 'x4': 375}, 'agent1': {'x0': 0, 'x1': 500, 'x2': 167, 'x3': 83, 'x4': 250}, 'agent2': {'x0': 0, 'x1': 1000, 'x2': 0, 'x3': 0, 'x4': 0}}
#     """

#     full_valuations_dict={}
#     for row_index, row in enumerate(valuation_matrix):
#         valuations_dict={}
#         for col_index, col in enumerate(row):
#             valuations_dict["x"+str(col_index)]=col
#         full_valuations_dict["agent"+str(row_index)]=valuations_dict
#     return full_valuations_dict


def assign_remaining_items(alloc:dict,remaining_items:List[str],agents:List[AdditiveAgent])->dict:
    alloc=deepcopy(alloc)
    flag_some_agent_want=True

    while(flag_some_agent_want):
        #if there is round where no agent want any item- end 
        flag_some_agent_want=False
        for agent in reversed(agents):
            for item in remaining_items:
                val_for_item=agent.value(item)
                if val_for_item>0:
                    flag_some_agent_want=True
                    alloc[agent._name].append(item)
                    remaining_items.remove(item)
                    break
    return alloc

        
def get_mms_alloc(agents):
    """
        Get deviation case in dictionary format (valuation of agents to items), and returns 3/4_mms allocation. 
        (with and without assigning remaining items)  
        >>> data={'agent0': {'x0': 1000.0, 'x1': 0.0, 'x2': 0.0}, 'agent1': {'x0': 0.0, 'x1': 1000.0, 'x2': 0.0}}
        >>> alloc,alloc_after_dividing_remaining_items=get_mms_alloc(data)
        >>> alloc
        agent0 gets {x0} with value 1e+03.
        agent1 gets {} with value 0.
        <BLANKLINE>
        >>> alloc_after_dividing_remaining_items
        agent0 gets {x0} with value 1e+03.
        agent1 gets {x1} with value 1e+03.
        <BLANKLINE>
        >>> data=[[1000.0,0.0,0.0],[0.0,1000.0,0.0]]
        >>> alloc,alloc_after_dividing_remaining_items=get_mms_alloc(data)
        >>> alloc
        Agent #0 gets {0} with value 1e+03.
        Agent #1 gets {} with value 0.
        <BLANKLINE>
        >>> alloc_after_dividing_remaining_items
        Agent #0 gets {0} with value 1e+03.
        Agent #1 gets {1} with value 1e+03.
        <BLANKLINE>

    """
    agents=agents_from(agents)  # Handles various input formats

    alloc, remaining_items= ams.three_quarters_MMS_allocation_algorithm(agents) 
    
    # Build the real allocations with the values    
    # Map the result to somting like this "{'Alice': ['x3'], 'Bruce': ['x2'], 'Carl': ['x1']}"
    dict_alloc=dict(alloc.map_agent_to_bundle())
   
    alloc_with_dividing_remaining_items=assign_remaining_items(dict_alloc,remaining_items,agents)
    alloc_with_dividing_remaining_items = Allocation(agents, alloc_with_dividing_remaining_items)

    return(alloc,alloc_with_dividing_remaining_items)

def plot_an_statistic(arr: list(), name: str()):
    # x-coordinates of left sides of bars
    left = [1, 2, 3, 4]

    # heights of bars
    height = arr

    # labels for bars
    tick_label = ['MMS', 'promp', 'leximin', 'max sum']

    # plotting a bar chart
    plt.bar(left, height, tick_label = tick_label,
            width = 0.8, color = ['blue', 'green', 'yellow', 'red'])
    
    # naming the x-axis
    # plt.xlabel('x - axis')
    # naming the y-axis
    # plt.ylabel('y - axis')
    # plot title
    plt.title(name)
    plt.annotate(text=str(format(height[0], ".3f")), xy=(left[0]-0.2, height[0]))
    plt.annotate(text=str(format(height[1], ".3f")), xy=(left[1]-0.2, height[1]))
    plt.annotate(text=str(format(height[2], ".3f")), xy=(left[2]-0.2, height[2]))
    plt.annotate(text=str(format(height[3], ".3f")), xy=(left[3]-0.2, height[3]))
    # function to show the plot
    plt.show()

    return

def plot_graph_statistics(arr: dict(), name: str(), ylim: int=4000):
    # x axis values
    i = list()
    j = list()
    for k1,k2 in arr.items():
        i.append(k1)
        j.append(k2)
    x = i
    # corresponding y axis values
    y=list()
    
    for k in j:
        y.append(k[0])

    y2=list()
    for k in j:
        y2.append(k[1])

    y3=list()
    for k in j:
        y3.append(k[2])
    
    y4=list()
    for k in j:
        y4.append(k[3])


    line = np.linspace(0,1,100)
    fig=plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(line,line , label='mms',color='blue')
    ax.plot(line, line**2,label='propm', color='green')
    ax.plot(line, line**3, label='leximin',color='y')
    ax.plot(line, line**4, label='max sum',color='red')
    ax.legend(loc=1, )

    # plotting the points
    plt.plot(x, y, color='blue', linestyle='dashed', linewidth = 1,
            marker='o', markerfacecolor='blue', markersize=7)
    plt.plot(x, y2, color='green', linestyle='dashed', linewidth = 1,
            marker='o', markerfacecolor='green', markersize=7)
    plt.plot(x, y3, color='y', linestyle='dashed', linewidth = 1,
            marker='o', markerfacecolor='y', markersize=7)
    plt.plot(x, y4, color='red', linestyle='dashed', linewidth = 1,
            marker='o', markerfacecolor='red', markersize=7)
    # setting x and y axis range
    plt.ylim(1,ylim)
    plt.xlim(0,15)

    # naming the x axis
    plt.xlabel('number of agents')
    # naming the y axis
    #plt.ylabel('y - axis')

    # giving a title to my graph
    plt.title(name)

    # function to show the plot
    plt.show()

    return



if __name__=="__main__":
    
    # import doctest
    # (failures, tests) = doctest.testmod(report=True)
    # print("{} failures, {} tests".format(failures, tests))

    min_sum=[0,0,0,0]
    sum_of_sum=[0,0,0,0]
    cont_for_avg = [0,0,0,0]
    cont_errors = [0,0,0,0]
    
    max_age = 15
    min_age = 2
    sum_of_sum_bay_len = dict()
    min_sum_bay_len = dict()
    cont_for_avg_bay_len = dict()
    for i in range(min_age, (max_age+1)):
        sum_of_sum_bay_len[i]=[0,0,0,0]
        min_sum_bay_len[i]=[0,0,0,0]
        cont_for_avg_bay_len[i]=[0,0,0,0]
    
    assignments_generator=spliddit_instances()

    #730 cases
    for i, assignment in enumerate(assignments_generator):

        ind,val_matrix=assignment
        len_agents = len(val_matrix)
        print (f"\n INSTANCE {i}: {len_agents} agents")
        try:
            alloc_mms,alloc_mms_with_dividing_items=get_mms_alloc(deepcopy(val_matrix))    
            # print("mms:\n",alloc_mms,"\nmms with assing:\n",alloc_mms_with_dividing_items)
            min1,sum1 = min_and_sum(alloc_mms_with_dividing_items)
            min_sum[0]+=min1
            sum_of_sum[0]+=sum1
            cont_for_avg[0]+=1
            sum_of_sum_bay_len[len_agents][0]+=sum1
            min_sum_bay_len[len_agents][0]+=min1
            cont_for_avg_bay_len[len_agents][0]+=1
        except Exception as e:
            cont_errors[0]+=1
            print("error in mms test ",i, e)

        try:
            alloc_propm=promp.propm_allocation(deepcopy(val_matrix))
            # print("propm:\n",alloc_propm)
            min2,sum2 = min_and_sum(alloc_propm,1000)
            min_sum[1]+=min2
            sum_of_sum[1]+=sum2
            cont_for_avg[1]+=1
            sum_of_sum_bay_len[len_agents][1]+=sum2
            min_sum_bay_len[len_agents][1]+=min2
            cont_for_avg_bay_len[len_agents][1]+=1

        except Exception as e:
            cont_errors[1]+=1
            print("Error in promp test "+str(i)+":\n"+str(e)+"\nTest case:\n"+str(val_matrix)+"\n")
            # with open('promp_errors.txt', 'a') as f:
            #     f.write("Error in promp test "+str(i)+":\n"+str(e)+"\nTest case:\n"+str(val_dict)+"\n")

        try:
            alloc_leximin=lexi.leximin_optimal_allocation(deepcopy(val_matrix), upper_tolerance=1.02)
            # print("leximin:\n",alloc_leximin)
            min3,sum3 = min_and_sum(alloc_leximin)
            min_sum[2]+=min3
            sum_of_sum[2]+=sum3
            cont_for_avg[2]+=1
            sum_of_sum_bay_len[len_agents][2]+=sum3
            min_sum_bay_len[len_agents][2]+=min3
            cont_for_avg_bay_len[len_agents][2]+=1
        except Exception as e:
            cont_errors[2]+=1
            print("error in leximin test ",i, e ,val_matrix)

        try:
            alloc_max_sum = max_sum_allocation((deepcopy(val_matrix))).round(3)
            # print("i: " +str(i),"alloc_um:",alloc_max_sum,sep='\n')
            min4,sum4 = min_and_sum(alloc_max_sum)
            min_sum[3]+=min4
            sum_of_sum[3]+=sum4
            cont_for_avg[3]+=1
            sum_of_sum_bay_len[len_agents][3]+=sum4
            min_sum_bay_len[len_agents][3]+=min4
            cont_for_avg_bay_len[len_agents][3]+=1
        except Exception as e:
            cont_errors[3]+=1
            print("error in max sum test ",i, e)
    
    # min_sum  = [238359.0, 236205.0, 389552.02057315334, 234400.0]
    # sum_of_sum  = [970628.0, 959304.0, 1034831.5491809144, 1106689.0]
    # cont_for_avg = [730, 730, 730, 730]
    # avg_of_sum  = [1329.627397260274, 1314.1150684931506, 1417.5774646313896, 1516.0123287671233]
    # avg_of_min  =[326.5191780821918, 323.56849315068496, 533.6329048947306, 321.09589041095893]
    # cont_errors  =[0, 0, 0, 0]
    # sum_of_sum_bay_len =  {2: [474556.0, 459932.0, 493229.4174257124, 505362.0], 3: [283091.0, 281452.0, 304382.70627232903, 327655.0], 4: [69965.0, 69032.0, 75701.95430424802, 84316.0], 5: [37396.0, 42071.0, 45295.426575084086, 52890.0], 6: [29440.0, 31585.0, 33295.45273185204, 39918.0], 7: [14807.0, 15552.0, 14811.870902421602, 19646.0], 8: [32268.0, 32317.0, 34632.96771375889, 38229.0], 9: [4351.0, 3799.0, 5199.573828253575, 6835.0], 10: [13164.0, 14457.0, 16937.35457535646, 19195.0], 11: [2751.0, 2309.9999999999995, 2793.757214833698, 3096.0], 12: [0, 0, 0, 0], 13: [0, 0, 0, 0], 14: [0, 0, 0, 0], 15: [8839.0, 6797.0, 8551.067637064752, 9547.0]}
    # min_sum_bay_len =  {2: [177188.0, 170067.0, 246614.7087128562, 177374.0], 3: [49876.0, 52500.0, 101010.78246515949, 47039.0], 4: [5724.0, 6666.0, 18601.329750626228, 5145.0], 5: [3018.0, 3105.0, 8936.338476507724, 2131.0], 6: [651.0, 1345.0, 5486.500676896816, 1591.0], 7: [310.0, 499.0, 2115.9815574887944, 229.0], 8: [1473.0, 1885.0, 3897.0954069695576, 891.0], 9: [24.0, 43.0, 577.7304253615076, 0.0], 10: [0.0, 0.0, 1493.7354575356455, 0.0], 11: [95.0, 95.0, 253.97792862124524, 0.0], 12: [0, 0, 0, 0], 13: [0, 0, 0, 0], 14: [0, 0, 0, 0], 15: [0.0, 0.0, 563.8397151301593, 0.0]}
    # cont_for_avg_bay_len =  {2: [401, 401, 401, 401], 3: [209, 209, 209, 209], 4: [48, 48, 48, 48], 5: [23, 23, 23, 23], 6: [15, 15, 15, 15], 7: [6, 6, 6, 6], 8: [14, 14, 14, 14], 9: [2, 2, 2, 2], 10: [8, 8, 8, 8], 11: [1, 1, 1, 1], 12: [0, 0, 0, 0], 13: [0, 0, 0, 0], 14: [0, 0, 0, 0], 15: [3, 3, 3, 3]}
        
    avg_of_sum = [sum_of_sum[0]/cont_for_avg[0],sum_of_sum[1]/cont_for_avg[1],sum_of_sum[2]/cont_for_avg[2], sum_of_sum[3]/cont_for_avg[3]]
    avg_of_min = [min_sum[0]/cont_for_avg[0],min_sum[1]/cont_for_avg[1],min_sum[2]/cont_for_avg[2], min_sum[3]/cont_for_avg[3]]

    avg_of_sum_by_len = dict()
    avg_of_min_by_len = dict()
    for i,j in sum_of_sum_bay_len.items():
        if(cont_for_avg_bay_len[i][0]!=0 and cont_for_avg_bay_len[i][1]!=0 and cont_for_avg_bay_len[i][2]!=0):
            avg_of_sum_by_len[i]=[j[0]/cont_for_avg_bay_len[i][0], j[1]/cont_for_avg_bay_len[i][1], j[2]/cont_for_avg_bay_len[i][2],j[3]/cont_for_avg_bay_len[i][3]]

    for i,j in min_sum_bay_len.items():
        if(cont_for_avg_bay_len[i][0]!=0 and cont_for_avg_bay_len[i][1]!=0 and cont_for_avg_bay_len[i][2]!=0):
            avg_of_min_by_len[i]=[i*(j[0]/cont_for_avg_bay_len[i][0]), i*(j[1]/cont_for_avg_bay_len[i][1]), i*(j[2]/cont_for_avg_bay_len[i][2]), i*(j[3]/cont_for_avg_bay_len[i][3])]        


    plot_graph_statistics(avg_of_sum_by_len, "avg of sum by number agents")
    plot_graph_statistics(avg_of_min_by_len, "avg of min by number agents",4000)
     
    print("min_sum ",min_sum)
    print("sum_of_sum ",sum_of_sum)
    print("cont_for_avg ",cont_for_avg)
    print("avg_of_sum ",avg_of_sum)
    print("avg_of_min ",avg_of_min)
    print("cont_errors ",cont_errors) 
    print("sum_of_sum_bay_len = ",sum_of_sum_bay_len)
    print("min_sum_bay_len = ",min_sum_bay_len)
    print("cont_for_avg_bay_len = ",cont_for_avg_bay_len)

    # plot_an_statistic(min_sum, "sum of minimum")
    # plot_an_statistic(sum_of_sum, "sum of sum")
    plot_an_statistic(avg_of_sum, "avg of sum")
    plot_an_statistic(avg_of_min, "avg of min")
    plot_an_statistic(cont_errors, "errors")
       