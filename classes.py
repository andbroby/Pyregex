import random

class State():
    def __init__(self, token):
        self.token = token
        self.transitions = {token:[]}
    def join(self, state):
        self.transitions[self.token].append(state)
    def __str__(self):
        return str(self.transitions)
    def __bool__(self):
        return False

class FinalState():
    def __bool__(self):
        return True

class NFAFragment():
    def __init__(self, start, out):
        self.start = start
        self.out = []
        if type(out) == list:
            self.out.extend(out)
        else:
            self.out.append(out)

class NFA():
    trying_epsilon = False
    
    def __init__(self, fragment):
        self.fragment = fragment
        self.current_states = [fragment.start]

    def has_valid_move(self, c):
        for state in self.current_states:
            if c in state.transitions:
                return True
        return False

    def is_at_epsilon(self):
        for state in self.current_states:
            if "#e" in state.transitions:
                return True
        return False

    def step(self, c, guess=None, epsilon_state=None):
        if self.is_at_epsilon():
            epsilon_state = self.current_states[:]
            choices = len(self.current_states[0].transitions["#e"])
            guess = random.randint(0, choices - 1)
            next_state = self.current_states[0].transitions["#e"][guess]
            self.current_states = [next_state]
            self.step(c, guess, epsilon_state)
            return True
            
        elif self.has_valid_move(c):
            new_states = []
            for state in self.current_states:
                if c in state.transitions:
                    new_states.extend(state.transitions[c])
            self.current_states = new_states
            return True

        elif guess is not None:
            new_guess = (guess + 1) % 2
            next_state = epsilon_state[0].transitions["#e"][new_guess]
            self.current_states = [next_state]
            self.step(c)
            return True
        return False
        
    def match(self, string):
        for c in string:
            if isinstance(self.current_states[0], FinalState):
                return True
            if not self.step(c):
                return False
        return any(self.current_states)
