class Phonebook:
    def __init__(self) -> None:
        self.numbers = dict[str, str]()

    def add(self, name, number):
        self.numbers[name] = number
        
    def lookup(self, name):
        return self.numbers[name]