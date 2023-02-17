from statemachine import StateMachine, State

key_words_dict = {'if': 0, 'or': 1, 'and': 2, 'for': 3, 'in': 4, 'then': 5, 'else': 6, 'while': 7, 'is': 8, 'elif': 9,
                  'def': 10, 'return':11, 'range':12}
operators_dict = {'<': 0, '>': 1, '<=': 2, '>=': 3, '+=': 4, '-=': 5, '*=': 6, '/=': 7, '=': 8, '==': 9, '+': 10,
                  '-': 11, '*': 12, '/': 13}
separators_dict = {'(': 0, ')': 1, '[': 2, ']': 3, '{': 4, '}': 5, '"': 6, ',': 7, ':': 8, "'": 9}

ident_dict = {}

numbers_dict = {}


class Translator(StateMachine):
    got_alpha = State("Got alpha", initial=True)
    got_digit = State("Got digit")
    got_dot = State("Got dot")
    got_first_operator = State("Got first operator")
    got_second_operator = State("Gor second operator")
    got_space = State("Got space")
    got_separator = State("Got separator")
    got_enter = State("Got enter", final=True)

    add_symbol = (
            got_alpha.from_(got_alpha, cond="is_alpha", on="add_char")  # проверка на идентификатор
            | got_digit.from_(got_alpha, cond="is_digit", on="add_char")
            | got_digit.from_(got_digit, cond="is_digit", on="add_char")
            | got_alpha.from_(got_digit, cond="is_alpha", on="add_char")

            | got_dot.from_(got_digit, cond="is_dot", on="add_char")
            | got_digit.from_(got_dot, cond="is_digit", on="add_char")

            | got_space.from_(got_alpha, got_digit, got_separator, got_first_operator, got_second_operator, cond = "is_space", before="check_word", after = "add_char")
            | got_space.from_(got_space, cond = "is_space", on = "add_char")

            | got_second_operator.from_(got_first_operator, cond = "is_operator", on = "add_char")

            | got_alpha.from_(got_space,got_separator,got_first_operator,got_second_operator, cond = "is_alpha", before="check_word", after = "add_char")
            | got_digit.from_(got_space,got_separator,got_first_operator,got_second_operator, cond = "is_digit", before="check_word", after = "add_char")
            | got_separator.from_(got_alpha,got_digit,got_separator,got_space,got_first_operator,got_second_operator, cond = "is_separator", before="check_word", after = "add_char")
            | got_first_operator.from_(got_alpha,got_digit,got_separator,got_space,cond = "is_operator", before="check_word", after = "add_char")

            | got_enter.from_(got_alpha,got_digit,got_separator,got_space, cond = "is_enter", before="check_word", after = "add_char")

    )

    def __init__(self):
        self.current_word = ""
        self.tokens_list = []
        super(Translator, self).__init__()

    def is_alpha(self, char):
        return (char.isalpha() or char == '_')
    def is_digit(self, char):
        return char.isdigit()
    def is_space(self,char):
        return char == ' '
    def is_separator(self,char):
        return char in separators_dict
    def is_operator(self,char):
        return char in operators_dict
    def is_enter(self,char):
        return char=='\n'
    def is_dot(self,char):
        return char=='.'

    def check_word(self):
        if self.current_word in key_words_dict:
            self.tokens_list.append('W' + str(key_words_dict[self.current_word]))
        elif self.current_word in operators_dict:
            self.tokens_list.append('O'+str(operators_dict[self.current_word]))
        elif self.current_word in separators_dict:
            self.tokens_list.append('R' + str(separators_dict[self.current_word]))
        elif self.current_word == ' ':
            self.tokens_list.append('Sp')
        elif self.current_word == '\n':
            self.tokens_list.append('En')
        elif self.current_word == '    ':
            self.tokens_list.append('Tb')
        elif self.current_word.isdigit():
            if self.current_word not in numbers_dict:
                numbers_dict[self.current_word] = len(numbers_dict)
            self.tokens_list.append('N' + str(numbers_dict[self.current_word]))
        else:
            if self.current_word not in ident_dict:
                ident_dict[self.current_word] = len(ident_dict)
            self.tokens_list.append('I' + str(ident_dict[self.current_word]))
        self.current_word = ""

    def add_char(self, char):
        self.current_word += char


output_lists = []
with open('python_code.txt','r') as file:
    for line in file:
        t = Translator()
        for symbol in line:
            t.add_symbol(symbol)
        output_lists.append(t.tokens_list)

with open('tokens.txt','w') as file:
    for line in output_lists:
        for value in line:
            file.write(value + " ")
        file.write('\n')


