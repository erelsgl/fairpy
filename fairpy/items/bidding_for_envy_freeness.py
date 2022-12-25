'''
An implementation of the bidding for envy freeness procedure.
This is a procedure for finding an efficient envy-free allocation of n bundles of items to n agents.

Reference:
    Claus-Jochen Haake, Matthias G. Raith and Francis Edward Su (2002).
    ["An implementation of the bidding for envy freeness: A procedural approach to n-player fair-division problems"](https://scholarship.claremont.edu/cgi/viewcontent.cgi?article=1676&context=hmc_fac_pub).
    Social Choice and Welfare.
    
Programmers: Barak Amram, Adi Dahari
Since: 2022-12
'''

import sys
from itertools import permutations
import pandas as pd
from fairpy.items.valuations import ValuationMatrix
import logging
import pprint

INF = float('inf')

logger = logging.getLogger(__name__)


class BiddingForEnvyFreeness:

    def __init__(self, matrix: ValuationMatrix):
        '''
        This init function initializes the algorithm, by the following steps:
            1. Find the best option (M, C) and the best option index.
            2. Find the M - C value.
            3. Find the best option list.
            4. Evaluate the bidding matrix.
            5. Calculate the discounts step by step.
        '''
        logger.info('Bidding for Envy Freeness')
        logger.info(f'Initial Bidding Matrix: \n{pprint.pformat(matrix)}')
        self.dct = dict()
        self.m, self.c, self.best = self.find_m_c_best(matrix)
        logger.debug(
            f'best: option {self.best} --- {self.players_options[self.best]}')
        logger.debug(f'C: {self.c}')
        logger.debug(f'M: {self.m}')
        self.MC = self.m - self.c
        logger.debug(f'M - C: {self.MC}')
        opt = list(self.players_options[self.best])
        self.bundle_allocation = {i + 1: opt[i] for i in range(len(opt))}
        logger.debug(f'best opt: {opt}')
        self.options_list = self.player_package(opt)
        logger.debug(self.options_list)
        self.table = self.bidding_to_envy(matrix, opt)
        self.res = self.calculate_discounts(2)
        self.calculated_discounts = {
            p: self.res[p] for p in self.res.keys()}
        self.final_result = {f'Player {p}': {
            'Allocated Bundle': self.bundle_allocation[p],
            'Discount': self.calculated_discounts[p]
        } for p in self.bundle_allocation}
        logger.info(
            f'Envy Free Allocation: \n{pprint.pformat(self.final_result)}')

    def __str__(self):
        return f'{self.dct}'

    def make_list(self, values: ValuationMatrix, players_options: list):
        '''
        This function makes a list of the total values of the bundles allocated to each agent.
        '''
        res = []
        for i in range(0, len(players_options)):
            sum = 0
            for j in range(0, values.num_of_agents):
                sum += values[players_options[i][j]][j]
            res.append(sum)
        return res

    def best_option(self, options: list):
        '''
        This function finds the best option and its index.

        '''
        best = -1
        m = -INF
        for i in range(0, len(options)):
            if m < options[i]:
                m, best = options[i], i
        return best, m

    def switch_row_column(self, matrix: list):
        '''
        This function switches the rows and columns of the matrix.
        '''
        return pd.DataFrame(data=matrix)

    def find_m_c_best(self, matrix: ValuationMatrix) -> tuple:
        '''
        This function intitalizes the algorithm M and C values,
        Where:
            - M stands for the total value of initially invested amount of money by each agent, for the bundle of items allocated to him.
            - C stands for the minimum total biddings of a single agent for all available bundles.
            - best stands for the best option index.

        For Example:
        For the following matrix: (Bi stands for bundle i, Ai stands for agent i)
                B1  B2  B3
                __  __  __
            A1  |50  45  10     # C1 = 105
            A2  |30  35  20     # C2 = 85
            A3  |50  40  30     # C3 = 120
                __  __  __
                130 120 60      

        So the bidding matrix will be:
        AB = [[50, 45, 10], 
            [30, 35, 20], 
            [50, 40, 30]]

        M = AB[0,0] + AB[1, 1] + AB[2, 2] = 50 + 35 + 30 = 115 # Mind that the diagonal of the matrix is the sum of the values of the bundles allocated to each agent.
        C = Min(C1, C2, C3) = 85

        And the output will be the following tuple (M, C):
            (M, C) = (115, 85)

        TESTS:
        >>> m = BiddingForEnvyFreeness(ValuationMatrix([[50, 25, 10], [40, 25, 20], [35, 25, 25]]))
        >>> m.find_m_c_best()
        (100, 85)
        >>> m = BiddingForEnvyFreeness(ValuationMatrix([[50, 30, 50], [45, 35, 40], [10, 20, 35]]))
        >>> m.find_m_c_best()
        (120, 85)
        >>> m = BiddingForEnvyFreeness(ValuationMatrix([[50, 45, 10, 25], [30, 35, 20, 10], [50, 40, 35, 0], [50, 35, 35, 20]]))
        >>> m.find_m_c_best()
        (140, 95)
        '''
        players_num = list(range(matrix.num_of_agents))

        self.players_options = list(permutations(players_num))
        options = self.make_list(
            values=matrix, players_options=self.players_options)
        best, m = self.best_option(options)
        c = INF
        for x in range(matrix.num_of_agents):
            sum = 0
            for j in range(0, len(matrix[x])):
                sum += matrix[j][x]
            if c > sum:
                c = sum
        return m, c, best

    def player_package(self, opt: list):
        res = []
        for i in range(0, len(opt)):
            temp = []
            temp.append(i)
            temp.append(opt[i])
            res.append(temp)
        return res

    def bidding_to_envy(self, matrix: ValuationMatrix, options) -> ValuationMatrix:
        '''
        The 1st stage of the algorithm, initialize a table of envy values based the bidding matrix,
        by the following rules:
            - If an agent bidded a higher value for a bundle than the agent who gets it, 
            then the envy value is a positive number - the difference between both bids (the higher offer and the one that been accepted).
            - If an agent bidded a lower value for a bundle than the agent who gets it, 
            then the envy value is a negative number - the difference between both bids (the lower offer and the one that been accepted).
            - The last column of the table initilized with zeros, and represents accumulated discounts for each agent.
        Input: None. works on the bidding matrix of the class.
        For Example:
            b = [[50, 40, 35], 
                [25, 25, 25], 
                [10, 20, 35]]

        Output: Envy Matrix + initializes the envy matrix 
        For Example:
            e = [[  0, -10, -15, 0], 
                [  0,   0,   0, 0], 
                [-15,  -5,   0, 0]]

        TESTS:
        >>> m = BiddingForEnvyFreeness(ValuationMatrix([[50, 40, 35], [25, 25, 25], [10, 20, 35]]))
        >>> m.bidding_to_envy()
        [[0, -10, -15, 0], [0, 0, 0, 0], [-15, -5, 0, 0]]
        >>> m = BiddingForEnvyFreeness(ValuationMatrix([[50, 30, 50], [45, 35, 40], [10, 20, 35]]))
        >>> m.bidding_to_envy()
        [[0, -20, 0, 0], [10, 0, 5, 0], [-25, -15, 0, 0]]
        >>> m = BiddingForEnvyFreeness(ValuationMatrix([[50, 60, 0, 50], [20, 40, 40, 35], [10, 15, 25, 10], [20, 10, 35, 30]]))
        >>> m.bidding_to_envy()
        [[0, 10, -50, 0, 0], [-20, 0, 0, -5, 0], [-15, -10, 0, -15, 0], [-10, -20, 5, 0, 0]]
        >>> m = BiddingForEnvyFreeness(ValuationMatrix([[50, 30, 50, 50], [45, 35, 40, 35], [10, 20, 35, 35], [25, 10, 0, 20]]))
        >>> m.bidding_to_envy()
        [[0, -20, 0, 0, 0], [10, 0, 5, 0, 0], [-25, -15, 0, 0, 0], [5, -10, -20, 0, 0]]
        '''
        table = list(list())
        for x in range(0, matrix.num_of_agents):
            y = x
            sub = matrix[x][options[x]]
            logger.debug(f'sub: {sub}')
            temp = list()
            x = matrix[x]
            for j in range(0, len(x)):
                temp.append(x[j] - sub) if y == j else temp.append(x[j] - sub)
            temp.append(0)
            table.append(temp)
        logger.debug(f'Stage 1: Making a table\n{table}')
        return table

    def calculate_discounts(self, stage: int) -> ValuationMatrix:
        '''
        This recursive function calculates the discounts for each agent,
        based on the envy values in the envy matrix, which being manipulated along the way.
        As the first stage is being applied before, the first stage being calculated here is 2 (2nd stage).

        This is a recursive function, which means that it calls itself until the last stage is reached.

        Input: None. works on the envy matrix of the class.
        For Example, if m is the initial envy matrix (after the first stage):
            m = [[ 0,  10, -50,   0, 0], 
                [-20,   0,   0,  -5, 0], 
                [-15, -10,   0, -15, 0], 
                [-10, -20,   5,   0, 0]]

        Output: The envy matrix after the discounts are calculated.
        For Example:
                [[  0,  10, -50,  0,  0], 
                [-10,  10,  10,  5, 10], 
                [ -5,   0,  10, -5, 10], 
                [ -5, -15,  10,  5,  5]]

        Where the last column represents the final discounts for each agent.
        '''
        g = self.switch_row_column(self.table)
        # print(g)
        count = 0
        for i in range(0, len(g)):
            m = 0
            for j in g[i]:
                if g[self.options_list[i][0]][self.options_list[i][1]] < j and j != i and m < j:
                    m = j - g[i][i]
                    logger.debug(f'--- Player {i+1}: discount {j} ---')
            if m > 0:
                count += 1
                for x in range(0, len(g[i])+1):
                    self.table[i][x] += m
                # print(self.table)
            self.MC -= m
        if self.MC < 0:
            logger.warning('There is no good division for this problem')
            raise NameError('There is no good division for this problem')
        if count == 0:
            c = 1
            for x in self.table:
                self.dct[c] = x[len(self.table)]
                c += 1
            dis = self.MC/len(self.table)
            result = ''
            for x in range(1, len(self.dct)+1):
                self.dct[x] += dis
                # print(self.options_list[x-1][1])
                result += f'player {x} got package: {self.options_list[x-1][1]+1} with discount: {self.dct[x]}\n'
            logger.debug(
                f'Final Stage:\n{result}\n--------------------------\n')
            # print(f'Final Stage:\n{self.dct}\n--------------------------\n')
            return self.dct
        logger.debug(f'\nStage {stage}:\n{self.table}\n')
        self.calculate_discounts(stage+1)


def run(matrix: ValuationMatrix):
    BiddingForEnvyFreeness(matrix)


if __name__ == "__main__":
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.INFO)
    b1 = [[25, 40, 35], [50, 25, 25], [10, 20, 25]]
    run(ValuationMatrix(b1))
