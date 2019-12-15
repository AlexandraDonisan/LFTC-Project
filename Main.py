from ParseError import ParseError
from Grammar import Grammar
from LRZeroParser import LRZeroParser
from Production import Production


def main():
    grammar = Grammar()
    grammar.nonterminals = {'S', 'A'}
    grammar.terminals = {'a', 'b', 'c'}
    grammar.productions.append(Production('S', ['a', 'A']))
    grammar.productions.append(Production('A', ['b', 'A']))
    grammar.productions.append(Production('A', ['a']))
    grammar.initial_symbol = 'S'

    parser = LRZeroParser(grammar, "abbc")

    try:
        parser.step1()
        parser.step2()
        parser.step3()
    except ParseError as e:
        print(e)

main()
