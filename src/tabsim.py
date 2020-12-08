
class SymbolTable:

    def __init__(self):
        self._table = []

    def add(self,symbol):
        s = self.find(symbol.id)

        if s is None or symbol.context != s.context:
            self._table.append(symbol)
        else:
            raise SymbolTable.Errors.IdExists(f"simbolo: {symbol}\ntabela\n{self.export()}")

    def remove(self,id):
        f = self.find(id)
        if f is not None:            
            self._table.remove()

    def use(self,id):
        f = self.find(id)
        if f is None:
            raise SymbolTable.Errors.NotDeclared(f"simbolo: {id}\ntabela\n{self.export()}")

    def find(self,id):
        for s in self._table:
            if s.id == id:
                return s
        return None

    def export(self):
        o = 'id\ttype\tdtype\tcontext\n'
        for s in self._table:
            o += str(s) + '\n'
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

    def __str__(self):
        return f"{self.id}\t{self.type}\t{self.data_type}\t{self.context}"