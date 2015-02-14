class State():
    def __init__(self, token):
        self.token = token
        self.transitions = {token:[]}
    def join(self, state):
        self.transitions[self.token].append(state)
    def __str__(self):
        return str(self.transitions)

class NFAFragment():
    def __init__(self, start, out):
        self.start = start
        self.out = out

class NFA():
    def __init__(self, fragment):
        self.fragment = fragment
        self.current_states = [fragment.start]

    def has_valid_move(self, c):
        for state in self.current_states:
            if c in state.transitions:
                return True
        return False

    def step(self, c):
        if self.has_valid_move(c):
            new_states = []
            for state in self.current_states:
                if c in state.transitions:
                    new_states.extend(state.transitions[c])
            self.current_states = new_states
            return True
        return False
        
    def match(self, string):
        for c in string:
            if not self.step(c):
                return False
        return True
