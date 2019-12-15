from enum import Enum


class Action(Enum):
    SHIFT = 1
    REDUCE = 2
    ACCEPT = 3


class ParseTable:
    def __init__(self, grammar, states):
        self.grammar = grammar
        self.states = states
        self.actions = []
        self.terms = self.grammar.nonterminals.union(self.grammar.terminals)


    def construct(self):
        pass


