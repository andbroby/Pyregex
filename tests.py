import unittest
import re
from util import re_to_postfix, match
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

class Re_matching_tests(unittest.TestCase):
    def boolre(self, pattern, string):
        return bool(re.match(pattern, string))
    
    def test_concatenation_matching(self):
        self.assertEqual(match('ab', 'ab'), self.boolre('ab', 'ab'))
        self.assertEqual(match('a(bb).(cd)', 'abbcd'), self.boolre('a(bb)(cd)', 'abbcd'))
        self.assertEqual(match('', ''), self.boolre('',''))
        self.assertEqual(match('(a(b))', 'ab'), self.boolre('(a(b))', 'ab'))
        self.assertEqual(match('ab(cd).ba(dc(cd))', 'abcdbadccd'), self.boolre('ab(cd)ba(dc(cd))', 'abcdbadccd'))


if __name__ == '__main__':
    unittest.main()
            
