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
        self.assertEqual(match('aaaa(b).(b).c(d)', 'aaaabbcd'), self.boolre('aaaa(b)(b)c(d)', 'aaaabbcd'))

    def test_alternation_matching(self):
        self.assertEqual(match('a|b', 'a'), self.boolre('a|b', 'a'))
        self.assertEqual(match('a|b', 'b'), self.boolre('a|b', 'b'))
        self.assertEqual(match('(ab)|(bc)', 'ab'), self.boolre('(ab)|(bc)', 'ab'))
        self.assertEqual(match('(ab)|(bc)', 'bc'), self.boolre('(ab)|(bc)', 'bc'))
        self.assertEquals(match('(ab).(a|b)', 'aba'), self.boolre('(ab)(a|b)', 'aba'))
        self.assertEquals(match('(ab).(a|b)', 'abb'), self.boolre('(ab)(a|b)', 'abb'))
    def test_star_matching(self):
        self.assertEqual(match('a*', ''), self.boolre('a*', ''))
        self.assertEqual(match('a*', 'a'), self.boolre('a*', 'a'))
        self.assertEqual(match('(a*b).bc(bb)*', 'bbc'), self.boolre('(a*b)bc(bb)*', 'bbc'))
        self.assertEqual(match('((aa)*.(bb)*)*', 'aa'), self.boolre('((aa)*.(bb)*)*', 'aa'))
        self.assertEqual(match('((aa)*.(bb)*)*', 'bbc'), self.boolre('((aa)*.(bb)*)*', 'bbc'))
        self.assertEqual(match('((aa)*.(bb)*)*', 'aabb'), self.boolre('((aa)*.(bb)*)*', 'aabb'))
        self.assertEqual(match('((aa)*.(bb)*)*', ''), self.boolre('((aa)*.(bb)*)*', ''))
    def test_one_or_more(self):
        self.assertEqual(match('a?', 'a'), self.boolre('a?', 'a'))
        self.assertEqual(match('a?', ''), self.boolre('a?', ''))
        self.assertEqual(match('(ab)?.(ab)', 'ab'), self.boolre('(ab)?(ab)', 'ab'))
        self.assertEqual(match('(ab)?.(ab)', 'abab'), self.boolre('(ab)?(ab)', 'abab'))
        self.assertEqual(match('(a?b?c?(def)?)', 'acdef'), self.boolre('(a?b?c?(def)?)', 'acdef'))
        self.assertEqual(match('((abc)?.(abab)?)?', 'abcabab'), self.boolre('((abc)?(abab)?)?', 'abcabab'))
        self.assertEqual(match('(a?b?c?).((ab)?bc)', 'ababbc'), self.boolre('(a?b?c?)((ab)?bc)', 'ababbc'))
        self.assertEqual(match('andreas broby?', 'andreas'), self.boolre('andreas broby?', 'andreas'))
        self.assertEqual(match('Does this work: no? yes?', 'Does this work: no'), self.boolre('Does this work: no? yes?', 'Does this work: no'))


if __name__ == '__main__':
    unittest.main()
            
