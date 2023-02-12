from statemachine import StateMachine, State



# class Translator(StateMachine):
#     start_position = State("Start position", initial=True)
#     got_key_word = State("Got key word")
#     got_operation_symbol = State("Got operation symbol")
#     got_separator = State("Got separator")
#     got_identifier = State("Got identifier")

class SpaceBeforeAndAfterWordsMachine(StateMachine):
    got_alpha = State("Got alpha", initial=True)
    got_digit = State("Got digit")
    got_dot = State("Got dot")
    got_first_operator = State("Got first operator")
    got_second_operator = State("Gor second operator")
    got_space = State("Got space")
    got_separator = State("Got separator")

    symbols = (
        got_alpha.from_(got_alpha, got_digit, got_space, cond = "is_alpha")
        | got_alpha.from_(got_first_operator, got_second_operator, got_separator, cond = "is_alpha", on = "make_space")#
        | got_digit.from_(got_alpha, got_digit, got_dot, got_space, cond = "is_digit")
        | got_digit.from_(got_first_operator, got_second_operator, got_separator, cond = "is_digit", on = "make_space")#
        | got_dot.from_(got_digit, cond = "is_dot")
        | got_first_operator.from_(got_space, cond = "is_operator")
        | got_first_operator.from_(got_alpha, got_digit,got_separator, cond = "is_operator", on = "make_space")#
        | got_second_operator.from_(got_first_operator, cond = "is_operator")
        | got_space.from_(got_alpha, got_digit, got_separator, got_first_operator, got_second_operator, cond ="is_space")
        | got_separator.from_(got_space, cond = "is_separator")
        | got_separator.from_(got_alpha, got_digit, got_separator, got_first_operator, got_second_operator, cond = "is_separator", on = "make_space")#
    )

    # def __init__(self, line):
    #     self.line = line
    #     self.index_line = 0

    def is_alpha(self, symb):
        return symb.isalpha()
    def is_digit(self, char):
        return char.isdigit()
    def is_dot(self, char):
        return char == '.'
    def is_operator(self, char):
        operators = ['<','>','=','+','-','*','/']
        return char in operators
    def is_separator(self, char):
        separators = ['(',')','[',']','{','}','"',',',':']
        return char in separators
    def is_space(self, char):
        return char == ' '
    def make_space(self):
        print('тут пробел')

testmachine = SpaceBeforeAndAfterWordsMachine()

for s in "if a>b then b7 = 10":
    testmachine.symbols(s)
    print(testmachine)




# with open('python_code.txt') as f:
#     lines = f.readlines()
#     print(lines)