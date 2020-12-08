
class SymbolTable:

    def __init__(self):
        self._table = []

    def add(self,symbol):
        s = self.find(symbol.id, symbol.context)

        if s is None or symbol.context != s[1].context:
            self._table.append(symbol)
        else:
            raise SymbolTable.Errors.IdExists(f"simbolo: {symbol}\ntabela\n{self.export()}")

    def remove(self,id,context,when=''):
        f = self.find(id,context)
        if f is not None:            
            self._table[f[0]].removed = True
            self._table[f[0]].removed_when = when

    def use(self,id,context):
        f = self.find(id,context)

        if f is not None and f[1].removed == True:
            print(f"\ntabela\n{self.export()}")
            raise SymbolTable.Errors.NotDeclared(f"ID not declared on this scope: {id}")
        
        if f is None:
            print(f"\ntabela\n{self.export()}")
            raise SymbolTable.Errors.NotDeclared(f"ID not declared: {id}")

    def find(self,id,context):
        # searches on local
        for i,s in enumerate(self._table):
            if s.id == id and s.context == context:
                    return (i,s)
        
        # searches on global
        for i,s in enumerate(self._table):
            if s.id == id and s.context == 'global':
                return (i,s)
        return None

    def export(self):
        o = '#\tid\ttype\tdtype\tcontext\tremoved\tremoved_when\n'
        for i,s in enumerate(self._table):
            o += f"{i}\t" + str(s) + '\n'
        return o

    class Errors:
        class IdExists(Exception):
            pass

        class NotDeclared(Exception):
            pass


class Symbol:
    def __init__(self, id, type, data_type, context):
        self.id = id
        self.type = type
        self.data_type = data_type
        self.context = context
        self.removed = False
        self.removed_when = None

    def __str__(self):
        return f"{self.id}\t{self.type}\t{self.data_type}\t{self.context}\t{self.removed}\t{self.removed_when}"