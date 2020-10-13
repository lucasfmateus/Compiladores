from analex import Analex


if __name__ == '__main__':

    a = Analex(
        input_str=open("conjuntoTeste.txt", 'r').read()
    )

    tokens = a.execute()

