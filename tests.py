import unittest
from shuntingyard import shunting_yard

class ShuntingYardTests(unittest.TestCase):
    def test_subtraction_addition(self):
        self.assertEqual(shunting_yard('4+3+2-4-2-3+4+2') ,['4', '3', '+', '2', '+', '4', '-', '2', '-', '3', '-', '4', '+', '2', '+'])
        self.assertEqual(shunting_yard('4-2-1-2'), ['4', '2', '-', '1', '-', '2', '-'])
        self.assertEqual(shunting_yard('423+23+11'), ['423', '23', '+', '11', '+'])

    def test_multiplication_division(self):
        self.assertEqual(shunting_yard('4*3*5/2*3/2*4*5/5'), ['4', '3', '*', '5', '*', '2', '/', '3', '*', '2', '/', '4', '*', '5', '*', '5', '/'])
        self.assertEqual(shunting_yard('4*2*1*4*3/2/3'), ['4','2','*','1','*','4','*','3','*','2','/','3','/'])
        self.assertEqual(shunting_yard('423*123*112415*1'), ['423', '123', '*', '112415', '*', '1', '*'])
                                                        
                                      
    def test_powers(self):
        self.assertEqual(shunting_yard('4^2^3^5^4^3'), ['4','2','3', '5', '4', '3', '^', '^', '^', '^', '^'])
        self.assertEqual(shunting_yard('23^1213^523^13'), ['23', '1213', '523', '13', '^', '^', '^'])


if __name__ == '__main__':
    unittest.main()
            
