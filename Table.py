from enum import Enum
from prettytable import PrettyTable


class Action(Enum):
    SHIFT = 1
    REDUCE = 2
    ACCEPT = 3


class ParseTable:
    def __init__(self, grammar, states, goto_dict):
        self.grammar = grammar
        self.states = states
        self.actions = []
        self.goto_dict = goto_dict
        self.terms = self.grammar.nonterminals.union(self.grammar.terminals)

    def is_accept(self, production):
        # if the production has the form: S' -> S.
        return production.lhs == self.grammar.enhanced_grammar_symbol \
               and production.rhs[0] == self.grammar.initial_symbol \
               and production.rhs[1] == '.'

    @staticmethod
    def is_reduce(production):
        """
        If the production has the form A -> aB.
        The dot is in the final position
        :param production: Production
        :return: void
        """
        return production.rhs[-1] == '.'

    def get_production_number(self, state):
        """
        Returns the index of the production from the grammar corresponding to the given state
        :param state: Set<Production>
        :return: index
        """
        initial_productions = self.grammar.productions
        for production in state.productions:
            index = 0
            for prod in initial_productions:
                if production.lhs == prod.lhs and production.rhs[:-1] == prod.rhs:
                    return index
                index += 1

    def construct(self):
        for state in self.states:
            check_action = []
            for production in state.productions:
                if state.get_size() == 1 and self.is_accept(production):
                    self.actions.append((Action.ACCEPT,))
                    continue
                if self.is_reduce(production):
                    check_action.append(1)
                else:
                    check_action.append(2)
            if check_action:
                # if all productions produced the same action, then add the corresponding action to the self.actions
                if check_action[1:] == check_action[:-1] and check_action[0] == 1:
                    # if all element of the check_action list are 1, then a REDUCE action was used
                    production_number = self.get_production_number(state)
                    self.actions.append((Action.REDUCE, production_number))
                elif check_action[1:] == check_action[:-1] and check_action[0] == 2:
                    # if all element of the check_action list are 2, then a SHIFT action was used
                    self.actions.append((Action.SHIFT,))
                else:
                    # if the productions generated different actions, then an error has occurred
                    raise Exception("Error in table")
        return self.actions

    def print_table(self):
        table_headers = [' ', 'Action']
        for term in self.terms:
            table_headers.append(term)
        table = PrettyTable(table_headers)

        table_state_names = []
        for state in self.states:
            table_state_names.append(state.name)

        table_action_names = []
        for action in self.actions:
            if action[0].name == 'REDUCE':
                table_action_names.append(action[0].name + " " + str(action[1]))
                continue
            table_action_names.append(action[0].name)

        for i in range(len(table_headers)):
            row = [table_state_names[i], table_action_names[i], " ", " ", " ", " ", " "]
            for index, term in enumerate(self.terms):
                try:
                    row[index + 2] = self.goto_dict[(table_state_names[i], term)]
                except KeyError:
                    pass

            table.add_row(row)
        print(table)

