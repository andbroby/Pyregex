from parsing_exceptions import MismatchedParentheses
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
    alphabet = [letter for letter in string.letters] + [str(i) for i in [0,1,2,3,4,5,6,7,8,9]]
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
            j = i + 1
            while j < len(infix) and (infix[j] in alphabet or infix[j] == '('):
                if infix[j] in alphabet:
                    output.append(infix[j])
                o1 = '.'
                while stack and stack[-1] in operators:
                    o2 = stack[-1]
                    if precedence[o2] >= precedence[o1]:
                        output.append(stack.pop())
                    else:
                        break
                stack.append(o1)
                if infix[j] == '(':
                    stack.append(infix[j])
                    j += 1
                    break
                j += 1
            i = j
            continue
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
            
            if e in unary_operators and i != len(infix)-1 and infix[i+1] in alphabet:
                o1 = '.'
                while stack and stack[-1] in operators:
                    o2 = stack[-1]
                    if precedence[o2] >= precedence[o1]:
                        output.append(stack.pop())
                    else:
                        break
                stack.append(o1)
                
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
            j = i+1
            if j < len(infix) and infix[j] not in operators:
                while stack and stack[-1] in operators:
                    o2 = stack[-1]
                    if precedence[o2] >= precedence['.']:
                        output.append(stack.pop())
                    else:
                        break
                stack.append('.')
            i = j
            continue
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
    alphabet = [letter for letter in string.letters] + [str(i) for i in [0,1,2,3,4,5,6,7,8,9]]

    for e in postfix:
        if e in alphabet:
            s = State(e)
            stack.append(NFAFragment(s, s))
        elif e == '.':
            f2 = stack.pop()
            f1 = stack.pop()
            f1.out.join(f2.start)
            f = NFAFragment(f1.start, f2.out)
            stack.append(NFAFragment(f1.start, f2.out))
        elif e == '|':
            f2 = stack.pop()
            f1 = stack.pop()
            print(f1.out)
            s = State('#e')
            s.join(f1.start)
            s.join(f2.start)
            stack.append(NFAFragment(s, f1.out.extend(f2.out)))
            
    final_state = State("#F")
    if stack:
        nfa = stack.pop()
        nfa.out.join(final_state)
    else:
        nfa = NFAFragment(final_state, final_state)
    return nfa

def match(pattern, string):
    pattern_postfix = re_to_postfix(pattern)
    nfa_frag = post2nfa(pattern_postfix)
    nfa = NFA(nfa_frag)
    return nfa.match(string)

if __name__ == "__main__":
    print(re_to_postfix(sys.argv[1]))
    #print(match(sys.argv[1], sys.argv[2]))
