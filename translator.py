from statemachine import StateMachine, State
import json

json_file = open('key_words.json')
key_words_dict = json.load(json_file)

json_file = open('operators.json')
operators_dict = json.load(json_file)

json_file = open('separators.json')
separators_dict = json.load(json_file)

ident_dict = {}

numbers_dict = {}

string_dict = {}

def is_digit(line: str):
    if line == '': return False
    for char in line:
        if not (char.isdigit() or char == '.'):
            return False
    return True

class Translator(StateMachine):
    got_alpha = State("Got alpha", initial=True)
    got_digit = State("Got digit")
    got_dot = State("Got dot")
    got_first_operator = State("Got first operator")
    got_second_operator = State("Got second operator")
    got_first_quot = State("Got first quotation ")
    got_second_quot = State("Got second quotation ")
    got_string = State("Got string")
    got_separator = State("Got separator")

    add_symbol = (
            got_alpha.from_(got_alpha, cond="is_alpha", on="add_char")
            | got_digit.from_(got_alpha, cond="is_digit", on="add_char")
            | got_digit.from_(got_digit, got_dot, cond="is_digit", on="add_char")
            | got_alpha.from_(got_digit, cond="is_alpha", on="add_char")

            | got_dot.from_(got_digit, cond="is_dot", on="add_char")

            | got_first_quot.from_(got_first_operator, got_second_operator, cond="is_quot", before="check_word", after="add_char")
            | got_string.from_(got_first_quot, got_string, cond="is_not_quot", on="add_char")
            | got_second_quot.from_(got_string, got_first_quot, before="add_char", after="check_word")

            | got_second_operator.from_(got_first_operator, cond = "is_operator", on = "add_char")

            | got_alpha.from_(got_separator,got_first_operator,got_second_operator, cond = "is_alpha", before="check_word", after = "add_char")
            | got_digit.from_(got_separator,got_first_operator,got_second_operator, cond = "is_digit", before="check_word", after = "add_char")
            | got_separator.from_(got_alpha,got_digit,got_separator,got_first_operator,got_second_operator,got_second_quot, cond = "is_separator", before="check_word", after = "add_char")
            | got_first_operator.from_(got_alpha,got_digit,got_separator,got_second_quot,cond = "is_operator", before="check_word", after = "add_char")
    )

    def __init__(self):
        self.current_word = ""
        self.tokens_list = []
        super(Translator, self).__init__()

    def is_alpha(self, char):
        return (char.isalpha() or char == '_')
    def is_digit(self, char):
        return is_digit(char)
    def is_separator(self,char):
        return char in separators_dict
    def is_operator(self,char):
        return char in operators_dict
    def is_dot(self,char):
        return char=='.'
    def is_quot(self, char):
        return char == '\'' or char == '"'
    def is_not_quot(self, char):
        return char != '\'' and char != '"'

    def check_word(self):
        if self.current_word in key_words_dict:
            self.tokens_list.append('W' + str(key_words_dict[self.current_word]))
        elif self.current_word in operators_dict:
            self.tokens_list.append('O'+str(operators_dict[self.current_word]))
        elif self.current_word in separators_dict:
            self.tokens_list.append('R' + str(separators_dict[self.current_word]))
        elif is_digit(self.current_word):
            if self.current_word not in numbers_dict:
                numbers_dict[self.current_word] = len(numbers_dict)
            self.tokens_list.append('N' + str(numbers_dict[self.current_word]))
        elif self.current_word.find('"') != -1 or self.current_word.find("'") != -1:
            if self.current_word not in string_dict:
                string_dict[self.current_word] = len(string_dict)
            self.tokens_list.append('S' + str(string_dict[self.current_word]))
        elif self.current_word != '':
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

with open('ident.json', 'w') as file:
    json.dump(ident_dict, file, indent=4)
with open('numbers.json', 'w') as file:
    json.dump(numbers_dict, file, indent=4)
with open('strings.json', 'w') as file:
    json.dump(string_dict, file, indent=4)
