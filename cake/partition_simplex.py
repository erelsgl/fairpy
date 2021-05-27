#!python3

"""
Demonstration of the simplex of partitions.

References:

    Walter Stromquist (1980):
    "How to cut a cake fairly."
    The American mathematical monthly, 87(8), 640-644.

    Francis Edward Su (1999):
    "Rental harmony: Sperner's lemma in fair division."
    The American mathematical monthly, 106(10), 930-942.

Programmer: Erel Segal-Halevi
Since: 2019-11
"""

from fairpy.agents import *

import matplotlib.pyplot as pyplot
import time, logging
logger = logging.getLogger(__name__)

class ColorMap:
    """
    Represents a map (usually of a triangle) in which each point (x,y) has a certain color (c).
    """
    def __init__(self, length: float):
        self.x_values = []
        self.y_values = []
        self.c_values = []  # maps each point-index to the color of that point
        self.length = length

    def add(self, x, y, c):
        self.x_values.append(x)
        self.y_values.append(y)
        self.c_values.append(c)

    def plot(self, axes, title, scale):
        if axes is None:
            axes = pyplot.axes()
        axes.scatter(self.x_values, self.y_values, c=self.c_values, s=scale, edgecolors=None)
        if axes == pyplot:
            axes = pyplot.axes()
        axes.set_title(title)
        axes.set_xticks(np.arange(0, self.length + 1, 1.0))
        axes.set_yticks(np.arange(0, self.length + 1, 1.0))


def plot_1_agent(agent:Agent, axes=None, samples_per_side:float=0.01):
    """
    Plot the partition-simplex of a given agent.
    The color of each point is determined by the piece that the agent wants in that partition:
    * red   = leftmost piece;
    * green = middle piece.
    * blue  = rightmost piece;

    :param agent: the agent for whom the simplex is plotted.
    :param axes:  pyplot axes object for plotting on. None to draw on the main axes.
    :param fractionStep: resolution for creating the simplex.
    :return:
    """
    length = agent.cake_length()
    step_length = length / samples_per_side
    map_best_piece_index_to_color = ['red', 'green', 'blue']
    start_time = time.time()
    colormap = ColorMap(length)
    for cut1 in np.arange(0, length-step_length, step_length):
        for cut2 in np.arange(cut1, length-step_length, step_length):
            best_piece = np.argmax(agent.partition_values([cut1,cut2]))
            colormap.add(cut1, cut2, map_best_piece_index_to_color[best_piece])
    logger.info("Color map created in %f seconds", (time.time()-start_time))

    scale = step_length*step_length*20000
    colormap.plot(axes, "Agent: " + agent.name(), scale)



def plot_many_agents(agents:List[Agent], axes=None, samples_per_side:float=0.01):
    """
    Plot the partition-simplexex of several different agents, overlayed one above the other.
    The color of each point is determined by the piece that each agent wants in that partition:
    * red   = leftmost piece;
    * green = middle piece.
    * blue  = rightmost piece;

    :param agent: the agent for whom the simplex is plotted.
    :param axes:  pyplot axes object for plotting on. None to draw on the main axes.
    :param fractionStep: resolution for creating the simplex.
    :return:
    """
    length = max([agent.cake_length() for agent in agents])
    step_length = length / samples_per_side
    num_of_agents = len(agents)
    color_step_per_agent = 1 / num_of_agents
    start_time = time.time()
    colormap = ColorMap(length)
    for cut1 in np.arange(0, length-step_length, step_length):
        for cut2 in np.arange(cut1, length-step_length, step_length):
            color = [0,0,0]
            for agent in agents:
                best_piece = np.argmax(agent.partition_values([cut1,cut2]))
                color[best_piece] += color_step_per_agent
            colormap.add(cut1, cut2, color)
    logger.info("Color map created in %f seconds", (time.time()-start_time))

    scale = step_length*step_length*20000
    # colormap.plot(axes, "Agents: {}".format([agent.name() for agent in agents]), scale)
    colormap.plot(axes, "{} agents".format(num_of_agents), scale)


