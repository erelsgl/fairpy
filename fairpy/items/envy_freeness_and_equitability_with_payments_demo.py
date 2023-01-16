import fairpy
from fairpy.items.envy_freeness_and_equitability_with_payments import find_envy_freeness_and_equitability_with_payments, logger

logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

eval_1 = {"a": {"x": 40, "y": 20, "r": 30, "xy":65, "rx": 80, "rxy": 100}, "b": {"x": 10, "y":30, "r": 70, "xy":555, "rx": 79, "rxy": 90}}
allocation_1 = {"a": ["y"], "b": ["x", "r"]}

eval_2 = {"A": {"x": 70}, "B": {"x": 60}, "C": {"x": 40}, "D": {"x": 80}, "E": {"x": 55}}
allocation_2 = {"A": ["x"], "B": [], "C": [], "D": [], "E": []}

eq_value = {"x":10,"y":5,"z":15, "xy": 15, "yz": 20, "xz": 25}
eval_3 = {"A":eq_value, "B":eq_value, "C":eq_value, "D":eq_value}
allocation_3 = {"A":["x"], "B":["y"], "C":["z"], "D":[]}

a = {"x": 15, "y": 20, "z":10,"w":5, "xy": 45,"xz":25,"wx":20,"yz":30,"yw":30,"zw":20,"xyz":50,"xyw":50,"xzw":30,"yzw":40,"wxyz":50}
b = {"x": 30, "y": 35, "z":22,"w":7, "xy": 65,"xz":55,"wx":40,"yz":60,"yw":45,"zw":30,"xyz":90,"xyw":75,"xzw":65,"yzw":65,"wxyz":95}
c = {"x": 40, "y": 12, "z":13,"w":21, "xy": 55,"xz":55,"wx":65,"yz":25,"yw":35,"zw":35,"xyz":65,"xyw":75,"xzw":75,"yzw":50,"wxyz":90}
d = {"x": 5, "y": 7, "z":17,"w":19, "xy": 12,"xz":25,"wx":25,"yz":25,"yw":30,"zw":36,"xyz":30,"xyw":35,"xzw":45,"yzw":45,"wxyz":50}
eval_4 = {"A":a, "B":b, "C":c, "D":d}
allocation_4={"A":["x"], "B":["y"], "C":["z"], "D":["w"]}



print(fairpy.divide(find_envy_freeness_and_equitability_with_payments, eval_1))
print(fairpy.divide(find_envy_freeness_and_equitability_with_payments, eval_2))
print(fairpy.divide(find_envy_freeness_and_equitability_with_payments, eval_3))
print(fairpy.divide(find_envy_freeness_and_equitability_with_payments, eval_4))