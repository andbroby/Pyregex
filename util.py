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
        if __name__ == "__main__" and len(sys.argv) > 2:
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
            stack_element = stack.pop()
            while stack_element != '(':
                output.append(stack_element)
                stack_element = stack.pop()
        i += 1
    while stack:
        output.append(stack.pop())
    return output

if __name__ == "__main__":
    infix = sys.argv[1]
    postfix = re_to_postfix(infix)
    print("".join(postfix))
