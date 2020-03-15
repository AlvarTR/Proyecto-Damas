from collections import namedtuple

Ficha = namedtuple("Ficha", ["tipoFicha", "movMax", "puedeIrAtras", "impresion"])

def nuevoPeon():
    return Ficha("Peon", movMax=1, puedeIrAtras=False, impresion=str.lower)

def nuevaDama(longTablero):
    return Ficha("Dama", movMax=longTablero, puedeIrAtras=True, impresion=str.upper)
