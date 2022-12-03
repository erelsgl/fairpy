from fairpy.items.valuations import ValuationMatrix


def find_m_c(p: ValuationMatrix) -> tuple:
    '''
    This function intitalizes the algorithm M and C values,
    Where:
        - M stands for the total value of initially invested amount of money by each agent, for the bundle of items allocated to him.
        - C stands for the minimum total biddings of a single agent for all available bundles.

    For Example:
    For the following matrix: (Bi stands for bundle i, Ai stands for agent i)
             B1  B2  B3
             __  __  __
        A1  |50  45  10     # C1 = 105
        A2  |30  35  20     # C2 = 85
        A3  |50  40  30     # C3 = 120
            __  __  __
            130 120 60      

    So the input matrix will be:
    AB = [[50, 45, 10], 
          [30, 35, 20], 
          [50, 40, 30]]

    M = AB[0,0] + AB[1, 1] + AB[2, 2] = 50 + 35 + 30 = 115 # Mind that the diagonal of the matrix is the sum of the values of the bundles allocated to each agent.
    C = Min(C1, C2, C3) = 85

    And the output will be the following tuple (M, C):
        (M, C) = (115, 85)

    TESTS:
    >>> find_m_c(ValuationMatrix([[50, 25, 10], [40, 25, 20], [35, 25, 25]]))
    (100, 85)
    >>> find_m_c(ValidationMatrix([[50, 30, 50], [45, 35, 40], [10, 20, 35]]))
    (120, 85)
    >>> find_m_c(ValidationMatrix([[50, 45, 10, 25], [30, 35, 20, 10], [50, 40, 35, 0], [50, 35, 35, 20]]))
    (140, 95)
    '''


def biddings_to_envy(b: ValuationMatrix) -> ValuationMatrix:
    '''
    The 1st stage of the algorithm, initialize a table of envy values based the bidding matrix,
    by the following rules:
        - If an agent bidded a higher value for a bundle than the agent who gets it, 
          then the envy value is a positive number - the difference between both bids (the higher offer and the one that been accepted).
        - If an agent bidded a lower value for a bundle than the agent who gets it, 
          then the envy value is a negative number - the difference between both bids (the lower offer and the one that been accepted).
        - The last column of the table initilized with zeros, and represents accumulated discounts for each agent.
    Input: Bidding Matrix
    For Example:
        b = [[50, 40, 35], 
             [25, 25, 25], 
             [10, 20, 35]]

    Output: Envy Matrix
    For Example:
        e = [[  0, -10, -15, 0], 
             [  0,   0,   0, 0], 
             [-15,  -5,   0, 0]]

    TESTS:
    >>> stage1(ValuationMatrix([[50, 40, 35], [25, 25, 25], [10, 20, 35]]))
    [[0, -10, -15, 0], [0, 0, 0, 0], [-15, -5, 0, 0]]
    >>> stage1(ValidationMatrix([[50, 30, 50], [45, 35, 40], [10, 20, 35]]))
    [[0, -20, 0, 0], [10, 0, 5, 0], [-25, -15, 0, 0]]
    >>> stage1(ValidationMatrix([[50, 60, 0, 50], [20, 40, 40, 35], [10, 15, 25, 10], [20, 10, 35, 30]]))
    [[0, 10, -50, 0, 0], [-20, 0, 0, -5, 0], [-15, -10, 0, -15, 0], [-10, -20, 5, 0, 0]]
    >>> stage1(ValidationMatrix([[50, 30, 50, 50], [45, 35, 40, 35], [10, 20, 35, 35], [25, 10, 0, 20]]))
    [[0, -20, 0, 0, 0], [10, 0, 5, 0, 0], [-25, -15, 0, 0, 0], [5, -10, -20, 0, 0]]
    '''


def calculate_discounts(m: ValuationMatrix) -> ValuationMatrix:
    '''
    This recursive function calculates the discounts for each agent,
    based on the envy values in the envy matrix, which being manipulated along the way.
    As the first stage is being applied before, the first stage being calculated here is 2 (2nd stage).

    This is a recursive function, which means that it calls itself until the last stage is reached.

    Input: The current state of the envy matrix.
    For Example:
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
