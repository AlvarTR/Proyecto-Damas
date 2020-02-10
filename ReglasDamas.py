from Tablero import *
from Fichas import *
import unittest

def posicionValida(x, y, longTablero):
    EH = False
    if x < 0 or x >= longTablero:
        return EH
    if y < 0 or y >= longTablero:
        return EH
    if (x + y) % 2 != 0:
        return EH

    return True

def ponFichasIniciales(longTablero=8, relacionCasillasFichas=0.4, equipos=("Blanco", "Negro")):
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
            for x in iter(x for x in range(t.LONG_TABLERO) if posicionValida(x, y, t.LONG_TABLERO)):
                t.fichasDelEquipo[e][(x, y)] = t.PEON
                print("Ficha puesta")
    return t

def movimientosFichaEnTablero(x, y, tablero):
    pass

class PruebasReglas(unittest.TestCase):
    def setUp(self):
        self.t = ponFichasIniciales()

    def testFichasInicialesBienPuestas(self):
        print(self.t)

if __name__ == "__main__":
    unittest.main()
