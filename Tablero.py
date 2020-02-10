from Fichas import *
import unittest

class Tablero():
    def __init__(self, longTablero=8, equipos=("Blanco", "Negro")):
        self.LONG_TABLERO = 8
        self.EQUIPOS = equipos

        self.PEON = nuevoPeon()
        self.DAMA = nuevaDama(self.LONG_TABLERO)

        self.filaObjetivoDelEquipo = {self.EQUIPOS[0]:0, self.EQUIPOS[1]:self.LONG_TABLERO - 1}
        self.fichasDelEquipo = {e:{} for e in self.EQUIPOS}

    def equipoEnCoordenadas(self, x, y):
        EH = None
        for e, fichasEquipo in self.fichasDelEquipo.items():
            if (x, y) in fichasEquipo:
                return e
        else:
            return EH

    def __str__(self):
        string = "\n"

        for y in range(self.LONG_TABLERO):
            for x in range(self.LONG_TABLERO):
                ficha = None
                e = self.equipoEnCoordenadas(x, y)
                if e:
                    ficha = self.fichasDelEquipo[e][(x, y)]

                if ficha is self.PEON:
                    string += e[0].lower()
                elif ficha is self.DAMA:
                    string += e[0].capitalize()
                else:
                    string += "_"

            string += "\n"

        string = "|".join(string)
        string = "_" * (2*self.LONG_TABLERO + 1) + string

        return string

if __name__ == "__main__":
    unittest.main()
