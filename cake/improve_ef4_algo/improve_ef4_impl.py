#!python3

import logging
from typing import *

from fairpy.agents import PiecewiseConstantAgent, Agent
from fairpy.cake.improve_ef4_algo.allocation import CakeAllocation
from fairpy.cake.improve_ef4_algo.cake import CakeSlice, full_cake_slice, slice_equally
from fairpy.cake.improve_ef4_algo.domination import get_most_satisfied_agent, get_least_satisfied_agent, is_dominated_by_all
from fairpy.cake.improve_ef4_algo.gain import allocation_with_lowest_gain, get_agent_gain
from fairpy.cake.improve_ef4_algo.marking import mark_by_preferences, allocate_by_rightmost_to_agent, allocate_all_partials_by_marks
from fairpy.cake.improve_ef4_algo.preference import find_favorite_slice, get_preferences_for_agents
from fairpy.cake.improve_ef4_algo.util import exclude_from_list


class Algorithm(object):

    def __init__(self, agents: List[Agent], logger: logging.Logger):
        self._agents = agents
        self._logger = logger

    def main(self) -> CakeAllocation:
        """
        Executes the "An Improved Envy-Free Cake Cutting Protocol for Four Agents" to allocate
        a cake to 4 agents.

        Runs the main protocol of the algorithm, which is divided into 3 phases.

        PHASE1
        Run `core` 4 times with the first agent (agent1) as the cutter.
        If for all those runs, the same agent was allocated their insignificant slice, `correction`
        is ran on the allocation where each agent gained the least.

        `core` is ran again with the first agent as the cutter.
        If cutter is the most satisfied agent, run the `Selfridge-Conway` protocol on the remaining slices for
        agents 2, 3, 4 (not the cutter), and return the result.
        Otherwise, define agent E as the most satisfied agent, run `core` with E as the cutter, excluding agent1
        from the competition phase of `core`.

        PHASE2
        define A as the least satisfied agent, and the other agents as B, C and D in order.
        Run `core` twice with D as the cutter, excluding the more satisfied out of B or C from the competition
        phase.

        If B and C are not both less satisfied then A and D, define F as on of B,C who received their
        insignificant slice in the last 2 runs `core`, and run `correction` on the allocation where
        the gain of F is smallest.

        PHASE3
        Run `cut_and_choose` on the cake remainder for B and C.

        :return: a `CakeAllocation` object with the allocation of the cake to the agents.
        """
        # full cake allocation
        cake = [full_cake_slice(self._agents)]
        total_allocation = CakeAllocation(cake)

        self._logger.info("Starting allocation on cake {} for agents {}".format(str(cake),
                                                                                ', '.join([agent.name() for agent in
                                                                                           self._agents])))

        self._logger.info("Starting phase1")
        # PHASE ONE
        active_agents = self._agents
        cutter = self._agents[0]
        all_allocations = []
        for i in range(4):
            # are these allocations permanent or are they simulated
            # residue = full cake? or remainder from last allocation
            allocation = self._core(cutter, total_allocation.unallocated_slices, active_agents)
            all_allocations.append(allocation)
            total_allocation.combine(allocation)

            if len(total_allocation.unallocated_slices) == 0:
                self._logger.info("All slices allocated, finished")
                return total_allocation

        agents_with_insignificant = list(filter(None, [
            allocation.try_get_agent_with_insignificant_slice()
            for allocation in all_allocations
        ]))
        if len(set(agents_with_insignificant)) == 1 and len(agents_with_insignificant) == 4:
            self._logger.info("{} received insignificant slice for 4 runs".format(agents_with_insignificant[0]))
            # same agent (agents_with_insignificant[0]) has insignificant slice
            # x(i) -> allocated slices for agent[i]
            # gain = sum of values of allocated slices to agent

            # gain(i) = (value of slice for agent i) - (value of slices other got)
            # find sub-allocation where the gain of agents (excluding cutter) is smallest
            low_gain_allocation = allocation_with_lowest_gain(self._agents[1:3], all_allocations)
            self._logger.info("allocation with lowest gain {}, running correction"
                              .format(all_allocations.index(low_gain_allocation)))
            self._correction(cutter, low_gain_allocation, total_allocation)

        self._logger.info("running core again")
        allocation = self._core(cutter, total_allocation.unallocated_slices, active_agents)
        total_allocation.combine(allocation)

        if len(total_allocation.unallocated_slices) == 0:
            self._logger.info("All slices allocated, finished")
            return total_allocation

        # dominated by === less satisfied than
        # dominates == more satisfied

        # if an agent is not dominated (E) by cutter
        # someone took agent1's preference at some point
        #   run core with not dominated agent (E) as cutter
        #   exclude original cutter from competition (from entire core, or just competition?)

        most_satisfied_agent = get_most_satisfied_agent(self._agents, total_allocation)
        if most_satisfied_agent != cutter:
            agent_e = most_satisfied_agent
            self._logger.info("most satisfied agent ({}) != agent1, running core".format(agent_e.name()))
            allocation = self._core(agent_e, total_allocation.unallocated_slices,
                                    active_agents, exclude_from_competition=cutter)
            total_allocation.combine(allocation)

            if len(total_allocation.unallocated_slices) == 0:
                self._logger.info("All slices allocated, finished")
                return total_allocation
        # else
        #   run "Selfridge-Conway protocol" (?) on residue for agents 2, 3, 4, and terminate
        else:
            self._logger.info("agent1 dominates, running selfridge_conway for other agents")
            allocation = self._selfridge_conway(self._agents[1:], total_allocation.unallocated_slices)
            total_allocation.combine(allocation)

            self._logger.info("finished, returning")
            return total_allocation

        # PHASE TWO
        # define A as dominated by B and C. D is the remaining
        agent_a = get_least_satisfied_agent(active_agents, total_allocation)
        others = exclude_from_list(active_agents, excluded=[agent_a])
        agent_b = others[0]
        agent_c = others[1]
        agent_d = others[2]

        self._logger.info("Starting phase2")

        all_allocations.clear()
        # line  11
        for i in range(2):
            # D = cutter
            # line 12
            # run core on residue and
            # exclude from competition any of {B,C} who dominates 2 non-cutters
            exclude = get_most_satisfied_agent([agent_b, agent_c], total_allocation)
            allocation = self._core(agent_d, total_allocation.unallocated_slices,
                                    self._agents, exclude_from_competition=exclude)
            all_allocations.append(allocation)
            total_allocation.combine(allocation)

            if len(total_allocation.unallocated_slices) == 0:
                self._logger.info("All slices allocated, finished")
                return total_allocation

        # if not (A and D are more satisfied than B, C)
        if not is_dominated_by_all(agent_b, [agent_a, agent_d], total_allocation) or \
                not is_dominated_by_all(agent_c, [agent_a, agent_d], total_allocation):
            self._logger.info("A and D not dominated both B and C")
            # if B,C not dominated by A,D
            # F is one of {B,C} which received the insignificant slice during runs in line 11
            # out of the two allocations in line 11, find the who where the gain of F is smaller
            # run correction on said allocation
            agents_with_insignificant = list(filter(None, [
                allocation.try_get_agent_with_insignificant_slice()
                for allocation in all_allocations
            ]))
            if set(agents_with_insignificant) != 1:
                raise ValueError("multiple agents with insignificant slice")
            agent_f = agents_with_insignificant[0]
            if agent_f not in [agent_b, agent_c]:
                raise ValueError("B,C should have insignificant")

            self._logger.info("{} has insignificant slice from last 2 runs".format(agent_f.name()))
            low_gain_allocation = min(all_allocations,
                                      key=lambda alloc: get_agent_gain(agent_f,
                                                                       exclude_from_list(self._agents, [agent_f]),
                                                                       alloc))
            self._logger.info("allocation with lowest gain {}, running correction"
                              .format(all_allocations.index(low_gain_allocation)))
            self._correction(agent_d, low_gain_allocation, total_allocation)

        # PHASE THREE
        # run CUT_AND_CHOOSE on residue for B,C
        self._logger.info("running cut and choose on {}, {}".format(agent_b.name(), agent_c.name()))
        allocation = self._cut_and_choose(agent_b, agent_c, total_allocation.unallocated_slices)
        total_allocation.combine(allocation)

        self._logger.info("finished")
        return total_allocation

    def _core(self, cutter: Agent, residue: List[CakeSlice], agents: List[Agent],
              exclude_from_competition: Agent = None) -> CakeAllocation:
        """
        Runs the core protocol of "An Improved Envy-Free Cake Cutting Protocol for Four Agents".

        Starts by having `cutter` cut the residue into 4 slices which they view as equal in value.
        The preferences of the other agents are then explored. Agents whose first preference is not
        conflicted with other agents receive their favorite slice.

        If all the agents received their favorite slice, return. Otherwise, we start the competition phase.

        For each of the non-cutter agents, we compare preferences.
        Agent who:
            - has not competition on the second preference, or
            - has 1 competition on the second preference, the competing agent also considers the slice as their second
            preference, and both have 1 competition for their first preference

        will make a "2-mark" on the first preference, which is a mark that makes the left part of the slice
        equal in value to the second preference.
        Other agents make a "3-mark" on the second preference, which is a mark that markes the left part of that
        preference equal in value to the third preference.

        Now allocate the slices by the rightmost rule:

        Find an agent which has made the rightmost mark on 2 slices. If one was found,
        out of those 2 slices, cut them until the second rightmost mark on each slice. Said
        agent will receive the preferred out of the two slices. The other slice is given to the
        agent who made the second rightmost mark on the slice taken by the previous agent.

        If there is no agent with rightmost marks on 2 slices, all the slices with marks are
        cut until the second rightmost mark, and each is allocated to the agent who made the rightmost mark.

        If any non-cutters remain that did not receive any slice yet, they are each given their preferred
        slice, out of the remaining uncut slices, in arbitrary order.

        Now the cutter is given the last unallocated complete slice, and the allocation
        of slices is returned.

        :param cutter: agent responsible for cutting
        :param residue: remaining slices of the cake
        :param agents: agents participating in the current allocation
        :param exclude_from_competition: agent to exclude from the competition stage.
        :return: an allocation of cake slices.

        >>> a = PiecewiseConstantAgent([10, 10, 10], "test1")
        >>> a2 = PiecewiseConstantAgent([10, 10, 10], "test2")
        >>> a3 = PiecewiseConstantAgent([10, 10, 10], "test3")
        >>> a4 = PiecewiseConstantAgent([10, 10, 10], "test4")
        >>> s = CakeSlice(0, 3)
        >>> algo = Algorithm([a, a2, a3, a4], logging.getLogger("test"))
        >>> alloc = algo._core(a, [s], [a2, a3, a4])
        >>> alloc.unallocated_slices
        []
        >>> sorted([agent.name() for agent in alloc.agents_with_allocations])
        ['test1', 'test2', 'test3', 'test4']
        >>> [alloc.get_allocation_for_agent(agent) for agent in [a, a2, a3, a4]]
        [[(2.25,3)], [(0.75,1.5)], [(0,0.75)], [(1.5,2.25)]]
        """
        active_agents = exclude_from_list(agents, [cutter])

        self._logger.info("Starting core with cutter {} and agents {} on residue {}".format(
            cutter.name(),
            ', '.join([agent.name() for agent in active_agents]),
            str(residue)
        ))

        # residue may not be a complete slice
        # cutter slices into 4
        slices = slice_equally(cutter, 4, residue)
        self._logger.info("Residue sliced into {}".format(str(slices)))

        preferences = get_preferences_for_agents(active_agents, slices)
        allocation = CakeAllocation(slices)

        satisfied_agents = []
        for agent in active_agents:
            preference = preferences.get_preference_for_agent(agent)

            favorite = preference[0]
            favorite_conflicts_first, _ = preferences \
                .find_agents_with_preference_for(favorite,
                                                 exclude_agents=[agent, exclude_from_competition])

            # line 8 if, not talking about lack of conflict for primary slice...
            if len(favorite_conflicts_first) == 0:
                allocation.allocate_slice(agent, favorite)
                satisfied_agents.append(agent)
                self._logger.info("{} has preference {} with no conflicts, allocating".format(agent.name(), favorite))
            else:
                self._logger.info("{} has preference {} with conflicts, not allocating".format(agent.name(), favorite))

        for agent in satisfied_agents:
            active_agents.remove(agent)

        if len(active_agents) == 0:
            self._logger.info(
                "all agents satisfied, allocating {} to cutter {}".format(str(allocation.free_complete_slices[0]),
                                                                          cutter.name()))
            allocation.allocate_slice(cutter, allocation.free_complete_slices[0])

            self._logger.info("core finished with {}".format(
                ', '.join("{}: {}".format(agent.name(), str(allocation.get_allocation_for_agent(agent)))
                          for agent in allocation.agents_with_allocations)
            ))
            return allocation

        # Conflict

        # do marking
        exclude = list(satisfied_agents)
        exclude.append(exclude_from_competition)
        self._logger.info("Starting conflict handling, excluding {}".format(', '.join(
            [agent.name() for agent in filter(None, exclude)])))

        for agent in exclude_from_list(active_agents, [exclude_from_competition]):
            slice, mark = mark_by_preferences(agent, preferences, allocation.marking, exclude)
            self._logger.info("{} made mark at {} on slice {}".format(agent.name(),
                                                                      str(mark), str(slice)))

        # Allocate by rightmost rule
        self._logger.info("Starting allocation by rightmost rule")

        agents_to_rightmost_marked_slices = allocation.marking.rightmost_marks_by_agents()

        allocated = False
        for agent, slices in agents_to_rightmost_marked_slices.items():
            if len(slices) != 2:
                continue
            self._logger.info("{} has rightmost mark on 2 slices {}".format(agent.name(), str(slices)))

            agents_to_allocated, sliced = allocate_by_rightmost_to_agent(agent, slices, allocation, allocation.marking)

            self._logger.info("slices cut into {}".format(str(sliced)))
            self._logger.info("allocated {}".format(', '.join([
                '{}: {}'.format(agent.name(), str(slice))
                for agent, slice in agents_to_allocated.items()
            ])))
            allocated = True
            break

        if not allocated:
            self._logger.info("No agent with rightmost mark on 2 slices")
            agents_to_allocated, sliced = allocate_all_partials_by_marks(allocation, allocation.marking)
            self._logger.info("slices cut into {}".format(str(sliced)))
            self._logger.info("allocated {}".format(', '.join([
                '{}: {}'.format(agent.name(), str(slice))
                for agent, slice in agents_to_allocated.items()
            ])))

        # if any non-cutters not given any slices
        #   each should choose favorite un-allocated complete slice
        for agent in exclude_from_list(active_agents, [exclude_from_competition]):
            if agent not in allocation.agents_with_allocations:
                favorite = find_favorite_slice(agent, allocation.free_complete_slices)
                allocation.allocate_slice(agent, favorite)

                self._logger.info("{} has not received slice yet, chose and received {}"
                                  .format(agent.name(), str(favorite)))

        # cutter given remaining un-allocated complete slice
        self._logger.info("cutter receives {}".format(str(allocation.free_complete_slices[0])))
        allocation.allocate_slice(cutter, allocation.free_complete_slices[0])

        self._logger.info("core finished with {}".format(
            ', '.join("{}: {}".format(agent.name(), str(allocation.get_allocation_for_agent(agent)))
                      for agent in allocation.agents_with_allocations)
        ))
        return allocation

    def _correction(self, cutter: Agent, allocation: CakeAllocation, total_allocation: CakeAllocation):
        """
        Runs the correction protocol of "An Improved Envy-Free Cake Cutting Protocol for Four Agents".

        Define A and B as the agents who made 2 marks on the allocated insignificant slice, where
        A is the one who received that allocation.
        Transfer the slice to B.

        If there are no more partial slices (other than the insignificant slice), agents
        C, A and D are allocated their favorite slices out of all the slices in the allocation,
        in order.

        Otherwise if there is another partial slice, let E be the agent who made the rightmost mark on
        it other than B.
        Allocate that slice to E.

        The remaining non-cutter chooses their favorite out of the 2 remaining slices and receives it.
        The cutter receives the last slice.

        :param cutter: cutter of the allocation to fix
        :param allocation: allocation to fix
        :param total_allocation: the complete state of the cake
        :return: void

        >>> a = PiecewiseConstantAgent([10, 10, 10], "test1")
        >>> a2 = PiecewiseConstantAgent([10, 10, 10], "test2")
        >>> a3 = PiecewiseConstantAgent([10, 10, 10], "test3")
        >>> a4 = PiecewiseConstantAgent([10, 10, 10], "test4")
        >>> s = CakeSlice(0,0.75)
        >>> s2 = CakeSlice(0.75,1.5)
        >>> s3 = CakeSlice(1.5,2)
        >>> s4 = CakeSlice(2,2.25)
        >>> s5 = CakeSlice(2.25,3)
        >>> algo = Algorithm([a, a2, a3, a4, s5], logging.getLogger("test"))
        >>> alloc = CakeAllocation([s, s2, s3, s4, s5])
        >>> alloc.allocate_slice(a, s)
        >>> alloc.allocate_slice(a2, s2)
        >>> alloc.allocate_slice(a3, s3)
        >>> alloc.allocate_slice(a4, s4)
        >>> sorted([agent.name() for agent in alloc.agents_with_allocations])
        ['test1', 'test2', 'test3', 'test4']
        >>> m = alloc.marking.mark(a3, s4, 2)
        >>> m = alloc.marking.mark(a3, s4, 1)
        >>> algo._correction(s, alloc, alloc)
        >>> alloc.unallocated_slices
        [(2.25,3)]
        >>> sorted([agent.name() for agent in alloc.agents_with_allocations])
        ['test2', 'test3']
        >>> [alloc.get_allocation_for_agent(agent) for agent in [a, a2, a3, a4]]
        [[], [(0,0.75), (0.75,1.5)], [(1.5,2), (2,2.25)], []]
        """
        agent_with_insignificant = allocation.try_get_agent_with_insignificant_slice()
        insignificant_slice = allocation.get_insignificant_slice(agent_with_insignificant)
        marks = allocation.marking.marks_on_slice(insignificant_slice)

        self._logger.info("{} has insignificant {}, with marks {}".format(agent_with_insignificant.name(),
                                                                          str(insignificant_slice),
                                                                          str([mark[1] for mark in marks])))
        if len(marks) != 2:
            raise ValueError("Slice should have 2 marks")
        # find insignificant slice
        # A, B agents who marked that slice
        # B is allocated the slice

        agent_a = agent_with_insignificant
        agent_b = [mark[0] for mark in marks if mark[0] != agent_a][0]

        self._logger.info("{} is allocated insignificant".format(agent_b.name()))

        total_allocation.allocate_slice(agent_b, insignificant_slice)

        remaining_agents = exclude_from_list(self._agents, [agent_a, agent_b])
        agent_c = remaining_agents[0]
        agent_d = remaining_agents[1]
        # if no other slice is marked
        #   agents choose fav by C, A, D
        # only the insignificant slice remains
        if len(allocation.partial_slices) <= 1:
            self._logger.info("no other partial slices")
            for agent in [agent_c, agent_a, agent_d]:
                if len(allocation.all_slices) > 0:
                    favorite = find_favorite_slice(agent, allocation.all_slices)
                    total_allocation.allocate_slice(agent, favorite)
                    self._logger.info("{} choose and received {}".format(agent.name(), str(favorite)))

            self._logger.info("correction finished with {}".format(
                ', '.join("{}: {}".format(agent.name(), str(allocation.get_allocation_for_agent(agent)))
                          for agent in allocation.agents_with_allocations)
            ))
        # else
        #   find rightmost mark not made by B on the other partial piece
        #   E = agent who made it
        #   E is allocated partial piece
        #   last non-cutter chooses their favorite among 2 complete slices
        #   the cutter is allocated the remaining piece
        else:
            other_slice = exclude_from_list(allocation.partial_slices, [insignificant_slice])[0]
            self._logger.info("{} is the other partial slice")

            agent_e, mark_made = [(agent, mark) for agent, mark in allocation.marking.marks_on_slice(other_slice)
                                  if agent != agent_b][0]
            self._logger.info(
                "{} made mark {} on slice and receives it".format(agent_e.name(), str(mark_made)))
            total_allocation.allocate_slice(agent_e, other_slice)

            last_non_cutter = exclude_from_list(self._agents, [cutter, agent_e, agent_b])[0]
            favorite = find_favorite_slice(last_non_cutter[0], allocation.free_complete_slices)
            self._logger.info("{} last non cutter choose and received {}".format(last_non_cutter.name, str(favorite)))
            total_allocation.allocate_slice(last_non_cutter, favorite)

            self._logger.info("{} (cutter) receives {}".format(cutter.name(), str(allocation.free_complete_slices[0])))
            total_allocation.allocate_slice(cutter, allocation.free_complete_slices[0])

            self._logger.info("correction finished with {}".format(
                ', '.join("{}: {}".format(agent.name(), str(allocation.get_allocation_for_agent(agent)))
                          for agent in allocation.agents_with_allocations)
            ))

    def _selfridge_conway(self, agents, residue: List[CakeSlice]) -> CakeAllocation:
        """
        Implements the Selfridge-Conway on the given agents and the cake residue, returning
        an allocation of slices.
        :param agents: agents to allocate among
        :param residue: residue to allocate
        :return: allocation of the residue.
        """
        p1 = agents[0]
        p2 = agents[1]
        p3 = agents[2]
        allocation = CakeAllocation(slice_equally(p1, 3, residue))

        p2_slices_order = sorted(allocation.all_slices, key=lambda s: s.value_according_to(p2), reverse=True)
        # if p2 thinks the two largest slices are equal in value, allocation preferred by order p3,p2,p1
        if abs(p2_slices_order[0].value_according_to(p2) - p2_slices_order[1].value_according_to(p2)) < 0.001:
            for agent in [p3, p2, p1]:
                favorite = find_favorite_slice(agent, allocation.unallocated_slices)
                allocation.allocate_slice(agent, favorite)

            return allocation

        # cut largest slice into 2, so that one part will be equal to the second largest
        slice_a = p2_slices_order[0]
        slice_b = p2_slices_order[1]
        slice_c = p2_slices_order[2]
        trimmings = slice_a.slice_to_value(p2, p2_slices_order[1].value_according_to(p2))
        slice_a1 = trimmings[0]
        slice_a2 = trimmings[1]
        allocation.set_slice_split(slice_a, trimmings)

        # p3 chooses among the large slices
        large_slices = [slice_a1, slice_b, slice_c]
        favorite = find_favorite_slice(p3, large_slices)
        allocation.allocate_slice(p3, favorite)
        large_slices.remove(favorite)

        # p2 chooses among the large slices
        # if a1 was not chosen by p3, p2 must choose a1
        if slice_a1 != favorite:
            agent_pa = p2
            agent_pb = p3
            allocation.allocate_slice(p2, slice_a1)
            large_slices.remove(slice_a1)
        else:
            agent_pa = p3
            agent_pb = p2
            favorite = find_favorite_slice(p2, large_slices)
            allocation.allocate_slice(p2, favorite)
            large_slices.remove(favorite)

        # p1 gets the last large slice
        allocation.allocate_slice(p1, large_slices.pop())

        # pb slices a2 into 3 parts
        a2_sliced_parts = slice_a2.slice_equally(agent_pb, 3)
        # agent choose slices in order pa, p1, pb
        for agent in [agent_pa, p1, agent_pb]:
            favorite = find_favorite_slice(agent, a2_sliced_parts)
            allocation.allocate_slice(agent, favorite)

        return allocation

    def _cut_and_choose(self, agent_a: Agent, agent_b: Agent, slices: List[CakeSlice]) -> CakeAllocation:
        """
        Implements the Cut-and-Choose protocol on the given agents and the cake residue, returning
        an allocation of slices.

        This is an adapted implementation of `fairpy`'s `cut_and_choose.asymmetric_protocol`, modified to work with a
        cake residue and to match the helper classes used here. This was chosen over using `fairpy`'s implementation
        due to it working with a full cake rather than a residue, which impacts allocation as agents produce
        different satisfaction values based on the cake area. This is farther amplified by the small size of the residue
        which is left by the time this method is used in the algorithm (near the end).
        Thus making `cut_and_choose.asymmetric_protocol` incompatible with our requirements.

        :param agent_a: agent 1 to allocate to
        :param agent_b: agent 2 to allocate to
        :param slices: residue slices of the cake
        :return: allocation of the residue.
        """
        allocation = CakeAllocation(slices)
        for slice in slices:
            mark_a = allocation.marking.mark(agent_a, slice, slice.value_according_to(agent_a) / 2)
            mark_b = allocation.marking.mark(agent_b, slice, slice.value_according_to(agent_b) / 2)

            if abs(mark_a.mark_position - mark_b.mark_position) < 0.0001:
                sliced = slice.slice_equally(agent_a, 2)
                allocation.set_slice_split(slice, sliced)
                allocation.allocate_slice(agent_a, sliced[0])
                allocation.allocate_slice(agent_b, sliced[1])
            else:
                cut_position = (mark_a.mark_position + mark_b.mark_position) / 2
                sliced = slice.slice_at(cut_position)
                allocation.set_slice_split(slice, sliced)

                if mark_a.mark_position < mark_b.mark_position:
                    allocation.allocate_slice(agent_a, sliced[0])
                    allocation.allocate_slice(agent_b, sliced[1])
                else:
                    allocation.allocate_slice(agent_a, sliced[1])
                    allocation.allocate_slice(agent_b, sliced[0])

        return allocation


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
