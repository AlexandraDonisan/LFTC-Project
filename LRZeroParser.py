from Production import Production
from State import State


class LRZeroParser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.states = []

    def step1(self):
        self.states.append(self.closure({Production('Z', ['.', 'S'])}))
        for state in self.states:
            for x in self.grammar.nonterminals.union(self.grammar.terminals):
                print("goto( " + str(state.name) + " " + x + " )")
                s = self.goto(state, x)
                if len(s.productions) != 0 and s not in self.states:
                    print(s)
                    self.states.append(s)

    def goto(self, state, X):
        """
        :param state: State
        :param X: 𝚺 ∪ N ( terminals or non-terminals )
        :return: State
        """
        result = set()
        for production in state.productions:
            # add Productions with X after dot and shift dot
            if production.has_X(X):
                result.add(Production(production.lhs, production.rhs, shift=True))
        return self.closure(result)

    def closure(self, I):
        """
        :param I: Set<Production>
        :return: State
        """
        state = State(set(), None)
        for production in I:
            if production.is_final():  # If dot is at the end
                state.add_production(production)
            else:
                non_terminal = production.has_non_terminal()
                if non_terminal:  # If dot is before a [A-Z]
                    state.add_production(Production(production.lhs, production.rhs))
                    # add all Productions of grammar having non_terminal in lhs
                    all_productions = self.grammar.get_non_terminal_productions(non_terminal)
                    for prod in all_productions:
                        state.add_production(prod)
                else:
                    state.add_production(production)  # If dot is before a [a-z]

        # check for any existing state in canonical collection of states
        for s in self.states:
            if s == state:
                return s

        # create new state
        state.name = len(self.states)
        return state
