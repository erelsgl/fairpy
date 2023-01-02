import logging
logger = logging.getLogger("hey")
console = logging.StreamHandler()  # writes to stderr (= cerr)
logger.handlers = [console]

# Example function
def quadratic_formula(a:float, b:float ,c:float) -> float:
    """ Returns the real solutions to the equation ax^2 + bx + c = 0  """
    import math
    # logger.info(f'quadratic_formula({a},{b},{c})')  # NOTE: We deliberately use the old-style C format below, and NOT the f-string.
    logger.info('quadratic_formula(%g,%g,%g)', a, b, c)
    discri = b**2 - 4*a*c
    logger.debug('Compute the discriminant: %g', discri)
    if discri<0:
        logger.warning('Discriminant is negative!')
        return (0,0)
    root_a = (-b + math.sqrt(discri))/(2*a)
    logger.debug('Compute the positive root: %g', root_a)
    root_b = (-b - math.sqrt(discri))/(2*a)
    logger.debug('Compute the negative root: %g', root_b)
    return root_a , root_b

print(quadratic_formula(1, 0, -4))
print(quadratic_formula(1, 0, 4))