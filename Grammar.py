import json

from Production import Production


class Grammar:
    def __init__(self):
        # set of nonterminals
        self.nonterminals = set()
        # set of terminals
        self.terminals = set()
        # set of Productions
        self.productions = []
        # initial symbol
        self.initial_symbol = None
        # epsilon symbol
        self.epsilon = "@"
        # starting symbol for enhanced grammar
        self.enhanced_grammar_symbol = 'Z'

    def get_non_terminal_productions(self, non_terminal) -> set:
        """
        Get set of all productions having non_terminal in lhs
        :param non_terminal: [A-Z]
        :return: Set<Productions>
        """
        result = set()
        for production in self.productions:
            if production.lhs == non_terminal:
                result.add(Production(production.lhs, production.rhs, add_dot=True))
        return result

    def read_file(self, filename) -> None:
        with open(filename) as json_data:
            data = json.load(json_data)
            self.nonterminals = set(data["nonterminals"])
            self.terminals = set(data["terminals"])
            for nonterminal in self.nonterminals:
                for rhs in data["productions"][nonterminal]:
                    production = Production(nonterminal, rhs.split())
                    self.productions.append(production)
            self.initial_symbol = data["initial_symbol"]

    def __str__(self) -> str:
        result = "Nonterminals: "
        result += str(self.nonterminals)
        result += "\nTerminals: "
        result += str(self.terminals)
        result += "\nProductions: "
        for index, production in enumerate(self.productions):
            result += str(index) + ": "
            result += str(production)
            result += ",\n"
        if len(self.productions) > 0:
            result = result[:-2]
        result += "\nInitial symbol: "
        result += str(self.initial_symbol)
        return result



