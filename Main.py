from Grammar import Grammar
from LRZeroParser import LRZeroParser
from Production import Production
from State import State


def main():
    grammar = Grammar()
    grammar.nonterminals = {'S', 'A'}
    grammar.terminals = {'a', 'b', 'c'}
    grammar.productions.add(Production('S', ['a', 'A']))
    grammar.productions.add(Production('A', ['b', 'A']))
    grammar.productions.add(Production('A', ['c']))
    grammar.initial_symbol = 'S'

    print("Hello World")

    parser = LRZeroParser(grammar)
    parser.step1()
    for state in parser.states:
        print(state)


main()
