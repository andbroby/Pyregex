import random

class State():
    def __init__(self, token):
        self.token = token
        self.transitions = {token:[]}
    def join(self, state, token=None):
        if token:
            if token in self.transitions:
                self.transitions[token].append(state)
            else:
                self.transitions[token] = [state]
        else:
            self.transitions[self.token].append(state)
    def __str__(self):
        return str(self.transitions)

class FinalState(State):
    pass

class NFAFragment():
    def __init__(self, start, out):
        self.start = start
        self.out = []
        if type(out) == list:
            self.out.extend(out)
        else:
            self.out.append(out)
        

class NFA():
    saved_states_stack = []
    
    def __init__(self, fragment):
        self.fragment = fragment
        self.current_states = [fragment.start]

    def has_valid_move(self, c):
        for state in self.current_states:
            if c in state.transitions and state.transitions[c]:
                return True
        return False

    def is_at_epsilon(self):
        for state in self.current_states:
            if "#e" in state.transitions:
                return True
        return False
    
    def step(self, string, i = 0, epsilon_state=None, guess=None, saved_index=None):
        c = None
        
        if isinstance(self.current_states[0], FinalState):
            return
        elif not self.is_at_epsilon and i >= len(string):
            return

        if i < len(string):
            c = string[i]
        else:
            c = ''
        
        if self.is_at_epsilon():
            saved_state = {}
            saved_state['state'] = self.current_states[:]
            saved_state['index'] = i
            if c is not None and c in self.current_states[0].transitions:
                self.current_states = self.current_states[0].transitions[c]
                return self.step(string, i+1)
            choices = len(self.current_states[0].transitions["#e"])
            guess = random.randint(0, choices - 1)
            saved_state['guess'] = guess
            next_state = self.current_states[0].transitions["#e"][guess]
            self.saved_states_stack.append(saved_state)
            self.current_states = [next_state]
            return self.step(string, i)
        elif self.has_valid_move(c):
            new_states = []
            for state in self.current_states:
                if c in state.transitions:
                    new_states.extend(state.transitions[c])
            self.current_states = new_states
            return self.step(string, i+1)
        elif self.saved_states_stack:
            saved_NFA_state = self.saved_states_stack.pop()
            saved_index = saved_NFA_state["index"]
            saved_state = saved_NFA_state["state"]
            saved_guess = saved_NFA_state["guess"]
            new_guess = (saved_guess + 1) % len(saved_state[0].transitions["#e"])
            next_state = saved_state[0].transitions["#e"][new_guess]
            self.current_states = [next_state]
            return self.step(string, saved_index)
        return
        
    def match(self, string):
        self.step(string)
        for state in self.current_states:
            if isinstance(state, FinalState):
                return True
        return False
