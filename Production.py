import re


class Production:
    def __init__(self, lhs, rhs, shift=False, add_dot=False):
        self.lhs = lhs  # [A-Z]
        self.rhs = rhs.copy()  # [a-zA-Z.]+ -> List<Chars>
        if shift:
            index_of_dot = self.rhs.index('.')
            self.rhs[index_of_dot], self.rhs[index_of_dot + 1] = self.rhs[index_of_dot + 1], self.rhs[index_of_dot]
        if add_dot:
            self.rhs.insert(0, '.')

    def is_final(self) -> bool:
        """
        Return true if dot is at the final position
        :return: bool
        """
        return self.rhs[-1] == '.'

    def has_non_terminal(self, grammar) -> chr:
        """
        Return non_terminal after dot or None otherwise
        :return: [A-Z] or None
        """
        index_of_dot = self.rhs.index('.')
        if self.rhs[index_of_dot + 1] in grammar.nonterminals:
            return self.rhs[index_of_dot + 1]
        # if re.match("[A-Z]", self.rhs[index_of_dot + 1]):
        return None

    def has_X(self, X) -> bool:
        """
        Check if X is next of dot
        :param X: char 𝚺 ∪ N ( terminals or non-terminals )
        :return: bool
        """
        index_of_dot = self.rhs.index('.')
        if index_of_dot == len(self.rhs) - 1:
            return False
        return self.rhs[index_of_dot + 1] == X

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Production):
            return self.lhs == o.lhs and self.rhs == o.rhs
        return False

    def __hash__(self) -> int:
        """
        !!!!!!!!
        :return:
        """
        return super().__hash__()

    def __str__(self) -> str:
        return self.lhs + " -> " + str(self.rhs)
