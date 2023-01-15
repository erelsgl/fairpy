"""
Demo to proportional_borda_allocations -
Article: "Proportional Borda Allocations"
Authors: Andreas Darmann and Christian Klamler. See https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5075029/
Publishing the article: 2016

Programmer: Shlomo Glick
Since:  2023-01
"""

import fairpy
from fairpy.items.propm_allocation import propm_allocation
from fairpy.items.proportional_borda_allocations import proportional_division, proportional_division_equal_number_of_items_and_players

import logging

proportional_division.logger.addHandler(logging.StreamHandler())
proportional_division.logger.setLevel(logging.INFO)

def main():
    agents1 = [[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9]]
    print(fairpy.divide(proportional_division, agents1))
    agents2 = {
        'Avi': {'A': 7, 'B': 2, 'C': 6, 'D': 4, 'E': 5, 'F': 0, 'G': 1, 'H': 3}, 
        'Beni': {'A': 7, 'B': 5, 'C': 6, 'D': 3, 'E': 4, 'F': 0, 'G': 2, 'H': 1}, 
        'David': {'A': 7, 'B': 4, 'C': 3, 'D': 5, 'E': 2, 'F': 1, 'G': 6, 'H': 0}, 
        'SHlomo': {'A': 6, 'B': 5, 'C': 2, 'D': 3, 'E': 1, 'F': 0, 'G': 4, 'H': 7}
    }
    print(fairpy.divide(proportional_division, agents2))
    agents3 = {
        'Avi': {'A': 2, 'B': 0, 'C': 1},
        'Beni': {'A': 2, 'B': 0, 'C': 1},
        'David': {'A': 2, 'B': 1, 'C': 0},
    }
    print(fairpy.divide(proportional_division_equal_number_of_items_and_players, agents3))

if __name__ == "__main__":
    main()