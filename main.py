from analex import Analex
from anasin import Anasin

if __name__ == '__main__':

    a = Analex(
        input_str=open("SIN_ConjuntoText.txt", 'r').read()
    )

    tokens = a.execute()
    
    b = Anasin(
        tokens=tokens
    )

    print()
    print()
    print()

    b.execute()

