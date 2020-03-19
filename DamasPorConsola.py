import unittest

class DamasPorConsola():
    def __init__(self):
        pass

    def intro(self):
        print("---------\n| DAMAS |\n---------")

    def output(self, gestorTurnos):
        print(gestorTurnos)

    def recogeCoordenada(self, mensaje):
        return int(input(mensaje).strip())
