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
        return EH

    def fichasPorEquipo(self, equipo):
        EH = -1
        if equipo not in self.EQUIPOS:
            return EH
        return len(self.fichasDelEquipo[equipo])

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

    def __copy__(self):
        t = Tablero(self.LONG_TABLERO, self.EQUIPOS)
        t.PEON = self.PEON
        t.DAMA = self.DAMA

        t.filaObjetivoDelEquipo = self.filaObjetivoDelEquipo.copy()
        t.fichasDelEquipo = self.fichasDelEquipo.copy()
        return t

    def copia(self):
        return self.__copy__()

class PruebasTablero(unittest.TestCase):
    def setUp(self):
        self.t = Tablero()

    def testCopia(self):
        self.t.fichasDelEquipo["Blanco"][(0, 0)] = self.t.PEON
        self.t.fichasDelEquipo["Negro"][(1, 1)] = self.t.PEON

        copia = self.t.copia()
        self.t.fichasDelEquipo["Blanco"] = {}
        self.t.fichasDelEquipo["Negro"] = {}
        for e in self.t.fichasDelEquipo:
            self.assertEqual(len(self.t.fichasDelEquipo[e]), 0)

        for e in copia.fichasDelEquipo:
            self.assertEqual(len(copia.fichasDelEquipo[e]), 1)


if __name__ == "__main__":
    unittest.main()
