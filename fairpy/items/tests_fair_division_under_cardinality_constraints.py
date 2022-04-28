import unittest

class TestAlgo(unittest.TestCase):

    def test_assertion_by_goods(self):
        catalog1 = ["food", "drinks"]
        dict_goods1 = {"1": {
                    "pizza":86,"hamburger":9,"sushi":40,"noodles":52,
                    "coffee":1,"vodka":13,"beer":84,"cola":36,
                },
                    "2":{
                    "pizza":68,"hamburger":1,"sushi":4,"noodles":25,
                    "coffee":5,"vodka":31,"beer":84,"water":10,
            }
        }
        catalog2 = ["laptops", "tv", "phones"]
        dict_goods2 = {"gidon": {
                    "asus":14,"lenovo":68,"acer":49,
                    "LG":56,"samsung":20,"sharp":31,
                    "iphone":40,"galaxy":2,"g5":42,
                },
                    "shmuel":{
                    "asus":41,"lenovo":86,"acer":94,
                    "LG":65,"samsung":2,"sharp":29,
                    "iphone":4,"galaxy":20,"g5":25,
            }
        } 
        data1 = Data(catalog1,dict_goods1)
        data2 = Data(catalog2,dict_goods2)

        ans1 = ef1_algorithm(["1","2"],data1)
        ans2 = ef1_algorithm(["gidon","shmuel"],data2)

        self.assertEqual(ans1, bundles.Bundle([{"1":["pizza","sushi","beer","vodka"]},{"2":["noodles","hamburger","cola","coffee"]}]))
        self.assertEqual(ans2, bundles.Bundle([{"1":["lenovo","asus","sharp","g5","galaxy"]},{"2":["acer","LG","samsung","iphone"]}]))

    def test_assertion_by_value(self):
        catalog = ["C1", "C2","C3","C4"]
        dict_goods = {"v1": {
                    "1":4,"2":17,"3":18,"4":39,
                    "5":19,"6":26,"7":31,"8":11,
                    "9":20,"10":14,"11":15,"12":27,
                    "13":44,"14":14,"15":15,"16":2,
                    "17":44,"18":10,"19":6,"20":17,
                    "21":17,"22":43,"23":20,"24":17,
                },"v2": {
                    "1":2,"2":29,"3":6,"4":6,
                    "5":23,"6":12,"7":50,"8":41,
                    "9":44,"10":32,"11":25,"12":19,
                    "13":38,"14":1,"15":19,"16":9,
                    "17":39,"18":34,"19":23,"20":41,
                    "21":36,"22":22,"23":49,"24":30,
                },
                "v3": {
                    "1":19,"2":7,"3":39,"4":38,
                    "5":9,"6":36,"7":29,"8":4,
                    "9":3,"10":34,"11":30,"12":6,
                    "13":11,"14":28,"15":7,"16":33,
                    "17":48,"18":39,"19":6,"20":1,
                    "21":8,"22":44,"23":13,"24":35,
                }   
        } 
        data = Data(catalog, dict_goods)
        sol = ef1_algorithm(["v1","v2","v3"], data)
        total_value_for_agents = [234,310,236]
        for i in range(3):
            self.assertEqual(sol[i], total_value_for_agents[i])
            

if __name__ == '__main__':
    unittest.main()