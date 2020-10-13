


class Analex:

    def __init__(self, input_str):
        self.input = input_str
        self.counter = -1 


    def previous(self):
        self.counter -= 1


    def next(self):
        self.counter += 1
        return self.input[self.counter]


    def execute(self):    
        while True:
            token, lexema = self._execute()
            print(token, '\t', lexema)
            if token == "FIM":
                break
        

    def _execute(self):
        state = 1
        lexema = ''

        operators = {
            '+': 'OP_SOM',
            '-': 'OP_SUB',
            '*': 'OP_MUL',
            '/': 'OP_DIV'
        }

        while True:
            ch = self.next()

            if state == 1:
                if ch.isdigit():
                    lexema += ch
                    state += 1
                
                elif ch in operators:
                    lexema += ch
                    return operators[ch], lexema

                elif ch == '\n':
                    return 'FIM', None

                elif ch in [' ', '\t']:
                    pass

                else:
                    return 'ERRO', None

            if state == 2:
                ch = self.next() 

                while ch.isdigit():
                    lexema += ch    
                    ch = self.next()
                self.previous()

                if ch == '.':
                    lexema += ch
                    state += 1
                    self.next()
                else:
                    return 'INT', lexema

            if state == 3:
                ch = self.next() 

                while ch.isdigit():
                    lexema += ch
                    ch = self.next()
                self.previous()

                return 'REAL', lexema

