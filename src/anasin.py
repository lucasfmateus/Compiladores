
from src.tabsim import Symbol, SymbolTable


class Anasin:

    def __init__(self, tokens):
        self.tokens = tokens
        self.counter = 0
        self.output = open('docs/anasin.log.csv', 'w')
        self.output.write('token,lexema,log\n')
        self.symbol_table = SymbolTable()
        self.last_type = None
        self.last_context = 'global'
        self.last_context_aux = 'global'
        self.last_data_type = None
        self.last_operation = None
        self.stack = {}

    def add_symbol(self):
        """Add symbol to Symbol Table.

        Always call it after accept functions"""
        id = self.tokens[self.counter - 1][1]

        s = Symbol(
            id = id,
            type = self.last_type,
            context = self.last_context,
            data_type = self.last_data_type
        )
        self.symbol_table.add(symbol=s)       

        if self.last_type in ['VAR','SUB','FUNC']:
            try:
                self.stack[self.last_context_aux].append(id)
            except KeyError:
                self.stack[self.last_context_aux] = [id]
    
    def remove_symbols(self,when=''):        
        if self.last_context_aux in self.stack:
            for i in self.stack[self.last_context_aux]:
                self.symbol_table.remove(id=i,context=self.last_context,when=when)

            del self.stack[self.last_context_aux]

    def get_aux_context(self):
        return  f"{self.last_context}-{self.last_operation}"

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

    def log(self, token='', lexema='', log=''):
        self.output.write(f"{token},{lexema},{log}\n")
        print("{:10}".format(token), "{:10}".format(lexema), "{:10}".format(log))

    def accept(self, expected, mode=None):
        """ check if a lexema or token is as expected
        
        params:
        expected - str | list<str>
        mode     - None | self.get_current | self.get_current_token

        return:
        LEXEMMA if mode is None or `self.get_current`. Otherwise, TOKEN.
        """
        mode = self.get_current if mode == None else mode
        #print(expected, '\t', self.get_current_token(), '\t', self.get_current(), '\t', mode)

        if type(expected) == type([]) and mode() in expected:   
            cur = mode()         
            self.log(token=self.get_current_token(), lexema= self.get_current(), log ='ok!')
            self.next()
            return cur

        elif expected == mode():
            cur = mode() 
            self.log(token=self.get_current_token(), lexema= self.get_current(), log ='ok!')
            self.next()
            return cur

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
        self.log(log ='programa')
        self.last_context = 'global'   #semantic-action
        self.lista_decl()
        

    def lista_decl(self):
        self.log(log ='lista_decl')
        #lista-decl => decl list-decl | vazio

        if self.get_current() in ['CONST', 'VAR', 'SUB', 'FUNCTION']:
            self.decl()

        if self.get_current() == None:            
            self.remove_symbols('fim')
            print("Tabela de simbolos")
            print(self.symbol_table.export())            
            exit()


    def decl(self):
        self.log(log ='decl')
        self.last_operation = 'decl'

        if self.get_current() == 'CONST':
            self.decl_const()
        elif self.get_current() == 'FUNCTION':            
            self.decl_func()
        elif self.get_current() == 'SUB':        
            self.decl_sub()
        elif self.get_current() == 'VAR':       
            self.decl_var()

        self.last_operation = None

    def decl_const(self):
        self.log(log ='decl_const')
        last = self.last_type   #semantic-action
        self.last_type = 'CONST' #semantic-action

        # decl-const => CONST ID = literal ;

        self.accept('CONST')
        self.accept_token('ID')
        self.add_symbol()   #semantic-action
        self.accept_token('OP_ATR')
        self.literal()
        self.accept_token('PV')
        self.last_type = last #semantic-action

    def decl_var(self):
        self.log(log ='decl_var')

        # decl-var => VAR espec-tipo lista-var ;
        self.accept('VAR')
        last = self.last_type #semantic-action
        self.last_type = 'VAR'#semantic-action
        self.espec_tipo()
        self.lista_var()
        self.accept_token('PV')
        self.last_type =last #semantic-action

    def espec_tipo(self):
        self.log(log ='espec_tipo')

        # espec-tipo => INT | FLOAT | CHAR | BOOL | STRING
        tipo = self.accept(['INT', 'FLOAT', 'CHAR', 'BOOL', 'STRING', 'VOID'])
        self.last_data_type = tipo

    def decl_sub(self):
        self.log(log ='decl_sub')
        last_context = self.last_context
        last_type = self.last_type #semantic-action
        self.last_type = 'SUB' #semantic-action

        # decl-proc => SUB espec-tipo ID ( params ) bloco END-SUB 
        self.accept('SUB')
        self.espec_tipo()
        self.accept_token('ID')
        self.add_symbol()
        self.last_context = self.tokens[self.counter - 1][1] #semantic-action
        self.last_context_aux = self.get_aux_context() #semantic-action
        self.accept('(')
        self.params()
        self.accept(')')
        self.bloco()
        self.accept('END-SUB')

        self.remove_symbols('end-sub') #semantic-action
        self.last_context = last_context #semantic-action
        self.last_context_aux = last_context #semantic-action
        self.last_func_sub_id = '' #semantic-action        
        self.last_type = last_type #semantic-action

    def decl_func(self):
        self.log(log ='decl_func')
        last_context = self.last_context #semantic-action
        last_type = self.last_type #semantic-action
        self.last_type = 'FUNC' #semantic-action

        #decl-func => FUNCTION espec-tipo ID ( params ) bloco END-FUNCTION
        self.accept('FUNCTION')
        self.espec_tipo()
        self.accept_token('ID')
        self.add_symbol()   #semantic-action
        self.last_context = self.tokens[self.counter - 1][1] #semantic-action
        self.last_context_aux = self.get_aux_context() #semantic-action
        self.accept('(')
        self.params() 
        self.accept(')')
        self.bloco()
        self.accept('END-FUNCTION')
        
        
        self.last_func_sub_id = '' #semantic-action
        self.last_context = last_context #semantic-action
        self.last_context_aux = last_context #semantic-action
        self.last_type = last_type #semantic-action                

    def params(self):
        self.log(log='params')
        
        #params => lista-param | vazio
        if self.get_current() in [None, ')'] :
            return
        self.lista_param()
    
    def lista_param(self):
        self.log(log ='lista_param')

        # lista-param => param lista-param'
        self.param()
        self.lista_param_linha()
    
    def lista_param_linha(self):
        self.log(log ='lista_param_linha')

        #lista-param' => , param | vazio
        if self.get_current() == ',':
            self.accept(',')
            self.param()
        
    def param(self):
        self.log(log ='param')
        last = self.last_type #semantic-action
        self.last_type = 'VAR' #semantic-action

        #param => VAR espec-tipo lista-var BY mode

        self.accept('VAR')
        self.espec_tipo()
        self.lista_var()
        self.accept("BY")
        self.mode()
        self.last_type = last #semantic-action

    def mode(self):
        self.log(log ='mode')

        #mode => VALUE | REF
        self.accept(["VALUE", "REF"])

    def bloco(self):
        last = self.last_context_aux    #semantic-action
        self.last_context_aux = self.get_aux_context() #semantic-action
        self.log(log ='bloco')
        self.lista_com()

        self.remove_symbols(f'fim {self.last_context_aux}')
        self.last_context_aux = last #semantic-action


    def lista_com(self):
        # comando => cham-proc | com-atrib | com-selecao | com-repeticao 
        #                 | com-desvio | com-leitura | com-escrita | decl-var | decl-const
        self.log(log ='lista_com')

        if self.get_current() in ['WHILE', 'DO', 'REPEAT', 'FOR', 'RETURN', 
                                    'BREAK', 'CONTINUE', 'SCAN', 'SCANLN',
                                    'PRINT', 'PRINTLN', 'IF', 'CONST', 'VAR',
                                    '('] or self.get_current_token() == 'ID':
            
            self.comando()
            self.lista_com()

    def comando(self):
        self.log(log ='comando')
        
        if self.get_current_token() == 'ID':
            last = self.last_operation #semantic-action
            self.last_operation = 'attrib' #semantic-action
            self.var_linha()
            self.last_operation = last #semantic-action

            if self.get_current() == '(':  
                self.cham_proc()
            elif self.get_current() == '[':
                self.var()
            else:
                self.com_atrib()

        if self.get_current() == 'VAR':
            last = self.last_operation #semantic-action
            self.last_operation = 'decl' #semantic-action            
            self.decl_var()
            self.last_operation = last #semantic-action            

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
        

    def var_linha(self):
        self.log(log ='var_linha')
        self.accept_token('ID')   #semantic-action
        
        if self.last_operation == 'decl': 
            self.add_symbol()
        else:
            self.symbol_table.use(
                id=self.tokens[self.counter - 1][1],
                context=self.last_context
            )

        self.var()

    def var(self):
        self.log(log ='var')
        if self.get_current() == '[':
            self.accept('[')
            self.exp_soma()
            self.accept(']')
            

    def cham_proc(self):
        self.log(log ='cham_proc')
        self.cham_func()
        self.accept_token('PV')

    def cham_func(self):
        self.log(log ='cham_func')
        self.accept('(')
        self.args()
        self.accept(')')

    def com_atrib(self):
        self.log(log ='com_atrib')
        self.accept_token('OP_ATR')
        last = self.last_operation      #semantic-action
        self.last_operation = 'attrib'  #semantic-action
        self.exp()
        self.accept_token('PV')
        self.last_operation = last      #semantic-action

    def com_selecao(self):
        self.log(log ='com_selecao')
        self.accept('IF')
        self.exp()
        self.accept('THEN')
        last = self.last_operation   #semantic-action
        self.last_operation = 'cond' #semantic-action        
        self.bloco()
        self.com_selecao_linha()
        self.last_operation = last #semantic-action

    def com_selecao_linha(self):
        self.log(log ='com_selecao_linha')

        if self.get_current() == 'END-IF':
            self.accept('END-IF')
        else:
            self.accept('ELSE')
            self.bloco()
            self.accept('END-IF')

    def com_repeticao(self):
        self.log(log ='com_repeticao')

        # com-repeticao => WHILE exp DO bloco LOOP | DO bloco WHILE exp ; | REPEAT bloco UNTIL exp ; | FOR ID = exp-soma TO exp-soma DO bloco NEXT
        if self.get_current() == 'WHILE':
            self.accept('WHILE')
            last = self.last_operation    #semantic-action
            self.last_operation = 'while' #semantic-action
            self.exp()
            self.accept('DO')
            self.bloco()
            self.accept('LOOP')
            self.last_operation = last   #semantic-action

        elif self.get_current() == 'DO':
            
            self.accept('DO')
            self.bloco()
            self.accept('WHILE')
            last = self.last_operation    #semantic-action
            self.last_operation = 'while' #semantic-action
            self.exp()
            self.accept_token('PV')
            self.last_operation = last    #semantic-action
        
        elif self.get_current() == 'REPEAT':
            self.accept('REPEAT')
            self.bloco()
            self.accept('UNTIL')
            last = self.last_operation     #semantic-action
            self.last_operation = 'repeat' #semantic-action            
            self.exp()
            self.accept_token('PV')
            self.last_operation = last      #semantic-action
        
        elif self.get_current() == 'FOR':
            self.accept('FOR')
            last = self.last_operation     #semantic-action
            self.last_operation = 'for'    #semantic-action             
            self.accept_token('ID')
            self.accept_token('OP_ATR')
            self.exp_soma()
            self.accept('TO')
            self.exp_soma()
            self.accept('DO')
            self.bloco()
            self.accept('NEXT')
            self.last_operation = last      #semantic-action
            
    def com_desvio(self):
        self.log(log ='com_desvio')

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
        self.log(log ='com_leitura')

        if self.get_current() == 'SCAN':
            self.accept('SCAN')

        elif self.get_current() == 'SCANLN':
            self.accept('SCANLN')

        last = self.last_operation #semantic-action
        self.last_operation = 'leitura' #semantic-action

        self.accept('(')
        self.lista_var()
        self.accept(')')
        self.accept_token('PV')

        self.last_operation = last #semantic-action
            
    def com_escrita(self):
        self.log(log ='com_escrita')

        if self.get_current() == 'PRINT':
            self.accept('PRINT')

        elif self.get_current() == 'PRINTLN':
            self.accept('PRINTLN')

        self.accept('(')
        self.lista_exp()
        self.accept(')')
        self.accept_token('PV')
        

    def lista_exp(self):
        self.log(log ='lista_exp')
        #lista-exp => exp lista-exp'
        self.exp()
        self.lista_exp_linha()

    def lista_exp_linha(self):
        self.log(log ='lista_exp_linha')

        #lista-exp' => , lista-exp | vazio
        if self.get_current() == ',':
            self.accept(',')
            self.lista_exp()

    def exp(self):
        self.log(log ='exp')
        # exp => exp-soma exp'
        self.exp_soma()
        self.exp_linha()
    
    def exp_linha(self):
        self.log(log ='exp_linha')
        # exp' => op-relac exp-soma | vazio
        if self.get_current() in ['<=', '<', '>', '>=', '==', '<>']:
            self.op_relac()
            self.exp_soma()

    def op_relac(self):
        self.log(log ='op_relac')
        # op-relac => <= | < | > | >= | == | <>
        self.accept(['<=', '<', '>', '>=', '==', '<>'])

    def exp_soma(self):
        self.log(log ='exp_soma')
        # exp-soma => exp-mult exp-soma'
        self.exp_mult()
        self.exp_soma_linha()

    def exp_soma_linha(self):
        self.log(log ='exp_soma_linha')
        #exp-soma' => op-soma exp-soma | vazio
        if self.get_current_token() in ['OP_SUM', 'OP_SUB', 'OP_OR']:
            self.op_soma()
            self.exp_soma()

    def op_soma(self):
        self.log(log ='op_soma')
        # op-soma => + | - | OR
        self.accept_token(['OP_SUM', 'OP_SUB', 'OP_OR'])

    def exp_mult(self):
        self.log(log ='exp_mult')
        # exp-mult => exp-simples exp-mult'
        self.exp_simples()
        self.exp_mult_linha()

    def exp_mult_linha(self):
        self.log(log ='exp_mult_linha')
        #exp-mult' => op-mult exp-simples exp-mult' | vazio
        if self.get_current_token() in ['OP_MULT', 'OP_DIV', 'OP_AND'] or self.get_current() in ['MOD', 'DIV', 'AND']:
            self.op_mult()
            self.exp_simples()
            self.exp_mult_linha()

    def op_mult(self):
        self.log(log ='op_mult')
        #op-mult => * | / | DIV | MOD | AND

        if self.get_current_token() in ['OP_MULT', 'OP_DIV', 'OP_AND']:
            self.accept_token(['OP_MULT', 'OP_DIV', 'OP_AND'])
        
        self.accept(['MOD', 'DIV', 'AND'])

    def exp_simples(self):
        self.log(log ='exp_simples')
        # exp-simples => ( exp ) | var | cham-func | literal | op-unario exp
        
        if self.get_current() == '(':
            self.exp()
            self.accept(')')
        
        elif self.get_current_token() == 'ID':
            self.accept_token('ID')
            self.symbol_table.use(
                id=self.tokens[self.counter -1][1],
                context=self.last_context) #semantic-action

            if self.get_current() == '[':
                self.var()
            elif self.get_current() == '(':
                self.cham_func()
            
        elif self.get_current_token() in ['INT', 'FLOAT', 'STRING', 'CHAR'] or self.get_current() in ['TRUE', 'FALSE']:
            self.literal()
        
        elif self.get_current() in ['+', '-', 'NOT']:
            self.op_unario()
            self.exp()

    def literal(self):
        self.log(log ='literal')
        # literal => NUMINT | NUMREAL | CARACTERE | STRING | valor-verdade

        if self.get_current_token() in ['INT', 'FLOAT', 'CHAR', 'STRING']:
            self.accept_token(['INT', 'FLOAT', 'CHAR', 'STRING'])
        else:
            self.valor_verdade()

    def valor_verdade(self):
        self.log(log ='valor_verdade')
        self.accept(['TRUE', 'FALSE'])

    def args(self):
        self.log(log ='args')
        #args => lista-exp | vazio
        if self.get_current() == None:
            return
        
        self.lista_exp()

    def lista_var(self):
        self.log(log ='lista_var')
        #lista-var => var lista-var'

        if self.get_current_token() == 'ID':
            self.var_linha()        
            self.lista_var_linha()

    def lista_var_linha(self):
        self.log(log ='lista_var_linha')
        #lista-var' => , lista-var | vazio
        if self.get_current() == ',':
            self.accept(',')
            self.lista_var()

    def op_unario(self):
        self.log(log ='op_unario')
        #op-unario => + | - | NOT
        if self.get_current_token() in ['OP_INC', 'OP_SNC']:
            self.accept_token(['OP_INC', 'OP_SNC'])
        else:
            self.accept('NOT')

    


    
    

      
        
