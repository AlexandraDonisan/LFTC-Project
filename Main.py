from Grammar import Grammar
from Table import ParseTable
from LRZeroParser import LRZeroParser
from Production import Production


def main():
    grammar = Grammar()
    grammar.nonterminals = {'S', 'A'}
    grammar.terminals = {'a', 'b', 'c'}
    grammar.productions.append(Production('S', ['a', 'A']))
    grammar.productions.append(Production('A', ['b', 'A']))
    grammar.productions.append(Production('A', ['c']))
    grammar.initial_symbol = 'S'

    print("Hello World")

    parser = LRZeroParser(grammar, "abbc")
    # parser.step1()
    # for state in parser.states:
    #     print(state)

    parser.step3()

    parse_table = ParseTable(grammar, parser.states, parser.goto_dict)
    actions = parse_table.construct()
    # print(actions)
    print(parse_table.print_table())


main()
