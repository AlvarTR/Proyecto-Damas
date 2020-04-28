import sys

class DamasPorConsola():
    def __init__(self):
        pass

    def intro(self):
        print("---------\n| DAMAS |\n---------")

    def output(self, gestorTurnos):
        print(gestorTurnos)

    def recogeCoordenada(self, mensaje):
        numero = None
        i = 0
        while numero is None:
            numero = input(mensaje).strip().lower()
            try:
                numero = int(numero)
            except ValueError:
                print("Numero no valido")
                numero = None

                i += 1
                if i >= 3:
                    sys.exit(1)

        return numero
