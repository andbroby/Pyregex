def shunting_yard(infix):
    precedence = {
        '^': 3,
        '*': 2,
        '/': 2,
        '+': 1,
        '-': 1
    }
    operators = precedence.keys()
    l_associative = ['*', '/', '+', '-']
    r_associative = ['^']
    
    stack = []
    output = []

    i = 0;
    l = len(infix)
    while i < l:
        e = infix[i]
        if e.isdigit():
            j = i
            while j < l and infix[j].isdigit():
                j += 1
            e = infix[i:j]
            i = j
            output.append(e)
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

print(shunting_yard("3+4*2/(1-5)^2^3"))
print(shunting_yard("3+4*3+42^(3*2)+54"))
