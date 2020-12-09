from src.analex import Analex
from src.anasin import Anasin


if __name__ == '__main__':


    a = Analex(
        #input_str=open("docs/SIN_ConjuntoText.txt", 'r').read()
        #input_str=open("docs/SEM_ConjuntoTest.txt", 'r').read()
        input_str=open("docs/MEPA_test.txt", 'r').read()
    )

    tokens = a.execute()
    
    b = Anasin(
        tokens=tokens
    )

    b.execute()

