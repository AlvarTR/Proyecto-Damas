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
            for x in iter(x for x in range(t.LONG_TABLERO) if posicionValida(x, y, t.LONG_TABLERO)):
                t.fichasDelEquipo[e][(x, y)] = t.PEON
    return t

def movimientosPosiblesFichaEnTablero(x, y, tablero):
    EH = []
    if not posicionValida(x, y, tablero.LONG_TABLERO):
        return EH

    equipo = tablero.equipoEnCoordenadas(x, y)
    if not equipo:
        return EH

    ficha = tablero.fichasDelEquipo[equipo][ (x, y) ]

    dirFicha = -1 if tablero.filaObjetivoDelEquipo[equipo] - y < 0 else 1

    movPosibles = []
    for i in range(-ficha.movMax, ficha.movMax + 1): #+1 para abarcar movMax
        if i == 0:
            continue

        if not ficha.puedeIrAtras:
            dirMovY = -1 if i < 0 else 1
            if dirFicha != dirMovY:
                continue

        posibleY = y + i
        for posibleX in (x - i, x + i):
            if posicionValida(posibleX, posibleY, tablero.LONG_TABLERO):
                movPosibles.append( (posibleX, posibleY) )


    return movPosibles

def movimientosLegalesFichaEnTablero(x, y, tablero):
    ## TODO:
    pass
    
class PruebasReglas(unittest.TestCase):
    def setUp(self):
        self.t = tableroConFichasIniciales()

    def testFichasInicialesBienPuestas(self):
        for e in self.t.fichasDelEquipo:
            self.assertEqual(len(self.t.fichasDelEquipo[e]), 12)

    def testFichasPorEquipo(self):
        for e in self.t.EQUIPOS:
            self.assertEqual(self.t.fichasPorEquipo(e), 12)
        self.assertEqual(self.t.fichasPorEquipo("Random"), -1)
        self.assertEqual(self.t.fichasPorEquipo(3), -1)

    def testMovPosibles(self):
        print(self.t)
        for e in self.t.fichasDelEquipo:
            for x, y in self.t.fichasDelEquipo[e]:
                print(e, (x, y), movimientosFichaEnTablero(x, y, self.t))


if __name__ == "__main__":
    unittest.main()
