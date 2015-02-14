class State():
    def __init__(self, state1, state2, token):
        self.token = token

class Fragment():
    def __init__(self, start_state, out_states):
        self.start_state = start_state
        self.out_states = out_states
        
class NFA():
    transition_table = {}
