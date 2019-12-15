from ParseError import ParseError
from Production import Production
from State import State
from Table import Action, ParseTable
from prettytable import PrettyTable


class LRZeroParser:
    def __init__(self, grammar, input_string):
        self.input_string = input_string
        self.grammar = grammar
        self.states = []
        self.goto_dict = {}  # {(state, term) : state}
        self.actions = []   # List<(Action, )>

    def step1(self):
        self.states.append(self.closure({Production('Z', ['.', 'S'])}))
        for state in self.states:
            for x in self.grammar.nonterminals.union(self.grammar.terminals):
                result_state = self.goto(state, x)
                if len(result_state.productions) != 0:
                    # add key (state, x) with the corresponding value state.name to the goto_dict
                    self.goto_dict[(state.name, x)] = result_state.name
                    if result_state not in self.states:
                        # add new state to the result if it is not already in the set
                        print(result_state)
                        self.states.append(result_state)

        print("Goto is: " + str(self.goto_dict))

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

    def step2(self):
        parse_table = ParseTable(self.grammar, self.states, self.goto_dict)
        self.actions = parse_table.construct()
        parse_table.print_table()

    @staticmethod
    def add_table_row(table, work_stack, input_stack, output_band):
        if len(output_band) == 0:
            output_band_print = 'E'
        else:
            output_band_print = "".join([str(elem) for elem in output_band[::-1]])
        table.add_row(["".join(map(lambda pair: pair[0] + str(pair[1]), work_stack)),
                       "".join(input_stack[::-1]),
                       output_band_print])

    def step3(self):
        """
        Parse input and return list of productions used to generate the input sequence
        :return: output_band: List<Int>
        """
        # initialize table
        table = PrettyTable()
        table.field_names = ["Work Stack", "Input Stack", "Output Band"]
        # initialize working, input stacks and output band
        work_stack = [('$', 0)]    # list of tuple (character from grammar, state number)
        input_stack = [char for char in self.input_string[::-1]]  # list of characters from grammar
        input_stack.insert(0, '$')
        output_band = []    # list of production numbers
        while True:
            self.add_table_row(table, work_stack, input_stack, output_band)
            top_work = work_stack[-1]
            if self.actions[top_work[1]][0] == Action.SHIFT:
                top_input = input_stack[-1]
                try:
                    goto_state = self.goto_dict[(top_work[1], top_input)]
                except KeyError:
                    raise ParseError("Could not find goto({top_work[1]}, {top_input})")
                work_stack.append((top_input, goto_state))
                input_stack = input_stack[:-1]
            elif self.actions[top_work[1]][0] == Action.REDUCE:
                production_number = self.actions[top_work[1]][1]
                production = self.grammar.productions[production_number]
                work_characters = map(lambda pair: pair[0], work_stack)
                rhs = "".join(production.rhs)
                work_sequence = "".join(work_characters)
                index = work_sequence.index(rhs)
                # remove tuples matching production
                work_stack = work_stack[:index]
                # add tuple matching rhs of production used in reduce
                goto_lhs = self.goto_dict[(work_stack[-1][1], production.lhs)]
                work_stack.append((production.lhs, goto_lhs))
                output_band.append(production_number)
            elif self.actions[top_work[1]][0] == Action.ACCEPT:
                print(table)
                break
        return output_band[::-1]
