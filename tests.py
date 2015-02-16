import unittest
import re
from util import re_to_postfix, match
from parsing_exceptions import MismatchedParentheses, UnrecognizedToken

class Re_to_postfix_test(unittest.TestCase):
    def test_concatenation(self):
        self.assertEqual(re_to_postfix('a.b.a.b'), ['a', 'b', '.', 'a', '.', 'b', '.'])
        self.assertEqual(re_to_postfix('a.(b.b)*.a'), ['a', 'b', 'b', '.', '*', '.', 'a', '.'])
        self.assertEqual(re_to_postfix('(a.(b.(c)))'), ['a', 'b', 'c', '.', '.'])
        self.assertEqual(re_to_postfix('()'), [])

    def test_exceptions(self):
        with self.assertRaises(MismatchedParentheses):
            re_to_postfix('(a.(b.c)))')
            re_to_postfix('(')

class Re_matching_tests(unittest.TestCase):
    def boolre(self, pattern, string):
        return bool(re.match(pattern, string))
    
    def test_concatenation_matching(self):
        self.assertEqual(match('a.b', 'ab'), self.boolre('ab', 'ab'))
        self.assertEqual(match('a.(b.b).(c.d)', 'a.b.b.c.d'), self.boolre('a(bb)(cd)', 'abbcd'))
        self.assertEqual(match('', ''), self.boolre('',''))
        self.assertEqual(match('(a.(b))', 'a.b'), self.boolre('(a(b))', 'ab'))
        self.assertEqual(match('a.b(c.d).b.a.(d.c(c.d))', 'abcdbadccd'), self.boolre('ab(cd)ba(dc(cd))', 'abcdbadccd'))
        self.assertEqual(match('a.a.a.a.(b).(b).c.(d)', 'aaaabbcd'), self.boolre('aaaa(b)(b)c(d)', 'aaaabbcd'))

    def test_alternation_matching(self):
        self.assertEqual(match('a|b', 'a'), self.boolre('a|b', 'a'))
        self.assertEqual(match('a|b', 'b'), self.boolre('a|b', 'b'))
        self.assertEqual(match('(a.b)|(b.c)', 'ab'), self.boolre('(ab)|(bc)', 'ab'))
        self.assertEqual(match('(a.b)|(b.c)', 'bc'), self.boolre('(ab)|(bc)', 'bc'))
        self.assertEquals(match('(a.b).(a|b)', 'aba'), self.boolre('(ab)(a|b)', 'aba'))
        self.assertEquals(match('(a.b).(a|b)', 'abb'), self.boolre('(ab)(a|b)', 'abb'))
    def test_star_matching(self):
        self.assertEqual(match('a*', ''), self.boolre('a*', ''))
        self.assertEqual(match('a*', 'a'), self.boolre('a*', 'a'))
        self.assertEqual(match('(a*b).b.c.(b.b)*', 'bbc'), self.boolre('(a*b)bc(bb)*', 'bbc'))
        self.assertEqual(match('((a.a)*.(b.b)*)*', 'aa'), self.boolre('((aa)*.(bb)*)*', 'aa'))
        self.assertEqual(match('((a.a)*.(b.b)*)*', 'bbc'), self.boolre('((aa)*.(bb)*)*', 'bbc'))
        self.assertEqual(match('((a.a)*.(b.b)*)*', 'aabb'), self.boolre('((aa)*.(bb)*)*', 'aabb'))
        self.assertEqual(match('((a.a)*.(b.b)*)*', ''), self.boolre('((aa)*.(bb)*)*', ''))
    def test_one_or_more(self):
        self.assertEqual(match('a?', 'a'), self.boolre('a?', 'a'))
        self.assertEqual(match('a?', ''), self.boolre('a?', ''))
        self.assertEqual(match('(a.b)?.(a.b)', 'ab'), self.boolre('(ab)?(ab)', 'ab'))
        self.assertEqual(match('(a.b)?.(a.b)', 'abab'), self.boolre('(ab)?(ab)', 'abab'))
        self.assertEqual(match('(a?.b?.c?.(d.e.f)?)', 'acdef'), self.boolre('(a?b?c?(def)?)', 'acdef'))
        self.assertEqual(match('((a.b.c)?.(a.b.a.b)?)?', 'abcabab'), self.boolre('((abc)?(abab)?)?', 'abcabab'))
        self.assertEqual(match('(a?.b?.c?).((a.b)?.bc)', 'ababbc'), self.boolre('(a?b?c?)((ab)?bc)', 'ababbc'))
        self.assertEqual(match('a.n.d.r.e.a.s. .b.r.o.b.y?', 'andreas'), self.boolre('andreas broby?', 'andreas'))
        self.assertEqual(match('D.o.e.s. .t.h.i.s. .w.o.r.k.:. .n.o?. .y.e.s?', 'Does this work: no'), self.boolre('Does this work: no? yes?', 'Does this work: no'))


if __name__ == '__main__':
    unittest.main()
            
