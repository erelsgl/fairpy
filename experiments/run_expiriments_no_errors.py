#!python3

"""

AUTHOR: Moriya Elgrabli and Liad Nagi
SINCE:  27 Apr 2022
"""
from typing import  List
from copy import deepcopy
from spliddit import spliddit_instances,SPLIDDIT_TASKS # file that get data from data file
from fairpy.agents import  AdditiveAgent
from fairpy import Allocation, allocations
from fairpy.items.max_welfare import *

from fairpy.items import  (
    approximation_maximin_share as ams,
    leximin as lexi,
    propm_allocation as promp,
)
import matplotlib.pyplot as plt
import numpy as np



def min_and_sum(alloc: Allocation):
    sum_all_sher = sum(alloc.utility_profile())
    min_val_agent = min(alloc.utility_profile())
    return min_val_agent, sum_all_sher


def convert_valuation_matrix_to_dict(valuation_matrix):
    """
    convert values in given as a valuation matrix - rows are agents, colomes are item valuations
    to dict with names to agents ang items for easyer use.
    >>> val_matrix=    [[ 500,0,0,125,375],[0,500,167,83,250],[0,1000,0,0,0]]
    >>> convert_valuation_matrix_to_dict(val_matrix)
    {'agent0': {'x0': 500, 'x1': 0, 'x2': 0, 'x3': 125, 'x4': 375}, 'agent1': {'x0': 0, 'x1': 500, 'x2': 167, 'x3': 83, 'x4': 250}, 'agent2': {'x0': 0, 'x1': 1000, 'x2': 0, 'x3': 0, 'x4': 0}}
    """

    full_valuations_dict={}
    for row_index, row in enumerate(valuation_matrix):
        valuations_dict={}
        for col_index, col in enumerate(row):
            valuations_dict["x"+str(col_index)]=col
        full_valuations_dict["agent"+str(row_index)]=valuations_dict
    return full_valuations_dict


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
                    alloc[agent._name][item]=val_for_item
                    remaining_items.remove(item)
                    break
    return alloc

        
def get_mms_alloc(data: dict):
    """
        Get deviation case in dictionary format (valuation of agents to items), and returns 3/4_mms allocation. 
        (with and without assigning remaining items)  
        >>> data={'agent0': {'x0': 1000.0, 'x1': 0.0, 'x2': 0.0}, 'agent1': {'x0': 0.0, 'x1': 1000.0, 'x2': 0.0}}
        >>> get_mms_alloc(data)
    """
    # build the agents from the data    
    agents = []
    for i,j in data.items():
        agents.append(AdditiveAgent(j, name=i))
    # Get all the items name from the first agents 
    name = str(agents[0].name())
    items = list(data[name].keys())
    
    # algo 7
    temp_agents = ams.agents_conversion_to_ordered_instance(agents, items)

    # algo 4
    res = ams.three_quarters_MMS_allocation(temp_agents, items)
    # Map the result to somting like this "{'Alice': ['x3'], 'Bruce': ['x2'], 'Carl': ['x1']}"
    res=dict(res.map_agent_to_bundle())
    

    # algo 8 -Get the real allocation
    real_res, remaining_items= ams.get_alpha_MMS_allocation_to_unordered_instance(agents, res, items)
    
    
    # print(real_res)
    # agent_names = list(real_res.keys())
    # # print(agent_names)

    # Build the real allocations with the values    
    alloc = dict()
    for nam,ite in real_res.items():
        alloc[nam]=dict()
        for k in ite:
            alloc[nam][k] = data[nam][k]


    alloc_with_dividing_remaining_items=assign_remaining_items(alloc,remaining_items,agents)
    #alloc = Allocation(data1, alloc1)
    alloc = Allocation(data, alloc)
    alloc_with_dividing_remaining_items = Allocation(data, alloc_with_dividing_remaining_items)

    #print("alloc = ",alloc)
    #print("alloc_with_dividing_remaining_items = ",alloc_with_dividing_remaining_items)
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
    # import sys

    # (failures, tests) = doctest.testmod(report=True)
    # print("{} failures, {} tests".format(failures, tests))
    
    # val_dict={'agent0': {'x0': 1000.0, 'x1': 0.0, 'x2': 0.0}, 'agent1': {'x0': 0.0, 'x1': 1000.0, 'x2': 0.0}}
    
    # alloc_mms=get_mms_alloc(val_dict)
    min_sum=[0,0,0,0]
    sum_of_sum=[0,0,0,0]
    cont_for_avg = [0,0,0,0]
    cont_errors = [0]

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
    
        val_dict=convert_valuation_matrix_to_dict(val_matrix)
    
        # if(i==11):
        #     break
        #print(i,":")
        #print("vals:",val_dict)
        len_agents = len(val_dict)
        #print(len_agents)
        try:
            alloc_mms,alloc_mms_with_dividing_items=get_mms_alloc(deepcopy(val_dict))
            alloc_propm=promp.propm_allocation(deepcopy(val_dict))
            alloc_leximin=lexi.leximin_optimal_allocation(deepcopy(val_dict))
            alloc_max_sum = max_sum_allocation((deepcopy(val_dict))).round(3)

            # print("mms:\n",alloc_mms,"\nmms with assing:\n",alloc_mms_with_dividing_items)
            min1,sum1 = min_and_sum(alloc_mms_with_dividing_items)
            min_sum[0]+=min1
            sum_of_sum[0]+=sum1
            cont_for_avg[0]+=1
            sum_of_sum_bay_len[len_agents][0]+=sum1
            min_sum_bay_len[len_agents][0]+=min1
            cont_for_avg_bay_len[len_agents][0]+=1

            min2,sum2 = min_and_sum(alloc_propm)
            min_sum[1]+=min2
            sum_of_sum[1]+=sum2
            cont_for_avg[1]+=1
            sum_of_sum_bay_len[len_agents][1]+=sum2
            min_sum_bay_len[len_agents][1]+=min2
            cont_for_avg_bay_len[len_agents][1]+=1
            #print("propm:\n",alloc_propm)

            # print("leximin:\n",alloc_leximin)
            min3,sum3 = min_and_sum(alloc_leximin)
            min_sum[2]+=min3
            sum_of_sum[2]+=sum3
            cont_for_avg[2]+=1
            sum_of_sum_bay_len[len_agents][2]+=sum3
            min_sum_bay_len[len_agents][2]+=min3
            cont_for_avg_bay_len[len_agents][2]+=1

            # print("i: " +str(i),"val dict:",val_dict,"alloc_um:",alloc_max_aum,sep='\n')
            min4,sum4 = min_and_sum(alloc_max_sum)
            min_sum[3]+=min4
            sum_of_sum[3]+=sum4
            cont_for_avg[3]+=1
            sum_of_sum_bay_len[len_agents][3]+=sum4
            min_sum_bay_len[len_agents][3]+=min4
            cont_for_avg_bay_len[len_agents][3]+=1
        except Exception as e:
            cont_errors[0]+=1
    """
    min_sum =  [223195.0, 221308.0, 331446.2186204845, 213764.0]
sum_of_sum  =[790399.0, 783365.0, 839050.699010763, 889838.0]
cont_for_avg = [606, 606, 606, 606]
avg_of_sum = [1304.2887788778878, 1292.6815181518152, 1384.5721105788168, 1468.3795379537953]
avg_of_min = [368.3085808580858, 365.19471947194717, 546.9409548192814, 352.74587458745873]
cont_errors = [124]
sum_of_sum_bay_len =  {2: [433454.0, 420243.0, 448268.9159698037, 459643.0], 3: [223036.0, 226489.0, 239838.5490207545, 258001.0], 4: [49379.0, 47962.0, 51920.706769091434, 57657.0], 5: [22968.0, 25226.0, 28733.648169116346, 32495.0], 6: [18033.0, 19667.0, 21070.75689769466, 25465.0], 7: [4123.0, 4013.0, 4084.831654262599, 4926.0], 8: [25544.0, 26070.0, 26516.696911908417, 29103.0], 9: [4271.0, 3799.0, 5199.573828253575, 6835.0], 10: [6840.0, 7586.0, 10623.262575043742, 12617.0], 11: [2751.0, 2310.0, 2793.757214833698, 3096.0], 12: [0, 0, 0, 0], 13: [0, 0, 0, 0], 14: [0, 0, 0, 0], 15: [0, 0, 0, 0]}
min_sum_bay_len =  {2: [171353.0, 164370.0, 224134.45798490185, 168509.0], 3: [42654.0, 46189.0, 79860.30999104517, 38084.0], 4: [4573.0, 5292.0, 12915.896460025127, 3289.0], 5: [2507.0, 2497.0, 5726.359265902422, 1822.0], 6: [356.0, 984.0, 3449.0513712039256, 1169.0], 7: [160.0, 153.0, 583.5473791803711, 0.0], 8: [1473.0, 1685.0, 2882.56155673825, 891.0], 9: [24.0, 43.0, 577.730425361508, 0.0], 10: [0.0, 0.0, 1062.3262575043736, 0.0], 11: [95.0, 95.0, 253.97792862124524, 0.0], 12: [0, 0, 0, 0], 13: [0, 0, 0, 0], 14: [0, 0, 0, 0], 15: [0, 0, 0, 0]}
cont_for_avg_bay_len =  {2: [361, 361, 361, 361], 3: [166, 166, 166, 166], 4: [35, 35, 35, 35], 5: [14, 14, 14, 14], 6: [9, 9, 9, 9], 7: [2, 2, 2, 2], 8: [10, 10, 10, 10], 9: [2, 2, 2, 2], 10: [6, 6, 6, 6], 11: [1, 1, 1, 1], 12: [0, 0, 0, 0], 13: [0, 0, 0, 0], 14: [0, 0, 0, 0], 15: [0, 0, 0, 0]}
    """
    avg_of_sum = [sum_of_sum[0]/cont_for_avg[0],sum_of_sum[1]/cont_for_avg[1],sum_of_sum[2]/cont_for_avg[2], sum_of_sum[3]/cont_for_avg[3],]
    avg_of_min = [min_sum[0]/cont_for_avg[0],min_sum[1]/cont_for_avg[1],min_sum[2]/cont_for_avg[2], min_sum[3]/cont_for_avg[3]]
    
    avg_of_sum_by_len = dict()
    avg_of_min_by_len = dict()
    for i,j in sum_of_sum_bay_len.items():
        #print(j[0],"//",cont_for_avg_bay_len[i][0]," = ")
        #print(j[0]/cont_for_avg_bay_len[i][0])
        if(cont_for_avg_bay_len[i][0]!=0 and cont_for_avg_bay_len[i][1]!=0 and cont_for_avg_bay_len[i][2]!=0):
            avg_of_sum_by_len[i]=[j[0]/cont_for_avg_bay_len[i][0], j[1]/cont_for_avg_bay_len[i][1], j[2]/cont_for_avg_bay_len[i][2],j[3]/cont_for_avg_bay_len[i][3]]

    for i,j in min_sum_bay_len.items():
        #print(j[0],"//",cont_for_avg_bay_len[i][0]," = ")
        #print(j[0]/cont_for_avg_bay_len[i][0])
        if(cont_for_avg_bay_len[i][0]!=0 and cont_for_avg_bay_len[i][1]!=0 and cont_for_avg_bay_len[i][2]!=0):
            avg_of_min_by_len[i]=[j[0]/cont_for_avg_bay_len[i][0], j[1]/cont_for_avg_bay_len[i][1], j[2]/cont_for_avg_bay_len[i][2], j[3]/cont_for_avg_bay_len[i][3]]        
    
    plot_graph_statistics(avg_of_sum_by_len, "avg of sum by number agents")
    plot_graph_statistics(avg_of_min_by_len, "avg of min by number agents",700)
     
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
    

            

    