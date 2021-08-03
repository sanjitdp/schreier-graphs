from sympy.combinatorics import Permutation
from copy import deepcopy


# class to represent a single symbol
class Symbol(str):
    inverse = False

    def __str__(self):
        if self.inverse:
            return "(~" + self + ")"
        else:
            return self

    def __invert__(self):
        if str(self) == "1":
            return self

        inverse = deepcopy(self)
        inverse.inverse = ~self.inverse
        return inverse


# function to clean pairs of a symbol and its inverse in a word,
# takes in a list of symbols and outputs a list of symbols
def clean_inverse_pairs(expression):
    for index, symbol in enumerate(expression):
        if index < len(expression) - 1:
            if expression[index + 1] == ~symbol:
                expression.pop(index + 1)
                expression.pop(index)
                return clean_inverse_pairs(expression)


# function to remove all occurrences of 1 given a nontrivial word,
# takes in a list of symbols and outputs a list of symbols
def simplify(expression):
    simplified = [symbol for symbol in expression if str(symbol) != "1"]
    clean_inverse_pairs(simplified)

    if len(simplified) == 0:
        simplified = [Symbol("1")]

    return simplified


# class to represent expression - list of symbols
class Expression:
    def __init__(self, expr_list):
        self.expression = simplify(expr_list)

    def __mul__(self, other):
        product = simplify(self.expression + other.expression)
        return product

    def __invert__(self):
        inverse_expression = [~element for element in reversed(self.expression)]
        return simplify(inverse_expression)

    def __str__(self):
        expression_string = ""
        for symbol in self.expression:
            expression_string += str(symbol)
        return expression_string

    def to_parse(self):
        expression_string = ""
        for symbol in self.expression:
            expression_string += str(symbol)
            expression_string += "*"

        if expression_string[-1] == "*":
            expression_string = expression_string[:-1]

        return expression_string


# class that represents a generator object,
# composed of a sympy permutation and an action
class Generator:
    def __init__(self, action, permutation, basic_generator=False):
        if type(permutation) == Permutation:
            self.permutation = permutation
        else:
            self.permutation = Permutation([permutation, [ACTION_SIZE - 1]])

        max_value = max(permutation)

        if basic_generator:
            self.action = []
            for j in range(0, ACTION_SIZE):
                self.action.append(Expression(["1"]))

            self.action[max_value] = Expression([action])

        else:
            self.action = action

    def __mul__(self, other):
        permutation_product = self.permutation * other.permutation
        action_product = [Expression(other.permutation(self.action)[j] * other.action[j])
                          for j in range(0, ACTION_SIZE)]
        return Generator(action_product, permutation_product)

    def __pow__(self, power):
        exponent_temp = Generator(self.action, self.permutation)

        for j in range(0, power - 1):
            exponent_temp *= self

        return exponent_temp

    def __invert__(self):
        inverse_permutation = ~self.permutation
        inverse_action = inverse_permutation([Expression(~a) for a in self.action])
        return Generator(inverse_action, inverse_permutation)


# function to determine if a word is the identity,
# returns tuple containing whether a word is the identity,
# and if so, at what recursion level it becomes the identity
def is_identity(generator, identity_level):
    if generator.permutation.is_Identity:
        for expression in generator.action:
            if str(expression) == "1":
                continue
            else:
                recurse = is_identity(eval(expression.to_parse()), identity_level + 1)
                if not recurse[0]:
                    return False, identity_level
                else:
                    identity_level = recurse[1]

        return True, identity_level
    else:
        return False, identity_level


# constants that represent group generators and word
ACTION_SIZE = 3
x = Generator(Symbol("x"), [0, 1], basic_generator=True)
y = Generator(Symbol("y"), [0, 2], basic_generator=True)
WORD = ((x ** 2) * (y ** 2) * ((~x) ** 2) * ((~y) ** 2)) ** 3


# prints simplified word and whether the word is the identity
if __name__ == "__main__":
    print("word:", WORD.permutation, end=" ")

    print("[", end="")

    for i in range(0, len(WORD.action)):
        if i == len(WORD.action) - 1:
            print(WORD.action[i], end="")
            continue
        print(WORD.action[i], end=", ")

    print("]\n")

    print("The given word is ", end="")
    identity = is_identity(WORD, 1)
    if identity[0]:
        print("the identity. This word becomes the identity at recursion level", identity[1], end=".\n")
    else:
        if not identity[0]:
            print("not the identity.")
