from collections import namedtuple

Ficha = namedtuple("Ficha", ["movMax", "puedeIrAtras", "equipo"])


class Peon(Ficha):
    def __repr__(self):
        return self.equipo[0].lower()

class Dama(Ficha):
    def __repr__(self):
        return self.equipo[0].capitalize()


def nuevoPeon(equipo):
    return Peon(movMax=1, puedeIrAtras=False, equipo=equipo)

def nuevaDama(equipo, filasTablero):
    return Dama(movMax=filasTablero, puedeIrAtras=True, equipo=equipo)
