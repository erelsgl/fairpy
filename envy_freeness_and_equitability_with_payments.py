from fairpy import Allocation, MonotoneValuation

# def envy_freeness_and_equitability_with_payments(allocation: dict, evaluation: dict):
    # """
    # "Achieving Envy-freeness and Equitability with Monetary Transfers" by Haris Aziz (2021),
    # https://ojs.aaai.org/index.php/AAAI/article/view/16645
    #
    # Algorithm 1: Creating envy-freeness and equitability division with the help of a payment function.
    #
    # Programmers: Noamya Shani, Eitan Shankolevski.
    #
    # >>> agent_dict = {"A":{"x":70},"B":{"x":60},"C":{"x":40},"D":{"x":80},"E":{"x":55}}
    # >>> envy_freeness_and_equitability_with_payments(Allocation(agents = agent_dict, bundles={"A":{"x"}}))
    # {"bundles":[[],[],[],[0],[]],"payments":[-16,-16,-16,64,-16]}
    # >>> eq_value = {"x":10,"y":5,"z":15}
    # >>> agent_dict2 = {"A":eq_value,"B":eq_value,"C":eq_value,"D":eq_value}
    # >>> envy_freeness_and_equitability_with_payments(Allocation(agents = agent_dict2, bundles={"A":{"x"},"B":{"y"},"C":{"z"}}))
    # {"bundles":[[0],[1],[2],[]],"payments":[2.5,-2.5,7.5,-7.5]}
    # >>> a = MonotoneValuation({"x": 15, "y": 20, "z":10,"w":5, "xy": 45,"xz":25,"xw":20,"yz":30,"yw":30,
    # ... "zw":20,"xyz":50,"xyw":50,"xzw":30,"yzw":40,"xyzw":50})
    # >>> b = MonotoneValuation({"x": 30, "y": 35, "z":22,"w":7, "xy": 65,"xz":55,"xw":40,"yz":60,"yw":45,
    # ... "zw":30,"xyz":90,"xyw":75,"xzw":65,"yzw":65,"xyzw":95})
    # >>> c = MonotoneValuation({"x": 40, "y": 12, "z":13,"w":21, "xy": 55,"xz":55,"xw":65,"yz":25,"yw":35,
    # ... "zw":35,"xyz":65,"xyw":75,"xzw":75,"yzw":50,"xyzw":90})
    # >>> d = MonotoneValuation({"x": 5, "y": 7, "z":17,"w":19, "xy": 12,"xz":25,"xw":25,"yz":25,"yw":30,
    # ... "zw":36,"xyz":30,"xyw":35,"xzw":45,"yzw":45,"xyzw":50})
    # >>> agent_dict3 = {"A":a,"B":b,"C":c,"D":d}
    # >>> envy_freeness_and_equitability_with_payments(Allocation(agents = agent_dict3, bundles={"A":{"x"},"B":{"y"},"C":{"z"},"D":{"w"}}))
    #  {"bundles":[[],[0,1,2],[3],[]],"payments":[-27.75,62.25,-6.75,-27.75]}
    # """
    #
    # pass

eval = {"a": {"x": 40, "y":20, "r": 30, "rx": 80, "rxy": 100}, "b": {"x": 10, "y":30, "r": 70, "rx": 79, "rxy": 90}}
allocation = {"a": ["y"], "b": ["x", "r"]}


def get_value(agent, boundle_of_agent: list, eval_func :dict):
    curr_bundles = "".join(map(str, sorted(boundle_of_agent)))
    return eval_func[agent][curr_bundles ]

# print(get_value("a",["y"], eval))
# print(get_value("b",["x", "r"], eval))
# print([] + [5, 6, 8])

def compare_2_bundles(agent_a, agent_b, allo: dict, eval_func: dict):
    if get_value(agent_a, allo[agent_a] + allo[agent_b], eval_func) > get_value(agent_a, allo[agent_a], eval_func) + get_value(agent_b, allo[agent_b], eval_func):
        allo[agent_a] = allo[agent_a] + allo[agent_b]
        allo[agent_b] = []
        return True
    return False

# print(compare_2_bundles("b","a", allocation, eval))
# print(allocation)
print(compare_2_bundles("a","b", allocation, eval))
print(allocation)