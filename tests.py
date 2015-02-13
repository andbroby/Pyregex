import unittest
from util import re_to_postfix

class Re_to_postfix_test(unittest.TestCase):
    def test_concatenation(self):
        self.assertEqual(re_to_postfix('ab.ab'), ['ab', 'ab', '.'])
        self.assertEqual(re_to_postfix('(ab.bb).b'), ['ab', 'bb', '.', 'b', '.'])
        self.assertEqual(re_to_postfix('bbb.((a.b).b)'), ['bbb', 'a', 'b', '.', 'b', '.', '.'])


if __name__ == '__main__':
    unittest.main()
            
