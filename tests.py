import unittest
from util import re_to_postfix
from parsing_exceptions import MismatchedParentheses, UnrecognizedToken

class Re_to_postfix_test(unittest.TestCase):
    def test_concatenation(self):
        self.assertEqual(re_to_postfix('ab.ab'), ['a', 'b', '.', 'a', 'b', '.', '.'])
        self.assertEqual(re_to_postfix('a(bb)*a'), ['a', 'b', 'b', '.', '*', '.', 'a', '.'])
        self.assertEqual(re_to_postfix('(a(b(c)))'), ['a', 'b', 'c', '.', '.'])
        self.assertEqual(re_to_postfix('()'), [])

    def test_exceptions(self):
        with self.assertRaises(MismatchedParentheses):
            re_to_postfix('(a(bc)))')
            re_to_postfix('(')

    def test_implicit_concatenation(self):
        self.assertEqual(re_to_postfix('abc'), ['a', 'b', 'c', '.', '.'])
        self.assertEqual(re_to_postfix('a(bb)+a'), ['a','b','b','.','+','.','a','.'])


if __name__ == '__main__':
    unittest.main()
            
