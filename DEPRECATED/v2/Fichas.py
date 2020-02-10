from collections import namedtuple

Ficha = namedtuple("Ficha", ["tipoFicha", "movMax", "puedeIrAtras"])

def nuevoPeon():
    return Ficha("Peon", movMax=1, puedeIrAtras=False)

def nuevaDama(longTablero):
    return Ficha("Dama", movMax=longTablero, puedeIrAtras=True)
