#!/usr/bin/python3

from parsing_exceptions import MismatchedParentheses, UnrecognizedToken
from classes import *
import string
import sys

def re_to_postfix(infix):
    precedence = {
        '|': 1,
        '.': 2,
        '*': 3,
        '+': 3,
        '?': 3
    }
    operators = precedence.keys()
    alphabet = [letter for letter in string.ascii_letters] + [str(i) for i in [0,1,2,3,4,5,6,7,8,9]] + [' ']
    binary_operators = ['|', '.']
    unary_operators = ['?', '*', '+']
    
    stack = []
    output = []

    read_entries = []

    i = 0;
    while i < len(infix):
        if __name__ == "__main__" and sys.argv[-1] == '--v':
            print(infix)
            print(" "*i + "^")
            print("Stack: " + str(stack))
            print("Output: " + str(output))
            raw_input()
        e = infix[i]
        if e in alphabet:
            output.append(e)
        elif e in operators:
            o1 = e
            while stack and stack[-1] in operators:
                o2 = stack[-1]
                if o1 in binary_operators and precedence[o2] >= precedence[o1] or \
                   o1 in unary_operators and precedence[o2] > precedence[o1]:
                    output.append(stack.pop())
                else:
                    break
            stack.append(e)
        elif e == '(':
            stack.append(e)
        elif e == ')':
            try:
                stack_element = stack.pop()
                while stack_element != '(':
                    output.append(stack_element)
                    stack_element = stack.pop()
            except IndexError:
                error_msg = "No matching left parenthesis for the right parenthesis at {}".format(i)
                raise MismatchedParentheses(error_msg)
        else:
            raise UnrecognizedToken()
        i += 1
    while stack:
        top = stack.pop()
        if top == '(':
            raise MismatchedParentheses("Unclosed left parenthesis.")
        output.append(top)
    return output

def post2nfa(postfix):
    """ Takes in a postfix expression and converts it into an NFA"""

    stack = []
    states = []
    alphabet = [letter for letter in string.ascii_letters] + [str(i) for i in [0,1,2,3,4,5,6,7,8,9]] + [' ']
    for e in postfix:
        if e in alphabet:
            s = State(e)
            stack.append(NFAFragment(s, s))
        elif e == '.':
            f2 = stack.pop()
            f1 = stack.pop()
            for out_state in f1.out:
                out_state.join(f2.start)
            f = NFAFragment(f1.start, f2.out)
            stack.append(NFAFragment(f1.start, f2.out))
        elif e == '|':
            f2 = stack.pop()
            f1 = stack.pop()
            s = State('#e')
            s.join(f1.start)
            s.join(f2.start)
            f1.out.extend(f2.out)
            stack.append(NFAFragment(s, f1.out))
        elif e == '*':
            f = stack.pop()
            s = State('#e')
            s.join(f.start, f.start.token)
            for out_state in f.out:
                out_state.transitions = {"#e": [s]}
            stack.append(NFAFragment(s,s))
        elif e == '?':
            f = stack.pop()
            s = State("#e")
            s.join(f.start)
            f.out.append(s)
            f1 = NFAFragment(s, f.out)
            stack.append(f1)
        elif e == '+':
            f = stack.pop()
            s = State('#e')
            for out in f.out:
                out.join(s)
            f1 = NFAFragment(f.start, s)
            stack.append(f1)
    final_state = FinalState("#F")
    if stack:
        final_frag = stack.pop()
        for state in final_frag.out:
            state.join(final_state)
        nfafrag = NFAFragment(final_frag.start, final_frag.out)
    else:
        nfafrag = NFAFragment(final_state, final_state)
    nfa = NFA(nfafrag)
    return nfa

def match(pattern, string):
    pattern_postfix = re_to_postfix(pattern)
    nfa = post2nfa(pattern_postfix)
    return nfa.match(string)

if __name__ == "__main__":
    print(re_to_postfix(sys.argv[1]))
    #print(match(sys.argv[1], sys.argv[2]))
