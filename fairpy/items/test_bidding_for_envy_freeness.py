'''
Main testing module for bidding_for_envy_freeness.py.

Programmers: Barak Amram, Adi Dahari.
Since: 2022-12.
'''

from fairpy.items.bidding_for_envy_freeness import BiddingForEnvyFreeness
from fairpy.items.valuations import ValuationMatrix


def test_find_m_c():
    '''
    Test the find_m_c function.
    '''

    bidding_matrix = ValuationMatrix(
        [[50, 45, 10], [30, 35, 20], [50, 40, 30]])
    assert BiddingForEnvyFreeness(bidding_matrix).find_m_c() == (115, 85)

    bidding_matrix = ValuationMatrix(
        [[50, 25, 10], [40, 25, 20], [35, 25, 25]])
    assert BiddingForEnvyFreeness(bidding_matrix).find_m_c() == (100, 85)

    bidding_matrix = ValuationMatrix(
        [[50, 30, 50], [45, 35, 40], [10, 20, 35]])
    assert BiddingForEnvyFreeness(bidding_matrix).find_m_c() == (120, 85)

    bidding_matrix = ValuationMatrix(
        [[50, 45, 10, 25], [30, 35, 20, 10], [50, 40, 35, 0], [50, 35, 35, 20]])
    assert BiddingForEnvyFreeness(bidding_matrix).find_m_c() == (140, 95)


def test_bidding_to_envy():
    '''
    Test the bidding_to_envy function.
    '''

    bidding_matrix = ValuationMatrix(
        [[50, 40, 35], [25, 25, 25], [10, 20, 35]])
    assert BiddingForEnvyFreeness(bidding_matrix).bidding_to_envy(
    ) == ValuationMatrix([[0, -10, -15, 0], [0, 0, 0, 0], [-15, -5, 0, 0]])

    bidding_matrix = ValuationMatrix(
        [[50, 30, 50], [45, 35, 40], [10, 20, 35]])
    assert BiddingForEnvyFreeness(bidding_matrix).bidding_to_envy(
    ) == ValuationMatrix([[0, -20, 0, 0], [10, 0, 5, 0], [-25, -15, 0, 0]])

    bidding_matrix = ValuationMatrix([[50, 60, 0, 50], [20, 40, 40, 35], [
                                     10, 15, 25, 10], [20, 10, 35, 30]])
    assert BiddingForEnvyFreeness(bidding_matrix).bidding_to_envy() == ValuationMatrix(
        [[0, 10, -50, 0, 0], [-20, 0, 0, -5, 0], [-15, -10, 0, -15, 0], [-10, -20, 5, 0, 0]])

    bidding_matrix = ValuationMatrix(
        [[50, 30, 50, 50], [45, 35, 40, 35], [10, 20, 35, 35], [25, 10, 0, 20]])
    assert BiddingForEnvyFreeness(bidding_matrix).bidding_to_envy() == ValuationMatrix(
        [[0, -20, 0, 0, 0], [10, 0, 5, 0, 0], [-25, -15, 0, 0, 0], [5, -10, -20, 0, 0]])


def test_calculate_discounts():
    '''
    Test the calculate_discounts function.
    '''

    bidding_matrix = [[0, 10, -50, 0, 0], [-20, 0, 0, -5, 0],
                      [-15, -10, 0, -15, 0], [-10, -20, 5, 0, 0]]

    bidding_matrix = ValuationMatrix(bidding_matrix)

    bfef = BiddingForEnvyFreeness(bidding_matrix)

    envy_mat = bfef.bidding_to_envy()

    assert bfef.calculate_discounts(envy_mat) == ValuationMatrix([[0,  10, -50,  0,  0],
                                                                  [-10,  10,
                                                                      10,  5, 10],
                                                                  [-5,   0,
                                                                      10, -5, 10],
                                                                  [-5, -15,  10,  5,  5]])


def test_full_cases():
    '''
    Test full cases.
    '''

    # -------------------Case 1-------------------
    # the bidding matrix in a raw form - nested list.
    input_matrix = [[50, 40, 35],
                    [25, 25, 25],
                    [10, 20, 35]]

    # convert the input matrix to a ValuationMatrix object.
    valuation_matrix = ValuationMatrix(input_matrix)

    # create a BiddingForEnvyFreeness object.
    bfef = BiddingForEnvyFreeness(valuation_matrix)

    # calculate the envy matrix - 1st stage.
    envy_mat = bfef.bidding_to_envy()

    # assert the envy matrix is correct.
    assert envy_mat == ValuationMatrix([[0, -10, -15, 0],
                                        [0,   0,   0, 0],
                                        [-15,  -5,   0, 0]])

    final_table = bfef.calculate_discounts()

    assert final_table == ValuationMatrix([[0, -10, -15, 0],
                                           [0,   0,   0, 0],
                                           [-15,  -5,   0, 0]])

    assert final_table[:, -1] == [0, 0, 0]

    # -------------------Case 2-------------------
    #             4 agents, 4 bundles.

    input_matrix = [[50, 60, 0, 50], [20, 40, 40, 35],
                    [10, 15, 25, 10], [20, 10, 35, 30]]

    valuation_matrix = ValuationMatrix(input_matrix)

    bfef = BiddingForEnvyFreeness(valuation_matrix)

    envy_mat = bfef.bidding_to_envy()

    assert envy_mat == ValuationMatrix(
        [[0, 10, -50, 0, 0], [-20, 0, 0, -5, 0], [-15, -10, 0, -15, 0], [-10, -20, 5, 0, 0]])

    final_table = bfef.calculate_discounts()

    assert final_table == ValuationMatrix(
        [[0, 10, -50, 0, 0], [-10, 10, 10, 5, 10], [-5, 0, 10, -5, 10], [-5, -15, 10, 5, 5]])

    assert final_table[:, -1] == [0, 10, 10, 5]
