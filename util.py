import string

def re_to_postfix(infix):
    precedence = {
        '|': 3,
        '.': 2,
        '*': 1,
        '+': 1,
        '?': 1
    }
    operators = precedence.keys()
    alphabet = [letter for letter in string.letters] + [0,1,2,3,4,5,6,7,8,9]
    l_associative = ['|', '.', '*', '+', '-']
    r_associative = ['?']
    
    stack = []
    output = []

    i = 0;
    while i < len(infix):
        e = infix[i]
        print("Currently at " + infix)
        print("             " + len(infix[:i])*" " + "^")
        print("Output: " + str(output))
        print("Stack: " + str(stack))
        raw_input()
        if e in alphabet:
            output.append(e)
            j = i + 1
            while j < len(infix) and infix[j] in alphabet:
                stack.append('.')
                output.append(infix[j])
                j += 1
            i = j
            continue
        elif e in operators:
            o1 = e
            while stack and stack[-1] in operators:
                o2 = stack[-1]
                if o1 in l_associative and precedence[o2] >= precedence[o1] or \
                   o1 in r_associative and precedence[o2] > precedence[o1]:
                    output.append(stack.pop())
                else:
                    break
            stack.append(e)
        elif e == '(':
            if not stack or stack[-1] != '.':
                infix = infix[:i] + '.' + infix[i:len(infix)]
                continue
            stack.append(e)
            i += 1
            j = i
            while j < l and infix[j] in alphabet:
                j += 1
            if infix[i:j]:
                output.append(infix[i:j])
            i = j
            continue
        elif e == ')':
            stack_element = stack.pop()
            while stack_element != '(':
                output.append(stack_element)
                stack_element = stack.pop()
        i += 1
    while stack:
        output.append(stack.pop())
    return output

