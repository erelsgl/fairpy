"""

Programmer: Ofec Israel

"""

import agents
from agents import PiecewiseLinearAgent
from agents import PiecewiseUniformAgent
from allocations import *
from random import shuffle
import logging
logger = logging.getLogger(__name__)
    



"""
Get the intersection of two intervals
"""
def intervals_intersection(a,b):
    intervals = []
    for i in a:
        for j in b:
            interval = (max(i[0], j[0]), min(i[1], j[1]))
            if(not interval[0]>=interval[1]):
                intervals.append(interval)
                
    return intervals

"""
Get first element
"""
def first_element(i):
    return i[0]

"""
Net implementation
"""
class Edge(object):
  def __init__(self, u, v, w):
    self.source = u
    self.target = v
    self.capacity = w

  def __repr__(self):
    return "%s->%s:%s" % (self.source, self.target, self.capacity)


class FlowNetwork(object):
  def  __init__(self):
    self.adj = {}
    self.flow = {}

  def AddVertex(self, vertex):
    self.adj[vertex] = []

  def GetEdges(self, v):
    return self.adj[v]

  def AddEdge(self, u, v, w = 0):
    if u == v:
      raise ValueError("u == v")
    edge = Edge(u, v, w)
    redge = Edge(v, u, 0)
    edge.redge = redge
    redge.redge = edge
    self.adj[u].append(edge)
    self.adj[v].append(redge)
    # Intialize all flows to zero
    self.flow[edge] = 0
    self.flow[redge] = 0
    
  def FindPath(self, source, target, path):
    if source == target:
      return path
    for edge in self.GetEdges(source):
      residual = edge.capacity - self.flow[edge]
      if residual > 0 and not (edge, residual) in path:
        result = self.FindPath(edge.target, target, path + [(edge, residual)])
        if result != None:
          return result

  def MaxFlow(self, source, target):
    path = self.FindPath(source, target, [])
    while path != None:
      flow = min(res for edge, res in path)
      for edge, res in path:
        self.flow[edge] += flow
        self.flow[edge.redge] -= flow
      path = self.FindPath(source, target, [])
    return sum(self.flow[edge] for edge in self.GetEdges(source))




"""
agents: list of PiecewiseLinearAgent
"""
def algorithm2(agents):
    """
    >>> a = PiecewiseLinearAgent([(0,0.39, 1,1)], "a")
    >>> b = PiecewiseLinearAgent([(0,0.6, 1,1)], "b")
    >>> c = PiecewiseLinearAgent([(0,0.1, 1,1)], "c")
    >>> agents = [a,b,c]
    
    >>> allocations = algorithm2(agents)
    
    >>> print(allocations)
    
    algorithm2
    > a gets [(0.0, 0.2), (1.0, 1.2000000000000002), (0.2, 0.3), (0.7, 0.7999999999999998)] with value 2.30
    > b gets [(0.2, 0.4), (0.8, 1.0), (0.3, 0.39999999999999997), (0.5999999999999999, 0.7)] with value 2.55
    """
    print("algorithm2")
    N = len(agents)
    logger.info("N is: %d", N)
    
    #organise the intervals
    intervals = []
    for agent in agents:
        regions = agent.desired_regions
        for region in regions:
            intervals.append((region[0],'start'))
            intervals.append((region[1],'end'))
    intervals = sorted(intervals, key = first_element)
    
    partitions = [[] for _ in range(N)]
    startCounter = 0
    lastPoint = None
    for i in intervals:
        if(lastPoint == None):
            lastPoint = i[0]
        if(startCounter > 0 and lastPoint != i[0]):
            for index in range(len(agents)):
                I = (i[0] - lastPoint) / 2*N
                
                partitions[index].append((lastPoint + I*index, lastPoint + (index+1)*I))
                partitions[index].append((lastPoint + (2*N-index+1)*I, lastPoint + (2*N-index+2)*I))

        if(i[1] == 'start'):
            startCounter += 1
        elif(i[1] == 'end'):
            startCounter -= 1
        lastPoint = i[0]
    
    #random match
    shuffle(partitions)
    
    #print(partitions)
    
    results = Allocation(agents)
    for i in range(N):
        results.set_piece(i, partitions[i])
        #results.append(('agent '+str(i), partitions[i]))
    return results

"""
agents: list of PiecewiseUniformAgent
cake: list of intervals
allocations: should be empty

called by algorithm1
"""
def algorithm1_recursive(agents, cake, allocations = {}):
    # all agents got their cake
    if not agents:
        logger.info("Done")
        return allocations
    
    #check for min avg
    minAvg = -1
    minSubGroup = []
    minUnion = []
    for i in range(len(agents) + 1):  
        for j in range(i + 1, len(agents) + 1): 
            # slice the subarray  
            sub = agents[i:j] 
            avg = 0
            union = []
            for s in sub:
                s_intervals = s.desired_regions
                s_intervals = intervals_intersection(cake, s_intervals)
                for begin,end in sorted(s_intervals):
                    if union and union[-1][1] >= begin - 1:
                        union[-1][1] = max(union[-1][1], end)
                    else:
                        union.append([begin, end])
            if(not union):
                continue
            avg = PiecewiseUniformAgent(union).cake_value()
            avg /= len(sub)
            if(minAvg == -1 or avg < minAvg):
                minAvg = avg
                minSubGroup = sub
                minUnion = union
          
    logger.info("Min Avg: %d", minAvg)
    
    l = []
    for s in minSubGroup:
        s_intervals = s.desired_regions
        s_intervals = intervals_intersection(cake, s_intervals)
        for i in s_intervals:
            l.append((i[0],'start',s))
            l.append((i[1],'end',s))
    
    l = sorted(l, key = first_element)

    agents_list = []
    intervals = []
    
    last_point = None
    for i in l:
        if last_point == None:
            last_point = i[0]
        if agents_list and last_point != i[0]:
            intervals.append((last_point, i[0], tuple(agents_list.copy())))
            
        if(i[1] == 'start'):
            agents_list.append(i[2])
        elif(i[1] == 'end'):
            agents_list.remove(i[2])
        last_point = i[0]
    
    #build graph from minSubGroup
    g = FlowNetwork()
    g.AddVertex('s')
    g.AddVertex('t')

    for i in minSubGroup:
        g.AddVertex(i)
        g.AddEdge(i, 't', minAvg)
        
    for i in intervals:
        g.AddVertex(i)
        g.AddEdge('s', i, i[1] - i[0])
        for j in i[2]:
            g.AddEdge(i, j, float("inf"))
    
    g.MaxFlow('s', 't')
    
    #add agents to allocations
    for s in minSubGroup:
        allocations[s] = []
    
    start_edges = g.GetEdges('s')
    for e in start_edges:
        interval_vertex = e.target
        interval_edges = g.GetEdges(interval_vertex)
        position = interval_vertex[0]
        for e2 in interval_edges:
            #not a real edge
            if(e2.capacity == 0):
                continue
            #allocate
            allocations[e2.target].append((position, position + g.flow[e2]))
            position = position + g.flow[e2]
            
    #update what's left from the cake
    points = []
    for i in minUnion:
        points.append((i[0], 'start', 'agent'))
        points.append((i[1], 'end', 'agent'))
    for i in cake:
        points.append((i[0], 'start', 'cake'))
        points.append((i[1], 'end', 'cake'))
    
    points = sorted(points, key = first_element)
    newCake = []
    lastStartCake = None
    inAgentsInterval = 0
    for p in points:
        if(p[2] == 'cake'):
            if(p[1] == 'start'):
                lastStartCake = p[0]
            elif(p[1] == 'end'):                
                if(lastStartCake != None and inAgentsInterval == 0):
                    newCake.append((lastStartCake, p[0]))
                lastStartCake = None
        if(p[2] == 'agent'):
            if(p[1] == 'start'):
                if(lastStartCake != None and inAgentsInterval == 0):
                    newCake.append((lastStartCake, p[0]))
                    lastStartCake = None
                inAgentsInterval += 1
            if(p[1] == 'end'):
                inAgentsInterval -= 1
                if(lastStartCake != None):
                    lastStartCake = p[0]
    
    #recurse
    algorithm1_recursive([item for item in agents if item not in minSubGroup], newCake, allocations)
    
    #make Allocation object
    result = Allocation(agents)
    for agent in allocations:
        if not agent in agents:
            return None
        result.set_piece(agents.index(agent), allocations[agent])

    return result


def algorithm1(agents):
    """"
    >>> a = PiecewiseUniformAgent([(0,0.39)], "a")
    >>> b = PiecewiseUniformAgent([(0,0.6)], "b")
    >>> c = PiecewiseUniformAgent([(0,0.1)], "c")
    >>> cake = [(0,1)]
    >>> agents = [a,b,c] 
    >>> allocations = algorithm1(agents, cake)
    >>> print(allocations)
    
    algorithm1
    > a gets [(0.1, 0.35)] with value 0.25
    > b gets [(0.35, 0.39), (0.39, 0.6)] with value 0.25
    > c gets [(0, 0.1)] with value 0.10
    
    """
    print("algorithm1")
    #get the cake
    min_cake = None
    max_cake = None
    for agent in agents:
        for region in agent.desired_regions:
            if min_cake == None:
                min_cake = region[0]
                max_cake = region[1]
                
            if min_cake > region[0]:
                min_cake = region[0]
            if max_cake < region[1]:
                max_cake = region[1]
        
    
    allocations = {}
    cake = [(min_cake,max_cake)]
    return algorithm1_recursive(agents, cake, allocations)
    
