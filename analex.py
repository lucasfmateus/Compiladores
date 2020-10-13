

class Analex:

    def __init__(self, input_str):
        self.input = input_str
        self.counter = -1
        self.state = None

    def previous(self):
        self.counter -= 1

    def next(self):
        self.counter += 1

        if self.counter == len(self.input):
            return '\0'
        return self.input[self.counter]

    def execute(self):
        result = []
        print('state', '\t', 'token', '\t', 'lexeme')
        while True:
            token, lexema = self._execute()
            print(self.state, '\t', token, '\t', lexema)
            result.append((token, lexema))
            if token == "FIM":
                return result

    def _execute(self):
        self.state = 1
        lexema = ''

        operators = {
            '++': 'OP_INC',
            '+=': 'OP_MEQ',
            '+': 'OP_SUM',
            '--': 'OP_SNC',
            '-=': 'OP_SEQ',
            '-': 'OP_SUB',
            '*': 'OP_MUL',
            '/': 'OP_DIV',
            '=': 'OP_ATR',
            '==': 'OP_EQ',
            '<': 'OP_LES',
            '<=': 'OP_LEQ',
            '>': 'OP_GRT',
            '>=': 'OP_GEQ',
            '%': 'OP_MOD',
            '!=': 'OP_NEQ',
            '&&': 'OP_AND',
            '||': 'OP_OR',
            '[': 'OP_CA',
            ']': 'OP_CF',
            '(': 'OP_PA',
            ')': 'OP_PF'
        }

        separator = [' ', '\t', '\n', '\r', ';', '\0']
        reserved = [",", "VAR", "END", "INT", "FLOAT", "CHAR", "SCAN", "SCANLN", "PRINT", "PRINTLN", "END-IF", "THEN", "ELSE", "DIV", "MOD", "END-SUB", "END-FUNCTION",  "VOID",
                    "BOOL", "STRING", "CONST", "REF", "BY", "SUB", "FUNCTION", "IF", "FOR", "WHILE", "DO", "RETURN", "BREAK", "CONTINUE", "GOTO", "TRUE", "FALSE", "VALUE", "LOOP", "NEXT"
                    "REPEAT", "UNTILL"]

        while True:
            ch = self.next()

            if self.state == 1:
                if ch in ['+', '-', '*', '/', '=', '<', '>', '!', '&', '|', '[',']','(', ')']:
                    lexema += ch
                    self.state += 1

                if ch == '\0':
                    return 'FIM', None

                if ch in separator:
                    if ch == ';':
                        return 'PV', ch
                    pass

                if ch.isdigit():
                    lexema += ch
                    self.state += 2

                if ch.isalpha() or ch == '$' or ch == '_' or ch == ',':
                    lexema += ch
                    self.state += 4

                if ch == "'":
                    lexema += ch
                    self.state += 5

                if ch == '"':
                    lexema += ch
                    self.state += 6                    

            elif self.state == 2:

                if lexema in ['+', '-', '>', '<', '=', '!'] and ch == '=':
                    lexema += ch
                    return operators[lexema], lexema

                elif lexema in ['+', '-', '|', '&'] and lexema == ch:
                    lexema += ch
                    return operators[lexema], lexema

                else:
                    self.previous()
                    return operators[lexema], lexema

            elif self.state == 3:

                while ch.isdigit():
                    lexema += ch
                    ch = self.next()

                if ch == '.':
                    lexema += ch
                    self.state += 1

                elif ch in separator:
                    self.previous()
                    return 'INT', lexema

                else:
                    lexema += ch
                    return 'ER1', f'{lexema} -> CARACTERE {ch} INVALIDO'

            elif self.state == 4:

                while ch.isdigit():
                    lexema += ch
                    ch = self.next()

                if ch in separator:
                    self.previous()
                    return 'FLOAT', lexema

                else:
                    lexema += ch
                    return 'ER1', f'{lexema} -> CARACTERE {ch} INVALIDO'

            elif self.state == 5:

                while ch not in separator:
                    lexema += ch
                    ch = self.next()

                self.previous()
                if lexema.upper() in reserved:
                    return 'RWORD', lexema.upper()
                else:
                    if False in list(map(lambda x: x.isdigit() or x.isalpha() or x == '$' or x == '_', lexema)):
                        return 'ER2', lexema
                    else:
                        return 'ID', lexema

            elif self.state == 6:
                
                while ch != "'":
                    lexema += ch
                    ch = self.next()

                lexema += ch
                if len(lexema) == 3:
                    return 'CHAR', lexema
                
                else:
                    return 'ER1', f'{lexema} -> CARACTERE INVALIDO'

            elif self.state == 7:
                
                while ch != '"' and ch != '\n':
                    lexema += ch
                    ch = self.next()

                if ch == '\n':
                    return 'ER3', 'CARACTERE \\n NAO PERMITIDO EM STRINGS'
            
                lexema += ch
                return 'STRING', lexema

