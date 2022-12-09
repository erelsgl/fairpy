#!python3

from typing import List, Set, Optional, Tuple, Dict

from fairpy.agents import PiecewiseConstantAgent, Agent
from fairpy.cake.improve_ef4_algo.cake import CakeSlice
from fairpy.cake.improve_ef4_algo.util import exclude_from_list


class Marking(object):
    """
    Represents a marking-context. Stores information about marks made
    by agents.

    Allows making marks by different input, or querying information about those marks.
    Each mark is identified by a position and has associated agent, which made the mark,
    and an associated slice, which the mark was made on.
    """

    def __init__(self):
        self._slice_to_marks = {}

    def mark(self, agent: Agent, slice: CakeSlice, desired_value: float) -> float:
        """
        Adds a mark, made by `agent` on a given slice.
        :param agent: agent making the mark
        :param slice: slice to mark
        :param desired_value: satisfaction value wanted by agent, such that
            slice.start -> mark position = `desired_value.
        :return: mark position

        >>> s = CakeSlice(0, 2)
        >>> a = PiecewiseConstantAgent([33, 33], "agent")
        >>> m = Marking().mark(a, s, 33)
        >>> m
        1.0
        """
        position = agent.mark(slice.start, desired_value)

        if slice not in self._slice_to_marks:
            self._slice_to_marks[slice] = []
        self._slice_to_marks[slice].append((agent, position))

        return position

    def mark_to_equalize_value(self, agent: Agent, slice: CakeSlice, value_slice: CakeSlice) -> float:
        """
        Adds a mark, made by `agent` on a given slice, such that agent has the same satisfaction
        from slice.start -> mark position as they do with `value_slice`.
        :param agent: agent making the mark
        :param slice: slice to mark
        :param value_slice: comparision slice whose satisfaction value for agent indicates
            the wanted satisfaction value for agent out of the new marked slice
        :return: mark position.

        >>> s = CakeSlice(1, 2)
        >>> s2 = CakeSlice(0.5, 1)
        >>> a = PiecewiseConstantAgent([33, 33], "agent")
        >>> m = Marking().mark_to_equalize_value(a, s, s2)
        >>> m
        1.5
        """
        value = value_slice.value_according_to(agent)
        return self.mark(agent, slice, value)

    def marks_on_slice(self, slice: CakeSlice) -> List[Tuple[Agent, float]]:
        """
        Gets all the marks made on the given slice.
        :param slice: slice whose marks to return
        :return: list of marks made on `slice`, with each mark being a tuple of agent who made the
            mark and position of mark

        >>> s = CakeSlice(1, 2)
        >>> a = PiecewiseConstantAgent([33, 33], "agent")
        >>> marking = Marking()
        >>> m = marking.mark(a, s, 11)
        >>> m2 = marking.mark(a, s, 22)
        >>> all([mark in [(a,m),(a,m2)] for mark in marking.marks_on_slice(s)])
        True
        """
        return sorted([m for m in self._slice_to_marks[slice]], key=lambda m: m[1])

    def rightmost_marks_by_agents(self) -> Dict[Agent, List[CakeSlice]]:
        """
        Gets the rightmost marks on all the marked slices, which are the marks
        closes to the end of each slide. Grouped by agents who made the marks and the slices which were marked.
        
        :return: dictionary mapping agents to a lists of slices they marked.

        >>> s = CakeSlice(1, 2)
        >>> a = PiecewiseConstantAgent([33, 33], "agent")
        >>> a2 = PiecewiseConstantAgent([33, 33], "agent")
        >>> marking = Marking()
        >>> m = marking.mark(a, s, 11)
        >>> m2 = marking.mark(a2, s, 22)
        >>> len(marking.rightmost_marks_by_agents())
        1
        >>> list(marking.rightmost_marks_by_agents().keys())[0] == a2
        True
        """
        rightmost_marks = {}
        for slice, marks in self._slice_to_marks.items():
            if len(marks) == 0:
                continue
            rightmost_agent, rightmost = max(marks, key=lambda m: m[1])

            if rightmost_agent not in rightmost_marks:
                rightmost_marks[rightmost_agent] = []
            rightmost_marks[rightmost_agent].append(slice)

        return rightmost_marks

    def second_rightmost_mark(self, marked_slice: CakeSlice) -> Tuple[Agent, float]:
        """
        Gets the second rightmost mark on the given slice.
        :param marked_slice: slice to find the second rightmost mark on.
        :return: second rightmost mark on the given slice, as tuple of marking agent and position
        :throws ValueError: if there is only one mark on the given slice

        >>> s = CakeSlice(1, 2)
        >>> a = PiecewiseConstantAgent([33, 33], "agent")
        >>> marking = Marking()
        >>> m = marking.mark(a, s, 11)
        >>> m2 = marking.mark(a, s, 22)
        >>> marking.second_rightmost_mark(s) == (a, m)
        True
        """
        rightmost_marks = self.marks_on_slice(marked_slice)
        if len(rightmost_marks) < 2:
            raise ValueError("No second mark")
        return rightmost_marks[-2]


class CakeAllocation(object):
    """
    Represents allocations of cake slices to agents.

    This is the main supporting class for the algorithm, as it allows tracking the cake status,
    including what slices exist, and which slice is allocated to whom.

    Given a list of several slices, an instance of this looks at those slices as the entire cake,
    like it is a new cake which is untouched, making all slices 'complete' and unallocated.
    Throughout usage, an instance will keep track of what was done with its slices, i.e. who
    they were allocated to, were they cut and were they marked.
    """

    def __init__(self, all_slices: List[CakeSlice]):
        self._complete_slices = list(all_slices)
        self._all_slices = list(all_slices)
        self._slice_allocations = {}
        self._marking = Marking()

    def __repr__(self):
        return "Unallocated: \n\t{}\nAllocation \n\t{}".format('\n\t'.join([str(slice)
                                                                            for slice in self.unallocated_slices]),
                                                               '\n\t'.join(["{} -> {}".format(slice, agent.name())
                                                                            for slice, agent in
                                                                            self._slice_allocations.items()]))

    @property
    def marking(self):
        """
        Gets the marking context for this allocation.
        :return: the marking context.
        """
        return self._marking

    @property
    def all_slices(self) -> List[CakeSlice]:
        """
        Gets all the slices in this allocation.
        :return: all the slices.
        """
        return list(self._all_slices)

    @property
    def unallocated_slices(self) -> List[CakeSlice]:
        """
        Gets all the unallocated slices, i.e. the slices which haven't being
        given to an agent.
        :return: unallocated slices, by order of slice.start
        """
        return sorted([slice for slice in self._all_slices if slice not in self._slice_allocations],
                      key=lambda s: s.start)

    @property
    def free_complete_slices(self) -> List[CakeSlice]:
        """
        Gets all the unallocated slices which were not sliced in this allocation scope.
        :return: unallocated-unsliced slices.
        """
        return [slice for slice in self._complete_slices if slice not in self._slice_allocations]

    @property
    def partial_slices(self) -> List[CakeSlice]:
        """
        Gets all the slices which were sliced in this allocation scope.
        :return: unsliced slices.
        """
        return exclude_from_list(self._all_slices, self._complete_slices)

    @property
    def agents_with_allocations(self) -> Set[Agent]:
        """
        Gets all the agents who have received at least one slice in this allocation.
        :return agents with allocated slices.
        """
        return set(self._slice_allocations.values())

    def get_allocation_for_agent(self, agent: Agent) -> List[CakeSlice]:
        """
        Gets all the slices given to agent.
        :param agent: agent to get allocated slices for.
        :return: list with slices given to agent

        >>> s = CakeSlice(0, 1)
        >>> s2 = CakeSlice(1, 2)
        >>> a = PiecewiseConstantAgent([33, 33], "agent")
        >>> alloc = CakeAllocation([s, s2])
        >>> alloc.get_allocation_for_agent(a)
        []
        >>> alloc.allocate_slice(a, s)
        >>> alloc.get_allocation_for_agent(a)
        [(0,1)]
        """
        return [slice for slice, agent_with_slice in self._slice_allocations.items()
                if agent == agent_with_slice]

    def allocate_slice(self, agent: Agent, slice: CakeSlice):
        """
        Allocates `slice` to `agent`. If the slices is already allocated, it is transferred
        to the given agent. If the slice is split in this allocation, all the parts are allocated
        to `agent`.
        :param agent: agent to allocate to
        :param slice: slice to allocate
        :return: void

        >>> s = CakeSlice(0, 1)
        >>> s2 = CakeSlice(1, 2)
        >>> a = PiecewiseConstantAgent([33, 33], "agent")
        >>> alloc = CakeAllocation([s, s2])
        >>> alloc.allocate_slice(a, s)
        >>> alloc._slice_allocations[s].name()
        'agent'
        >>> alloc.allocate_slice(a, s2)
        >>> alloc._slice_allocations[s2].name()
        'agent'
        """
        slice_parts = []
        for s in self.all_slices:
            if slice.contains(s):
                slice_parts.append(s)

        for s in slice_parts:
            self._slice_allocations[s] = agent

    def set_slice_split(self, original_slice: CakeSlice, new_slices: List[CakeSlice]):
        """
        Updates the allocation slices that a slice was cut into multiple parts.
        :param original_slice: slice that was cut
        :param new_slices: slice parts
        :return: void
        :throws ValueError: if `original_slice` is allocated already

        >>> s = CakeSlice(0, 1)
        >>> alloc = CakeAllocation([s])
        >>> alloc.set_slice_split(s, [CakeSlice(0, 0.3), CakeSlice(0.3, 1)])
        >>> alloc.all_slices
        [(0,0.3), (0.3,1)]
        """
        if original_slice in self._slice_allocations:
            raise ValueError("cannot change allocated slice {}".format(original_slice))

        if original_slice in self._complete_slices:
            self._complete_slices.remove(original_slice)
        if original_slice in self._all_slices:
            self._all_slices.remove(original_slice)
        self._all_slices.extend(new_slices)

    def get_insignificant_slice(self, agent: Agent) -> CakeSlice:
        """
        Gets the insignificant slice out of all the allocated slices according to `agent`.
        Insignificant slice is defined as the slice which least satisfies `agent`.

        :param agent: agent whose insignificant slice to get
        :return: insignificant slice of agent

        >>> s = CakeSlice(0, 1)
        >>> s2 = CakeSlice(1, 1.5)
        >>> s3 = CakeSlice(1.5, 1.6)
        >>> a = PiecewiseConstantAgent([33, 33], "agent")
        >>> a2 = PiecewiseConstantAgent([33, 33], "agent2")
        >>> alloc = CakeAllocation([s, s2, s3])
        >>> alloc.allocate_slice(a, s)
        >>> alloc.allocate_slice(a, s2)
        >>> alloc.get_insignificant_slice(a)
        (1,1.5)
        >>> alloc.allocate_slice(a2, s3)
        >>> alloc.get_insignificant_slice(a)
        (1.5,1.6)
        """
        worst_slice = min(self._slice_allocations.keys(),
                          key=lambda s: s.value_according_to(agent))
        return worst_slice

    def try_get_agent_with_insignificant_slice(self) -> Optional[Agent]:
        """
        Tries to get the agent who was allocated the slice they
        consider to be the insignificant slice, as defined by `get_insignificant_slice`.

        :return: agent who was allocated their insignificant slice, or None if there
            is no such agent

        >>> s = CakeSlice(0, 1)
        >>> s2 = CakeSlice(1, 1.5)
        >>> s3 = CakeSlice(1.5, 1.6)
        >>> a = PiecewiseConstantAgent([33, 33], "agent")
        >>> a2 = PiecewiseConstantAgent([33, 33], "agent2")
        >>> alloc = CakeAllocation([s, s2, s3])
        >>> alloc.allocate_slice(a, s)
        >>> alloc.allocate_slice(a2, s2)
        >>> alloc.allocate_slice(a, s3)
        >>> alloc.try_get_agent_with_insignificant_slice().name()
        'agent'
        """
        for agent in self.agents_with_allocations:
            worst_slice = self.get_insignificant_slice(agent)
            if worst_slice in self._slice_allocations and \
                    self._slice_allocations[worst_slice] == agent:
                return agent

        return None

    def combine(self, allocation: 'CakeAllocation'):
        """
        Combines a given allocation into this one, modifying data about slices to match
        changes made in the given allocation.
        :param allocation: allocation to combine into this one
        :return: void

        >>> s = CakeSlice(0, 1)
        >>> s2 = CakeSlice(1, 1.5)
        >>> s3 = CakeSlice(1.5, 1.6)
        >>> s4 = CakeSlice(1.7, 1.8)
        >>> a = PiecewiseConstantAgent([33, 33], "agent")
        >>> a2 = PiecewiseConstantAgent([33, 33], "agent2")
        >>> alloc = CakeAllocation([s, s2, s3, s4])
        >>> alloc.allocate_slice(a, s)
        >>> len(alloc.agents_with_allocations)
        1
        >>> alloc.unallocated_slices
        [(1,1.5), (1.5,1.6), (1.7,1.8)]
        >>> alloc2 = CakeAllocation([s, s2, s3, s4])
        >>> alloc2.allocate_slice(a, s2)
        >>> alloc2.allocate_slice(a2, s3)
        >>> s41 = CakeSlice(1.7, 1.75)
        >>> s42 = CakeSlice(1.75, 1.8)
        >>> alloc2.set_slice_split(s4, [s41, s42])
        >>> alloc2.allocate_slice(a, s41)
        >>> alloc2.allocate_slice(a, s42)
        >>> alloc.combine(alloc2)
        >>> len(alloc.agents_with_allocations)
        2
        >>> alloc.unallocated_slices
        []
        >>> alloc.partial_slices
        [(1.7,1.75), (1.75,1.8)]
        """
        slice_partition = {}
        for slice in allocation.all_slices:
            complete_slice = self._try_get_complete_slice(slice)
            if complete_slice is None:
                continue

            if complete_slice not in slice_partition:
                slice_partition[complete_slice] = []
            slice_partition[complete_slice].append(slice)

        for complete_slice, pieces in slice_partition.items():
            if len(pieces) == 1:
                continue
            self.set_slice_split(complete_slice, pieces)

        for slice, agent in allocation._slice_allocations.items():
            self.allocate_slice(agent, slice)

        # combine unallocated slices
        slices_to_combine = []
        for slice in self.unallocated_slices:
            found = False
            for slice_list in slices_to_combine:
                for ss in slice_list:
                    if ss.start == slice.end or ss.end == slice.start:
                        slice_list.append(slice)
                        found = True
                        break
                if found:
                    break
            slices_to_combine.append([slice])
        self._combine_slices(slices_to_combine)

    def _try_get_complete_slice(self, slice: CakeSlice) -> Optional[CakeSlice]:
        """
        Tries to find a slice which the given `slice` is a part of.
        :param slice: partial slice to find the slice it is a part of
        :return: slice, the given slice, is a part of, or None if it was not found

        >>> s = CakeSlice(0, 1)
        >>> a = PiecewiseConstantAgent([33, 33], "agent")
        >>> a2 = PiecewiseConstantAgent([33, 33], "agent2")
        >>> alloc = CakeAllocation([s])
        >>> alloc._try_get_complete_slice(CakeSlice(0, 0.1))
        (0,1)
        >>> alloc._try_get_complete_slice(CakeSlice(0.5, 0.6))
        (0,1)
        >>> alloc._try_get_complete_slice(CakeSlice(0.8, 1))
        (0,1)
        >>> alloc._try_get_complete_slice(CakeSlice(1, 2))
        """
        for original_slice in self._all_slices:
            if original_slice.contains(slice):
                return original_slice
        return None

    def _combine_slices(self, slices_to_combine: List[List['CakeSlice']]):
        for slice_list in slices_to_combine:
            if len(slice_list) < 2:
                continue

            start = min(slice_list, key=lambda s: s.start).start
            end = max(slice_list, key=lambda s: s.end).end
            full_slice = CakeSlice(start, end)

            for s in slice_list:
                if s in self._all_slices:
                    self._all_slices.remove(s)
            self._all_slices.append(full_slice)


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
