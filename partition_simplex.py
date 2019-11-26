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

from agents import *
import matplotlib.pyplot as pyplot


class ColoredRegion:
    """
    Describes a region in the two-dimensional plane, that is colored by a single color.
    """
    def __init__(self, color, label, scale=100):
        self.color = color
        self.label = label
        self.scale = scale
        self.x = []
        self.y = []

    def addPoint(self, x, y):
        self.x.append(x)
        self.y.append(y)

    def plot(self, axes):
        axes.scatter(self.x, self.y, c=self.color, s=self.scale, label=self.label, edgecolors='none')


def plot_partition_simplex(agent:Agent, axes=None, samples_per_side:float=0.01):
    """
    Plot the partition-simplex of a given agent.
    The color of each point is determined by the piece that the agent wants in that partition:
    * blue  = leftmost piece;
    * red   = middle piece;

    * green = rightmost piece.
    :param agent: the agent for whom the simplex is plotted.
    :param axes:  pyplot axes object for plotting on. None to draw on the main axes.
    :param fractionStep: resolution for creating the simplex.
    :return:
    """
    length = agent.cake_length()
    step_length = length / samples_per_side
    scale = step_length*step_length*20000
    partitionsByBestPiece = [
        ColoredRegion('blue', "piece 1", scale),
        ColoredRegion('red',  "piece 2", scale),
        ColoredRegion('green',"piece 3", scale)]
    for cut1 in np.arange(0, length-step_length, step_length):
        for cut2 in np.arange(cut1, length-step_length, step_length):
            best_piece = np.argmax(agent.partition_values([cut1,cut2]))
            partitionsByBestPiece[best_piece].addPoint(cut1, cut2)

    if axes is None:
        axes = pyplot.axes()
    for p in partitionsByBestPiece:
        p.plot(axes)
    if axes==pyplot:
        axes = pyplot.axes()
    axes.set_title("val="+agent.name())
    # axes.set_aspect('equal', 'datalim')
    axes.set_xticks(np.arange(0, length+1, 1.0))
    axes.set_yticks(np.arange(0, length+1, 1.0))
