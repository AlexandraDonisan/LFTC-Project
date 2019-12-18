from ParseError import ParseError
from Grammar import Grammar
from LRZeroParser import LRZeroParser
from Production import Production
from Scanner import Scanner


def main():
    # grammar = Grammar()
    # grammar.read_file("inputs\grammar_lab4.json")
    # print(grammar)

    # pif, codification_table = get_pif()

    grammar = Grammar()
    grammar.nonterminals = {'S', 'A'}
    grammar.terminals = {'a', 'b', 'c'}
    grammar.productions.append(Production('S', ['a', 'A']))
    grammar.productions.append(Production('A', ['b', 'A']))
    grammar.productions.append(Production('A', ['c']))
    grammar.initial_symbol = 'S'

    parser = LRZeroParser(grammar, "abbc")

    try:
        parser.step1()
        parser.step2()
        parser.step3()
        # parser.step3_pif(pif, codification_table)
        parser.derivations_string()
    except ParseError as e:
        print(e)


def get_pif():
    codification_table_file = "inputs\codification_table_lab4.in"
    program_file = "inputs\input_lab4.in"
    scanner = Scanner(codification_table_file, program_file)
    scanner.scan()

    codification_table_list = [key for key in scanner.codification_table.keys()]
    print("Condification Table: " + str(codification_table_list))
    print(str(scanner.st))
    print("PIF: " + str(scanner.pif))

    return scanner.pif, codification_table_list


def get_simple_grammar():
    grammar = Grammar()
    grammar.nonterminals = {'S', 'A'}
    grammar.terminals = {'a', 'b', 'c'}
    grammar.productions.append(Production('S', ['a', 'A']))
    grammar.productions.append(Production('A', ['b', 'A']))
    grammar.productions.append(Production('A', ['c']))
    grammar.initial_symbol = 'S'
    return grammar

main()