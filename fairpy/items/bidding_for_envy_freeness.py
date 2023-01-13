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

from fairpy import ValuationMatrix

import networkx as nx
import numpy as np
import pprint
import logging
logger = logging.getLogger(__name__)

class BiddingForEnvyFreeness:
    def __init__(self, matrix: ValuationMatrix = None):
        '''
        Bidding for Envy Freeness algorithm.
        :param matrix: a matrix of players bids for bundles.
        
        >>> matrix = [[3, 2, 1], [2, 3, 1], [2, 1, 3]]
        >>> bidding_for_envy_freeness = BiddingForEnvyFreeness(matrix)
        >>> print(bidding_for_envy_freeness.M)
        9
        
        >>> print(bidding_for_envy_freeness.C)
        6
        
        >>> print(bidding_for_envy_freeness.MC)
        3
        
        >>> bidding_for_envy_freeness.initialize_assessment_matrix()
        array([[ 0, -1, -2],
               [-1,  0, -2],
               [-1, -2,  0],
               [ 0,  0,  0]])
        
        
        '''
        
        logger.info(f'\n----------[ INFO ]----------\nInitializing BiddingForEnvyFreeness with bidding matrix:\n{matrix}\n----------------------------')
        
        # initializing the players bids for bundles matrix
        self.players_bids_for_bundles = matrix
        
        if not isinstance(matrix, ValuationMatrix):
            self.players_bids_for_bundles = ValuationMatrix(matrix)

        

        self.players_order = self.find_best_matching()
        logger.debug(f'\n----------[ INFO ]----------\nFound best players order:\n{pprint.pformat(self.players_order)}\n----------------------------')
        
        self.players_bids_for_bundles = ValuationMatrix([self.players_bids_for_bundles[i] for i in self.players_order])
        logger.debug(f'\n----------[ INFO ]----------\nReordered players bids for bundles matrix:\n{pprint.pformat(self.players_bids_for_bundles)}\n----------------------------')
        
                
        # finding M and C
        self.M, self.C, self.MC = self.find_m_c()
        logger.debug(f'\n----------[ INFO ]----------\nFound M = {self.M}, C = {self.C}, M-C = {self.MC}\n----------------------------')
        
        # initializing the assessment matrix
        self.assessment_matrix = self.initialize_assessment_matrix()
        logger.info(f'\n----------[ INFO ]----------\nInitialized assessment matrix:\n{pprint.pformat(self.assessment_matrix)}\n----------------------------')
        
        # running the compensation procedure
        self.compensation_procedure()
        
        
        logger.info(f'\n----------[ INFO ]----------\nFinished BiddingForEnvyFreeness with assessment matrix:\n{pprint.pformat(self.assessment_matrix)}\n----------------------------')
        
        
    def find_best_matching(self, matrix: ValuationMatrix = None) -> list:
        '''
        Find the best matching for the given bidding matrix.
        Using NetworkX maximum_weight_matching algorithm, which finds the maximum weight matching in a bipartite graph.
        For applying the algorithm on our data, the following conversion is done:
            consider 2 sides of the bipartite graph: A, B, such that:
            A is the set of players, B is the set of bundles.
            each edge A_i -> B_j has weight equal to the bid of player i for bundle j.
            
            The algorithm returns a list of allocated bundles for each player, in the form of a list of integers,
            which each index of the list is a player and the value of the index is the allocated bundle for the player.
                    
        reference: 
        https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.matching.max_weight_matching.html
        
        :param matrix: a matrix of players bids for bundles.
        :return: a list of allocated bundles for each player.
        >>> matrix = [[3, 2, 1], [2, 3, 1], [2, 1, 3]]
        >>> bidding_for_envy_freeness = BiddingForEnvyFreeness(matrix)
        >>> print(bidding_for_envy_freeness.find_best_matching(ValuationMatrix(matrix)))
        [0, 1, 2]
        >>> matrix = [[2, 3, 1], [3, 2, 1], [2, 1, 3]]
        >>> bidding_for_envy_freeness = BiddingForEnvyFreeness(matrix)
        >>> print(bidding_for_envy_freeness.find_best_matching(ValuationMatrix(matrix)))
        [1, 0, 2]
        >>> matrix = [[2, 3, 1], [2, 1, 3], [3, 2, 1]]
        >>> bidding_for_envy_freeness = BiddingForEnvyFreeness(matrix)
        >>> print(bidding_for_envy_freeness.find_best_matching(ValuationMatrix(matrix)))
        [2, 0, 1]
        
        >>> matrix = [[50, 20, 10, 20], [60, 40, 15, 10], [0, 40, 25, 35], [50, 35, 10, 30]]
        >>> bidding_for_envy_freeness = BiddingForEnvyFreeness(matrix)
        >>> print(bidding_for_envy_freeness.find_best_matching(ValuationMatrix(matrix)))
        [0, 1, 2, 3]
        >>> matrix = [[60, 40, 15, 10], [50, 20, 10, 20], [0, 40, 25, 35], [50, 35, 10, 30]]
        >>> bidding_for_envy_freeness = BiddingForEnvyFreeness(matrix)
        >>> print(bidding_for_envy_freeness.find_best_matching(ValuationMatrix(matrix)))
        [1, 0, 2, 3]
        >>> matrix = [[60, 40, 15, 10], [0, 40, 25, 35], [50, 20, 10, 20], [50, 35, 10, 30]]
        >>> bidding_for_envy_freeness = BiddingForEnvyFreeness(matrix)
        >>> print(bidding_for_envy_freeness.find_best_matching(ValuationMatrix(matrix)))
        [2, 0, 1, 3]
        >>> matrix = [[60, 40, 15, 10], [0, 40, 25, 35], [50, 35, 10, 30], [50, 20, 10, 20]]
        >>> bidding_for_envy_freeness = BiddingForEnvyFreeness(matrix)
        >>> print(bidding_for_envy_freeness.find_best_matching(ValuationMatrix(matrix)))
        [3, 0, 1, 2]
        
        '''
        if matrix is None:
            matrix = self.players_bids_for_bundles
        
        # Initializing the graph
        g = nx.Graph()
        
        # Creating the edges by bids
        edges = [(f'p{player}', f'b{bundle}', matrix[bundle][player]) for player in range(matrix.num_of_agents) for bundle in range(matrix.num_of_objects)]
        
        # Adding the edges to the graph
        g.add_weighted_edges_from(edges)
        
        # Finding the maximum weight matching
        matching = nx.max_weight_matching(g)
        
        # Sorting the tuples to a form of (player, bundle)
        matching = [sorted(m, reverse=True) for m in matching]
        
        # Sorting the tuples by player number
        matching = sorted(matching, key=lambda x: int(x[0][1:]))
        
        # Returning the allocated bundles for each player as a list of integers
        # each index of the list is a player and the value of the index is the allocated bundle for the player.
        return [int(m[1][1:]) for m in matching]
    
        
    def find_m_c(self, matrix: ValuationMatrix = None) -> tuple:
        '''
        Find M and C for the given bidding matrix.
        :param matrix: a matrix of players bids for bundles.
        :return: M, C, M-C
        >>> matrix = [[3, 2, 1], [2, 3, 1], [2, 1, 3]]
        >>> bidding_for_envy_freeness = BiddingForEnvyFreeness(matrix)
        >>> print(bidding_for_envy_freeness.M)
        9
        >>> print(bidding_for_envy_freeness.C)
        6
        >>> print(bidding_for_envy_freeness.MC)
        3
        
        
        >>> matrix = [[50, 20, 10, 20],[60, 40, 15, 10],[0, 40, 25, 35], [50, 35, 10, 30]]
        >>> bidding_for_envy_freeness = BiddingForEnvyFreeness(matrix)
        >>> print(bidding_for_envy_freeness.M)
        145
        >>> print(bidding_for_envy_freeness.C)
        100
        >>> print(bidding_for_envy_freeness.MC)
        45
        
        
        >>> matrix = [[50, 40, 35], [25, 25, 25], [10, 20, 25]]
        >>> bidding_for_envy_freeness = BiddingForEnvyFreeness(matrix)
        >>> print(bidding_for_envy_freeness.M)
        100
        >>> print(bidding_for_envy_freeness.C)
        55
        >>> print(bidding_for_envy_freeness.MC)
        45
        
        '''
        
        # for tests, debugging and standalone use
        if matrix is None:
            matrix = self.players_bids_for_bundles
            
        elif not isinstance(matrix, ValuationMatrix):
            matrix = ValuationMatrix(matrix)
        
        # M is the diagonal sum of the matrix, which represents the sum of the players' bids for their allocated bundles
        m = sum([matrix[Bi][Bi] for Bi in range(matrix.num_of_agents)])
        
        # C is the minimum sum of a row, which represents the minimum sum of single player's bids for all bundles
        c = min([sum(matrix[ci]) for ci in range(matrix.num_of_agents)])
        
        return m, c, m-c
    
    def initialize_assessment_matrix(self, matrix: ValuationMatrix = None) -> np.ndarray:
        """
        Create the inititial assessment matrix for the given bidding matrix( by default the class' 'self.players_bids_for_bundles' ).
        :param matrix: a matrix of players bids for bundles.
        :return: the initial assessment matrix.
        >>> matrix = [[3, 2, 1], [2, 3, 1], [2, 1, 3]]
        >>> bidding_for_envy_freeness = BiddingForEnvyFreeness(matrix)
        >>> print(bidding_for_envy_freeness.initialize_assessment_matrix())
        [[ 0 -1 -2]
         [-1  0 -2]
         [-1 -2  0]
         [ 0  0  0]]
        
        
        >>> matrix = [[50, 20, 10, 20],[60, 40, 15, 10],[0, 40, 25, 35], [50, 35, 10, 30]]
        >>> bidding_for_envy_freeness = BiddingForEnvyFreeness(matrix)
        >>> print(bidding_for_envy_freeness.initialize_assessment_matrix())
        [[  0 -20 -15 -10]
         [ 10   0 -10 -20]
         [-50   0   0   5]
         [  0  -5 -15   0]
         [  0   0   0   0]]
        
        
        >>> matrix = [[50, 40, 35], [25, 25, 25], [10, 20, 25]]
        >>> bidding_for_envy_freeness = BiddingForEnvyFreeness(matrix)
        >>> print(bidding_for_envy_freeness.initialize_assessment_matrix())
        [[  0  15  10]
         [-25   0   0]
         [-40  -5   0]
         [  0   0   0]]
        """
        
        # for tests, debugging and standalone use
        if matrix is None:
            matrix = self.players_bids_for_bundles            

        
        # creating the assessment matrix, each players enviness is:
        #   ( his bid for a bundle ( [player, bid] ) ) - ( the accepted bid for that bundle ( [bid, bid] ) )
        assessment_matrix = [
            [matrix[player][bid] - matrix[bid][bid] 
             for bid in range(matrix.num_of_objects)]
            for player in range(matrix.num_of_agents)]
        
        # adding a row of zeros to the end of the matrix for the initial players discounts
        assessment_matrix.append([0 for _ in range(matrix.num_of_agents)])
        
        # returning the assessment matrix as a numpy array
        return np.array(assessment_matrix)
    
    def compensation_procedure(self, assessment_matrix: np.ndarray = None, MC: int = None) -> np.ndarray:
        '''
        The compensation procedure for the Bidding for Envy Freeness algorithm.
        :param assessment_matrix: the assessment matrix to perform the compensation procedure on.
        :return: the assessment matrix after the compensation procedure.
        '''
        
        # for tests, debugging and standalone use
        if assessment_matrix is None and MC is None:
            assessment_matrix = self.assessment_matrix
            MC = self.MC

        # if all players enviness is less or equal to zero, return the assessment matrix
        if all(
            [all([x <= assessment_matrix[player][player] for x in assessment_matrix[player]]) for player in range(len(assessment_matrix)-1)]
            ):
            
            # adding the remaining MC to the last row of the assessment matrix (the players discounts) evenly
            assessment_matrix[-1, :] += int((self.MC - sum(self.assessment_matrix[-1, :])) / self.players_bids_for_bundles.num_of_agents)
            logger.debug(f'\n----------< DEBUG (compensation_procedure) >----------\nCompensation procedure finished with assessment matrix:\n{pprint.pformat(assessment_matrix)}\n------------------------------------------------------')

            # returning the assessment matrix - final result
            return assessment_matrix
        
        # compensation procedure is not finished, continue
        else:
            
            logger.debug(f'\n----------< DEBUG (compensation_procedure) >----------\nCompensation procedure started with assessment matrix:\n{pprint.pformat(assessment_matrix)}\n------------------------------------------------------')
            
            # finding the maximum enviness of each player, if exists. else - zero
            compansations = [max(assessment_matrix[player]) - assessment_matrix[player][player] if any([x > assessment_matrix[player][player] for x in assessment_matrix[player]]) else 0 for player in range(len(assessment_matrix)-1)]
            logger.debug(f'\n----------< DEBUG (compensation_procedure) >----------\nCompansations:\n{pprint.pformat(compansations)}\n------------------------------------------------------')
            
           # adding the compansations to the assessment matrix
            for compansation in range(len(compansations)):
                # adding the compansation to the player's column
                assessment_matrix[:, compansation] += compansations[compansation]
            logger.debug(f'\n----------< DEBUG (compensation_procedure) >----------\nCompensation procedure finished with assessment matrix:\n{pprint.pformat(assessment_matrix)}\n------------------------------------------------------')
            
            # if total discount is greater than MC, raise an exception
            if MC and sum(self.assessment_matrix[-1, :]) > MC:
                logger.warning(f'\n--------!!! WARNING !!!--------\nNo fair division exists for the given bidding matrix:\n{self.players_bids_for_bundles}\n-------------------------------')
                raise Exception('No fair division exists for the given bidding matrix')
            
            # returning the assessment matrix after the compensation procedure step
            return self.compensation_procedure(assessment_matrix, MC)
                
def bidding_for_envy_freeness(bidding_matrix: ValuationMatrix) -> dict:
    '''
    The Bidding for Envy Freeness function.
    :param bidding_matrix: the bidding matrix to perform the Bidding for Envy Freeness algorithm on.
    :return: the allocation of bundles and discounts after the Bidding for Envy Freeness algorithm.
    >>> bidding_for_envy_freeness([[50, 20, 10, 20], [60, 40, 15, 10], [0, 40, 25, 35], [50, 35, 10, 30]])
    {0: {'bundle': 0, 'discount': 5}, 1: {'bundle': 1, 'discount': 15}, 2: {'bundle': 2, 'discount': 15}, 3: {'bundle': 3, 'discount': 10}}
    
    >>> bidding_for_envy_freeness([[60, 40, 15, 10], [50, 20, 10, 20], [0, 40, 25, 35], [50, 35, 10, 30]])
    {1: {'bundle': 0, 'discount': 5}, 0: {'bundle': 1, 'discount': 15}, 2: {'bundle': 2, 'discount': 15}, 3: {'bundle': 3, 'discount': 10}}
    
    >>> bidding_for_envy_freeness([[50, 40, 35], [25, 25, 25], [10, 20, 25]])
    {0: {'bundle': 0, 'discount': 25}, 1: {'bundle': 1, 'discount': 10}, 2: {'bundle': 2, 'discount': 10}}
    
    >>> bidding_for_envy_freeness([[25, 25, 25], [10, 20, 25], [50, 40, 35]])
    {2: {'bundle': 0, 'discount': 25}, 0: {'bundle': 1, 'discount': 10}, 1: {'bundle': 2, 'discount': 10}}
    '''
    bfef =  BiddingForEnvyFreeness(bidding_matrix)
    return {player: {'bundle': index, 'discount': bfef.assessment_matrix[-1][index]} for index, player in enumerate(bfef.players_order)}
        
if __name__ == '__main__':
    import sys 
    logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)
    
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
    