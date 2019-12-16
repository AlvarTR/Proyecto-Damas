from collections import namedtuple

PEON = "PEON"
DAMA = "Dama"

class Ficha(namedtuple("Ficha", ["tipo", "movMax", "puedeIrAtras", "equipo"])):
    def __repr__(self):
        string = self.equipo[0]
        if self.tipo == PEON:
            string = string.lower()
        elif self.tipo == DAMA:
            string = string.capitalize()
        return string


def nuevoPeon(equipo):
    return Ficha(tipo=PEON, movMax=1, puedeIrAtras=False, equipo=equipo)

def nuevaDama(equipo, filasTablero):
    return Ficha(tipo=DAMA, movMax=filasTablero, puedeIrAtras=True, equipo=equipo)
