import unittest

class DamasPorConsola():
    def __init__(self):
        pass

    def intro(self):
        print("---------\n| DAMAS |\n---------")

    def output(self, gestorTurnos):
        print(gestorTurnos)

    def recogeCoordenada(self, mensaje):
        numero = None
        while numero is None:
            numero = input(mensaje).strip()
            try:
                numero = int(numero)
            except ValueError:
                print("Numero no valido")
                numero = None

        return numero
