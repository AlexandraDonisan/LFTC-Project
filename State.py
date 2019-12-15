class State:
    def __init__(self, productions, name):
        self.productions = productions  # Set<Production>
        self.name = name  # int

    def add_production(self, production):
        """
        Add new production to the set of states
        :param production: Production
        :return: void
        """
        self.productions.add(production)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, State) or o.get_size() != self.get_size():
            return False

        for prod in o.productions:
            found = False
            for p in self.productions:
                if p == prod:
                    found = True
            if not found:
                return False
        return True

    def get_size(self) -> int:
        return len(self.productions)

    def __str__(self) -> str:
        result = "s" + str(self.name) + " = { "
        for prod in self.productions:
            result += "[ " + str(prod) + " ] "
        result += " }\n"
        return result
