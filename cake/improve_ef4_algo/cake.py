#!python3

from typing import *

from fairpy.agents import Agent, PiecewiseConstantAgent


class CakeSlice(object):
    """
    Represents a slice of cake. Can be anywhere between the full cake,
    to 1/20 or smaller out of the full cake.

    The slice is represented on a number axis from 0 until an unspecified limit.
    Where `slice.start` is always smaller than `slice.end`.
    Thus, several slices can be seen as a continuation of one-another when `slice1.end == slice2.start`.
    """

    def __init__(self, start, end):
        self._start = start
        self._end = end

    @property
    def start(self) -> float:
        """
        Gets the start position of this slice, along the entire cake.
        :return: start position
        """
        return self._start

    @property
    def end(self) -> float:
        """
        Gets the end position of this slice, along the entire cake.
        :return: end position
        """
        return self._end

    @property
    def size(self) -> float:
        """
        Gets the size of this slice. Can be described as `slice.end` - `slice.start`.
        :return: size of this slice
        """
        return self._end - self._start

    def __repr__(self):
        return "({},{})".format(self._start, self._end)

    def slice_at(self, position: float) -> List['CakeSlice']:
        """
        Slice this into 2 parts at the given position, where slice.start < position < slice.end.

        :param position: position where to slice the cake in 2.
        :return: list containing the new slices, by order [(slice.start, position), (position, slice.end)].
            if position is at slice.start, or slice.end, a list containing this slice.

        >>> s = CakeSlice(0, 3)
        >>> s.slice_at(1.5)
        [(0,1.5), (1.5,3)]
        >>> s = CakeSlice(0, 1)
        >>> s.slice_at(0.9)
        [(0,0.9), (0.9,1)]
        >>> s = CakeSlice(0, 0.5)
        >>> s.slice_at(0.49999999999)
        [(0,0.5)]
        """
        if abs(position - self.start) < 0.00001 or abs(position - self.end) < 0.00001:
            return [self]

        first_slice = self._create_slice_part(self.start, position)
        second_slice = self._create_slice_part(position, self.end)

        return [first_slice, second_slice]

    def slice_equally(self, cutter: Agent, amount: int) -> List['CakeSlice']:
        """
        Slices this slice into several parts equal in value according to the cutter.

        :param cutter: cutter of the slices, determines the value for each slice
        :param amount: amount of parts to slice into
        :return: list containing `amount` slices, each equal in value according to
            `cutter`.

        >>> s = CakeSlice(0, 1)
        >>> a = PiecewiseConstantAgent([1, 3, 11], "agent")
        >>> s.slice_equally(a, 2)
        [(0,0.5), (0.5,1)]
        >>> s = CakeSlice(0, 1)
        >>> a = PiecewiseConstantAgent([1, 3, 11], "agent")
        >>> s.slice_equally(a, 4)
        [(0,0.25), (0.25,0.5), (0.5,0.75), (0.75,1)]
        """

        slices = []
        slice_value = cutter.eval(self.start, self.end) / amount
        last_start = self._start

        for i in range(amount - 1):
            end = cutter.mark(last_start, slice_value)
            slices.append(self._create_slice_part(last_start, end))
            last_start = end

        slices.append(self._create_slice_part(last_start, self.end))

        return slices

    def slice_to_value(self, cutter: Agent, value: float) -> List['CakeSlice']:
        """
        Slice this such that each part will equal a given value.
        :param cutter: cutter of the cake, based on whom the cake parts are
            evaluated.
        :param value: value for one part to equal
        :return: a list containing the new slices

        >>> a = PiecewiseConstantAgent([11, 33, 11], "agent")
        >>> s = CakeSlice(0, a.cake_length())
        >>> len(s.slice_to_value(a, a.total_value() / 10))
        10
        >>> a = PiecewiseConstantAgent([55, 3, 11], "agent")
        >>> s = CakeSlice(0, a.cake_length())
        >>> len(s.slice_to_value(a, a.total_value() / 2))
        2
        >>> a = PiecewiseConstantAgent([1, 3, 11], "agent")
        >>> s = CakeSlice(0, 1)
        >>> s.slice_to_value(a, a.eval(0, 1) / 2)
        [(0,0.5), (0.5,1)]
        """
        amount = int(cutter.eval(self.start, self.end) / value)
        return self.slice_equally(cutter, amount)

    def contains(self, slice: 'CakeSlice') -> bool:
        """
        Gets whether or not the given slice is part of this slice. In other words,
        if `slice.start >= self.start and slice.end <= self.end`.

        :param slice: slice to check if is part of this
        :return: true if `slice` is part of this, `false` otherwise.

        >>> s = CakeSlice(0, 1)
        >>> s2 = CakeSlice(0, 1)
        >>> s.contains(s2)
        True
        >>> s = CakeSlice(0, 1)
        >>> s2 = CakeSlice(0, 0.5)
        >>> s.contains(s2)
        True
        >>> s = CakeSlice(0.1, 1)
        >>> s2 = CakeSlice(0, 1)
        >>> s.contains(s2)
        False
        >>> s = CakeSlice(0, 1)
        >>> s2 = CakeSlice(0.5, 0.6)
        >>> s.contains(s2)
        True
        >>> s = CakeSlice(2, 3)
        >>> s2 = CakeSlice(0, 1)
        >>> s.contains(s2)
        False
        """
        return slice.start >= self.start and slice.end <= self.end

    def value_according_to(self, agent: Agent) -> float:
        """
        Gets the value assigned to this cake, according the an agent. This value
        represents how much an agent is interested in this slice.

        >>> a = PiecewiseConstantAgent([33, 3, 0.1], "agent")
        >>> s = CakeSlice(0, a.cake_length())
        >>> s.value_according_to(a) == a.total_value()
        True
        >>> a = PiecewiseConstantAgent([33, 33, 11], "agent")
        >>> s = CakeSlice(0, a.cake_length())
        >>> s.value_according_to(a) == a.total_value()
        True
        """
        return agent.eval(self.start, self.end)

    def _create_slice_part(self, start, end) -> 'CakeSlice':
        return CakeSlice(start, end)


def full_cake_slice(agents: List[Agent]) -> CakeSlice:
    """
    Returns the full cake to be divided among the given agents.

    :param agents: all the agents participating in the division
    :return: full cake slice

    >>> a = PiecewiseConstantAgent([33, 33, 11], "agent")
    >>> s = full_cake_slice([a])
    >>> s.size == a.cake_length()
    True
    >>> a = PiecewiseConstantAgent([33, 33, 11], "agent")
    >>> a2 = PiecewiseConstantAgent([1.1, 33], "agent")
    >>> s = full_cake_slice([a, a2])
    >>> s.size
    3
    """
    cake_size = max([agent.cake_length() for agent in agents])
    return CakeSlice(0, cake_size)


def slice_equally(cutter: Agent, amount: int, slices: List[CakeSlice]) -> List[CakeSlice]:
    """
    Slices the given slices into the given amount, so that each slice will be as equal
    as possible in terms of value for cutter (as described by CakeSlice.value_according_to)

    :param cutter: agent who performs the cutting
    :param amount: amount of equal-value slices to cut into
    :param slices: slices to cut to `amount`
    :return: list containing the modified slices, the size of the list might not be `amount`,
    as depending by the size and amount of given slices.

    >>> a = PiecewiseConstantAgent([11, 11, 11], "agent")
    >>> s = [CakeSlice(0, 1)]
    >>> slice_equally(a, 2, s)
    [(0,0.5), (0.5,1)]
    >>> a = PiecewiseConstantAgent([11, 11, 11], "agent")
    >>> s = [CakeSlice(0, 1), CakeSlice(0, 1)]
    >>> slice_equally(a, 2, s)
    [(0,1), (0,1)]
    """
    output = []
    average_value = sum([slice.value_according_to(cutter) for slice in slices]) / amount
    for slice in slices:
        if slice.value_according_to(cutter) <= average_value:
            output.append(slice)
            continue

        sliced = slice.slice_to_value(cutter, average_value)
        output.extend(sliced)

    return output


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
