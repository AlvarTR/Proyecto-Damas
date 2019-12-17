from collections import namedtuple

Peon = namedtuple("Peon", ["movMax", "puedeIrAtras"])
Dama = namedtuple("Dama", ["movMax", "puedeIrAtras"])

def nuevoPeon():
    return Peon(movMax=1, puedeIrAtras=False)

def nuevaDama(longTablero):
    return Dama(movMax=longTablero, puedeIrAtras=True)
