"""
Utility functions for reading instances from the Spliddit website.
The database should be in sqlite format.

AUTHOR: Erel Segal-Halevi
SINCE:  2020-07
"""

SPLIDDIT_DATABASE_FILE = 'spliddit-2020-07-31-goods-real.db'

import sqlite3, numpy as np

# Application IDs:

SPLIDDIT_GOODS = 2
SPLIDDIT_TASKS = 5


def spliddit_instances(first_id:int=0, application_id=SPLIDDIT_GOODS, remove_demo_instances=False):
    """
    Generate all "divide-goods" instances from the Spliddit database.
    Each instance is converted into a valuation matrix,
    in which the rows are the users and the columns are the resources.

    :return yields pairs (instance_id, valuation_matrix)
    """
    connection = sqlite3.connect(SPLIDDIT_DATABASE_FILE)
    instances_query = "select id from instances where application_id={} group by id having id>={}".format(application_id,first_id)
    for (instance_id,) in query_to_array(connection, instances_query):
        (agent_count, resource_count) = query_to_array(connection, "select count(distinct agent_id),count(distinct resource_id) from valuations where instance_id={}".format(instance_id))[0]
        valuation_list = query_to_array(connection, "select agent_id,resource_id,value from valuations where instance_id={}".format(instance_id))
        valuation_matrix = valuation_list_to_valuation_matrix(valuation_list, agent_count, resource_count)
        yield (instance_id, valuation_matrix)
    connection.close()


def spliddit_instance(instance_id:int):
    """
    Return a single valuation matrix representing a Spliddit instance.
    :return A valuation_matrix.
    """
    connection = sqlite3.connect(SPLIDDIT_DATABASE_FILE)
    application_ids = query_to_array(connection, "select application_id from instances where id={}".format(instance_id))
    if len(application_ids)==0:
        raise ValueError("Instance {} not found".format(instance_id))
    (application_id,) = application_ids[0]
    (agent_count, resource_count) = query_to_array(connection, "select count(distinct agent_id),count(distinct resource_id) from valuations where instance_id={}".format(instance_id))[0]
    valuation_list = query_to_array(connection, "select agent_id,resource_id,value from valuations where instance_id={}".format(instance_id))
    valuation_matrix = valuation_list_to_valuation_matrix(valuation_list, agent_count, resource_count)
    connection.close()
    if application_id==SPLIDDIT_GOODS:
        return valuation_matrix
    elif application_id==SPLIDDIT_TASKS:
        return -valuation_matrix
    else:
        raise ValueError("Invalid application_id "+str(application_id))





def query_to_array(connection, query:str):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()




def valuation_list_to_valuation_matrix(valuation_list:list, agent_count:int, resource_count:int):
    """
    Converts a valuation-list from the Spliddit database to a valuation-matrix for the algorithm.
    :param valuation_list: a list with triplets of the form:
       (agent_id, resource_id, value)
    :return:  valuation_matrix: a matrix where in each (row,col) there is the value of agent row to resource col.

    >>> valuation_list = [(5778, 5599, 80.0), (5778, 5600, 799.0), (5778, 5601, 121.0), (5779, 5599, 109.0), (5779, 5600, 732.0), (5779, 5601, 159.0)]
    >>> print(valuation_list_to_valuation_matrix(valuation_list, agent_count=2, resource_count=3))
    [[ 80. 799. 121.]
     [109. 732. 159.]]
    """
    current_agent_index = 0
    map_agentid_to_index = {}
    current_resource_index = 0
    map_resourceid_to_index = {}
    valuation_matrix = np.zeros((agent_count,resource_count))
    for (agentid, resourceid, value) in valuation_list:

        if agentid in map_agentid_to_index:
            agent_index = map_agentid_to_index[agentid]
        else:
            agent_index = current_agent_index
            current_agent_index += 1
            map_agentid_to_index[agentid] = agent_index

        if resourceid in map_resourceid_to_index:
            resource_index = map_resourceid_to_index[resourceid]
        else:
            resource_index = current_resource_index
            current_resource_index += 1
            map_resourceid_to_index[resourceid] = resource_index

        valuation_matrix[agent_index,resource_index] = value

    return valuation_matrix



if __name__=="__main__":
    connection = sqlite3.connect(SPLIDDIT_DATABASE_FILE)
    tables = query_to_array(connection, "select name from sqlite_master where type='table'")
    print("Tables: ", tables)
    print(query_to_array(connection, "select distinct(type) from instances"))
    print("Instances: ", list(spliddit_instances()))
