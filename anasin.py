

class Anasin:

    def __init__(self, tokens):
        self.tokens = tokens
        self.counter = 0

    def next(self):
        n = self.tokens[self.counter]
        self.counter += 1
        return n

    def get_current(self):
        """ return lexemma """
        return self.tokens[self.counter][1]

    def get_current_token(self):
        """ return token """
        return self.tokens[self.counter][0]

    def accept(self, expected, mode=None):
        """ check if a lexema or token is as expected
        
        params:
        expected - str | list<str>
        mode     - None | self.get_current | self.get_current_token
        """
        mode = self.get_current if mode == None else mode
        #print(expected, '\t', self.get_current_token(), '\t', self.get_current(), '\t', mode)

        if type(expected) == type([]) and mode() in expected:            
            print(f"{self.get_current_token()} {self.get_current()} ok!")
            self.next()

        elif expected == mode():
            print(f"{self.get_current_token()} {self.get_current()} ok!")
            self.next()

        else:
            print(f"{self.get_current_token()} {self.get_current()} nao ok :(")
            raise Exception (f'COMANDO {expected} ESPERADO QUANDO {self.get_current()} FOI FORNECIDO')
            
    def accept_token(self, expected):
        self.accept(expected, self.get_current_token)

    def execute(self):
        while self.counter < len(self.tokens):
            self.programa()

    # A partir daqui funcoes em ptbr devido ao 
    # requisito do trabalho    
    #         
    def programa(self):
        print('programa')
        self.lista_decl()

    def lista_decl(self):
        print('lista_decl')
        #lista-decl => decl list-decl | vazio

        if self.get_current() in ['CONST', 'VAR', 'SUB', 'FUNCTION']:
            self.decl()

        if self.get_current() == None:
            exit()


    def decl(self):
        print('decl')

        if self.get_current() == 'CONST':
            self.decl_const()
        elif self.get_current() == 'FUNCTION':            
            self.decl_func()
        elif self.get_current() == 'SUB':        
            self.decl_sub()
        elif self.get_current() == 'VAR':        
            self.decl_var()

    def decl_const(self):
        print('decl_const')
        # decl-const => CONST ID = literal ;
        self.accept('CONST')
        self.accept_token('ID')
        self.accept_token('OP_ATR')
        self.literal()
        self.accept_token('PV')

    def decl_var(self):
        print('decl_var')
        # decl-var => VAR espec-tipo lista-var ;
        self.accept('VAR')
        self.espec_tipo()
        self.lista_var()
        self.accept_token('PV')

    def espec_tipo(self):
        print('espec_tipo')
        # espec-tipo => INT | FLOAT | CHAR | BOOL | STRING
        self.accept(['INT', 'FLOAT', 'CHAR', 'BOOL', 'STRING', 'VOID'])

    def decl_sub(self):
        print('decl_sub')
        # decl-proc => SUB espec-tipo ID ( params ) bloco END-SUB 
        self.accept('SUB')
        self.espec_tipo()
        self.accept_token('ID')
        self.accept('(')
        self.params()
        self.accept(')')
        self.bloco()
        self.accept('END-SUB')

    def decl_func(self):
        print('decl_func')
        #decl-func => FUNCTION espec-tipo ID ( params ) bloco END-FUNCTION
        self.accept('FUNCTION')
        self.espec_tipo()
        self.accept_token('ID')
        self.accept('(')
        self.params()
        self.accept(')')
        self.bloco()
        self.accept('END-FUNCTION')

    def params(self):
        print('params')
        #params => lista-param | vazio
        if self.get_current() in [None, ')'] :
            return
        self.lista_param()
    
    def lista_param(self):
        print('lista_param')
        # lista-param => param lista-param'
        self.param()
        self.lista_param_linha()
    
    def lista_param_linha(self):
        print('lista_param_linha')
        #lista-param' => , param | vazio
        if self.get_current() == ',':
            self.accept(',')
            self.param()
        
    def param(self):
        print('param')
        #param => VAR espec-tipo lista-var BY mode
        self.accept('VAR')
        self.espec_tipo()
        self.lista_var()
        self.accept("BY")
        self.mode()

    def mode(self):
        print('mode')
        #mode => VALUE | REF
        self.accept(["VALUE", "REF"])

    def bloco(self):
        print('bloco')
        self.lista_com()

    def lista_com(self):
        # comando => cham-proc | com-atrib | com-selecao | com-repeticao 
        #                 | com-desvio | com-leitura | com-escrita | decl-var | decl-const
        print('lista_com')
        if self.get_current() in ['WHILE', 'DO', 'REPEAT', 'FOR', 'RETURN', 
                                    'BREAK', 'CONTINUE', 'SCAN', 'SCANLN'
                                    'PRINT', 'PRINTLN', 'IF', 'CONST', 'VAR'
                                    '('] or self.get_current_token() == 'ID':
            self.comando()
            self.lista_com()

    def comando(self):
        print('comando')

        if self.get_current_token() == 'ID':
            self.var_linha()

            if self.get_current() == '(':  
                self.cham_proc()
            elif self.get_current() == '[':
                self.var()
            else:
                self.com_atrib()

        if self.get_current() == 'VAR':
            self.decl_var()

        if self.get_current() == 'CONST':
            self.decl_const()

        if self.get_current() == 'IF':
            self.com_selecao()

        if self.get_current() in ['WHILE', 'DO', 'REPEAT', 'FOR']:
            self.com_repeticao()

        if self.get_current() in ['RETURN', 'BREAK', 'CONTINUE']:
            self.com_desvio()

        if self.get_current() in ['SCAN', 'SCANLN']:
            self.com_leitura()

        if self.get_current() in ['PRINT', 'PRINTLN']:
            self.com_escrita()
        #    

    def var_linha(self):
        print('var_linha')
        self.accept_token('ID')
        self.var()

    def var(self):
        print('var')
        if self.get_current() == '[':
            self.accept('[')
            self.exp_soma()
            self.accept(']')
            

    def cham_proc(self):
        print('cham_proc')
        self.cham_func()
        self.accept_token('PV')

    def cham_func(self):
        print('cham_func')
        self.accept('(')
        self.args()
        self.accept(')')

    def com_atrib(self):
        print('com_atrib')
        # self.accept('VAR')
        self.accept_token('OP_ATR')
        self.exp()
        self.accept_token('PV')

    def com_selecao(self):
        print('com_selecao')
        self.accept('IF')
        self.exp()
        self.accept('THEN')
        self.bloco()
        self.com_selecao_linha()

    def com_selecao_linha(self):
        print('com_selecao_linha')

        if self.get_current() == 'END-IF':
            self.accept('END-IF')
        else:
            self.accept('ELSE')
            self.bloco()
            self.accept('END-IF')

    def com_repeticao(self):
        print('com_repeticao')
        # com-repeticao => WHILE exp DO bloco LOOP | DO bloco WHILE exp ; | REPEAT bloco UNTIL exp ; | FOR ID = exp-soma TO exp-soma DO bloco NEXT
        if self.get_current() == 'WHILE':
            self.accept('WHILE')
            self.exp()
            self.accept('DO')
            self.bloco()
            self.accept('LOOP')

        elif self.get_current() == 'DO':
            
            self.accept('DO')
            self.bloco()
            self.accept('WHILE')
            self.exp()
            self.accept_token('PV')
        
        elif self.get_current() == 'REPEAT':
            self.accept('REPEAT')
            self.bloco()
            self.accept('UNTIL')
            self.exp()
            self.accept_token('PV')
        
        elif self.get_current() == 'FOR':
            self.accept('FOR')
            self.accept_token('ID')
            self.accept_token('OP_ATR')
            self.exp_soma()
            self.accept('TO')
            self.exp_soma()
            self.accept('DO')
            self.bloco()
            self.accept('NEXT')
            
    def com_desvio(self):
        print('com_desvio')
        if self.get_current() == 'RETURN':
            self.accept('RETURN')
            self.exp()
            self.accept_token('PV')

        elif self.get_current() == 'BREAK':
            self.accept('BREAK')
            self.accept_token('PV')
        
        elif self.get_current() == 'CONTINUE':
            self.accept('CONTINUE')
            self.accept_token('PV')
            
    def com_leitura(self):
        print('com_leitura')
        if self.get_current() == 'SCAN':
            self.accept('SCAN')

        elif self.get_current() == 'SCANLN':
            self.accept('SCANLN')

        self.accept('(')
        self.lista_var()
        self.accept(')')
        self.accept_token('PV')
            
    def com_escrita(self):
        print('com_escrita')
        if self.get_current() == 'PRINT':
            self.accept('PRINT')

        elif self.get_current() == 'PRINTLN':
            self.accept('PRINTLN')

        self.accept('(')
        self.lista_exp()
        self.accept(')')
        self.accept_token('PV')
        

    def lista_exp(self):
        print('lista_exp')
        #lista-exp => exp lista-exp'
        self.exp()
        self.lista_exp_linha()

    def lista_exp_linha(self):
        print('lista_exp_linha')
        #lista-exp' => , lista-exp | vazio
        if self.get_current() == None:
            return 
        self.accept(',')
        self.lista_exp()

    def exp(self):
        print('exp')
        # exp => exp-soma exp'
        self.exp_soma()
        self.exp_linha()
    
    def exp_linha(self):
        print('exp_linha')
        # exp' => op-relac exp-soma | vazio
        if self.get_current() in ['<=', '<', '>', '>=', '==', '<>']:
            self.op_relac()
            self.exp_soma()

    def op_relac(self):
        print('op_relac')
        # op-relac => <= | < | > | >= | == | <>
        self.accept(['<=', '<', '>', '>=', '==', '<>'])

    def exp_soma(self):
        print('exp_soma')
        # exp-soma => exp-mult exp-soma'
        self.exp_mult()
        self.exp_soma_linha()

    def exp_soma_linha(self):
        print('exp_soma_linha')
        #exp-soma' => op-soma exp-soma | vazio
        if self.get_current_token() in ['OP_SUM', 'OP_SUB', 'OP_OR']:
            self.op_soma()
            self.exp_soma()

    def op_soma(self):
        print('op_soma')
        # op-soma => + | - | OR
        self.accept_token(['OP_SUM', 'OP_SUB', 'OP_OR'])

    def exp_mult(self):
        print('exp_mult')
        # exp-mult => exp-simples exp-mult'
        self.exp_simples()
        self.exp_mult_linha()

    def exp_mult_linha(self):
        print('exp_mult_linha')
        #exp-mult' => op-mult exp-simples exp-mult' | vazio
        if self.get_current_token() in ['OP_MULT', 'OP_DIV', 'OP_AND'] or self.get_current() in ['MOD', 'DIV', 'AND']:
            self.op_mult()
            self.exp_simples()
            self.exp_mult_linha()

    def op_mult(self):
        print('op_mult')
        #op-mult => * | / | DIV | MOD | AND

        if self.get_current_token() in ['OP_MULT', 'OP_DIV', 'OP_AND']:
            self.accept_token(['OP_MULT', 'OP_DIV', 'OP_AND'])
        
        self.accept(['MOD', 'DIV', 'AND'])

    def exp_simples(self):
        print('exp_simples')
        # exp-simples => ( exp ) | var | cham-func | literal | op-unario exp
        
        if self.get_current() == '(':
            self.exp()
            self.accept(')')
        
        elif self.get_current_token() == 'ID':
            self.accept_token('ID')
            if self.get_current() == '[':
                self.var()
            elif self.get_current() == '(':
                self.cham_func()
            
        elif self.get_current_token() in ['INT', 'FLOAT', 'STRING'] or self.get_current() in ['TRUE', 'FALSE']:
            self.literal()
        
        elif self.get_current() in ['+', '-', 'NOT']:
            self.op_unario()
            self.exp()

    def literal(self):
        print('literal')
        # literal => NUMINT | NUMREAL | CARACTERE | STRING | valor-verdade

        if self.get_current_token() in ['INT', 'FLOAT', 'CHAR', 'STRING']:
            self.accept_token(['INT', 'FLOAT', 'CHAR', 'STRING'])
        else:
            self.valor_verdade()

    def valor_verdade(self):
        print('valor_Verdade')
        self.accept(['TRUE', 'FALSE'])

    def args(self):
        print('args')
        #args => lista-exp | vazio
        if self.get_current() == None:
            return
        
        self.lista_exp()

    def lista_var(self):
        print('lista_var')
        #lista-var => var lista-var'

        if self.get_current_token() == 'ID':
            self.var_linha()        
            self.lista_var_linha()

    def lista_var_linha(self):
        print('lista_var_linha')
        #lista-var' => , lista-var | vazio
        if self.get_current() == ',':
            self.accept(',')
            self.lista_var()

    def op_unario(self):
        print('op_unario')
        #op-unario => + | - | NOT
        if self.get_current_token() in ['OP_INC', 'OP_SNC']:
            self.accept_token(['OP_INC', 'OP_SNC'])
        else:
            self.accept('NOT')

    


    
    

      
        
