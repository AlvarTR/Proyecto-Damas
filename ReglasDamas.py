from Tablero import *
from Fichas import *
import unittest

def tableroConFichasIniciales(longTablero=8, relacionCasillasFichas=0.4, equipos=("Blanco", "Negro")):
    t = Tablero(longTablero, equipos)
    filasPeones = int(longTablero*relacionCasillasFichas)

    primeraFila = 0
    ultimaFila = t.LONG_TABLERO - 1

    for e in t.filaObjetivoDelEquipo:
        inicial = primeraFila
        final = ultimaFila
        if t.filaObjetivoDelEquipo[e] == primeraFila:
            inicial = t.LONG_TABLERO - filasPeones
        elif t.filaObjetivoDelEquipo[e] == ultimaFila:
            final = primeraFila + filasPeones-1 #-1 para hacer 0 -> self.FILAS_PEONES-1 (2) en el bucle

        for y in range(inicial, final+1): #+1 porque "final" es el ultimo valor que queremos rellenar
            for x in iter(x for x in range(t.LONG_TABLERO) if t.posicionValida(x, y)):
                t.fichasDelEquipo[e][(x, y)] = t.PEON
    return t

class PruebasFichasIniciales(unittest.TestCase):
    def setUp(self):
        self.t = tableroConFichasIniciales()

    def testFichasInicialesBienPuestas(self):
        print(self.t)
        for e in self.t.fichasDelEquipo:
            self.assertEqual(len(self.t.fichasDelEquipo[e]), 12)

    def testFichasPorEquipo(self):
        for e in self.t.EQUIPOS:
            self.assertEqual(self.t.fichasPorEquipo(e), 12)
        self.assertEqual(self.t.fichasPorEquipo("Random"), -1)
        self.assertEqual(self.t.fichasPorEquipo(3), -1)

    def testRangoMovFichasIniciales(self):
        for e in self.t.fichasDelEquipo:
            for x, y in self.t.fichasDelEquipo[e]:
                rangoFicha = self.t.rangoFichaEnTablero(x, y)
                self.assertGreater(len(rangoFicha), 0)
                self.assertLessEqual(len(rangoFicha), 2)



if __name__ == "__main__":
    unittest.main()
