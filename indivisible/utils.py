#!python3

"""
Short utils used for demonstration and presentation
"""



def plural(i: int)->str:
    return " " if i==1 else "s"



def demo(algorithm, families, goods, *args):
    """
    Demonstrate the given algorithm on the given families (must be 2 families).
    """
    for family in families:
        print(family)
    allocation = algorithm(families, goods, *args)
    print("\nFinal allocation:")
    for index in range(len(families)):
        print (" * ", families[index].allocation_description(allocation[index], allocation))


