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

def rangoFichaEnTablero(x, y, tablero):
    EH = {}
    if not posicionValida(x, y, tablero.LONG_TABLERO):
        return EH

    equipo = tablero.equipoEnCoordenadas(x, y)
    if not equipo:
        return EH

    ficha = tablero.fichasDelEquipo[equipo][ (x, y) ]

    dirFicha = -1 if tablero.filaObjetivoDelEquipo[equipo] - y < 0 else 1

    movPosibles = set()
    fichasEncontradas = set()
    for i in range(-ficha.movMax, ficha.movMax + 1): #+1 para abarcar movMax
        if i == 0:
            continue

        if not ficha.puedeIrAtras:
            dirMovY = -1 if i < 0 else 1
            if dirFicha != dirMovY:
                continue

        posibleY = y + i
        for posibleX in (x - i, x + i):
            if not posicionValida(posibleX, posibleY, tablero.LONG_TABLERO):
                continue
            if tablero.equipoEnCoordenadas( posibleX, posibleY ):
                fichasEncontradas.add( (posibleX, posibleY) )

            movPosibles.add( (posibleX, posibleY) )


    for xEncontrada, yEncontrada in fichasEncontradas:
        distX = xEncontrada - x
        distY = yEncontrada - y

        dirX = -1 if distX < 0 else 1
        dirY = -1 if distY < 0 else 1

        distX = dirX * distX
        distY = dirY * distY

        for posibleX, posibleY in movPosibles.copy():
            distPosibleX = posibleX - x
            distPosibleY = posibleY - y

            dirPosibleX = -1 if distPosibleX < 0 else 1
            dirPosibleY = -1 if distPosibleY < 0 else 1

            if dirPosibleX != dirX:
                continue
            if dirPosibleY != dirY:
                continue

            distPosibleX = dirPosibleX * distPosibleX
            distPosibleY = dirPosibleY * distPosibleY

            if distPosibleX <= distX:
                continue
            if distPosibleY <= distY:
                continue

            movPosibles.remove( (posibleX, posibleY) )

    return list(movPosibles)


def desplazamientoFichaEnTablero(x, y, tablero):
    EH = []
    rangoMov = rangoFichaEnTablero(x, y, tablero)
    if not rangoMov:
        return EH

    fichasEncontradas = set([])

    desplazamiento = []
    for xObjetivo, yObjetivo in rangoMov:
        if tablero.equipoEnCoordenadas(xObjetivo, yObjetivo):
            continue
        desplazamiento.append( (xObjetivo, yObjetivo) )

    return desplazamiento

def fichasEnemigasAccesiblesPorFichaEnTablero(x, y, tablero):
    EH = []
    rangoMov = desplazamientoFichaEnTablero(x, y, tablero)
    if not rangoMov:
        return EH

    equipo = tablero.equipoEnCoordenadas(x, y)
    coordenadasEnemigas = []
    for xObjetivo, yObjetivo in rangoMov:
        equipoObjetivo = tablero.equipoEnCoordenadas(xObjetivo, yObjetivo)
        if equipo != equipoObjetivo:
            coordenadasEnemigas.append( (xObjetivo, yObjetivo) )

    return coordenadasEnemigas

class PruebasFichasIniciales(unittest.TestCase):
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

    def testRangoMovFichasIniciales(self):
        for e in self.t.fichasDelEquipo:
            for x, y in self.t.fichasDelEquipo[e]:
                rangoFicha = rangoFichaEnTablero(x, y, self.t)
                self.assertGreater(len(rangoFicha), 0)
                self.assertLessEqual(len(rangoFicha), 2)

class PruebasMovimiento(unittest.TestCase):
    def setUp(self):
        self.t = Tablero()

    def testRangoMovDamaSola(self):
        self.t.fichasDelEquipo["Blanco"][(3, 3)] = self.t.DAMA
        rangoDama = rangoFichaEnTablero(3, 3, self.t)
        self.assertEqual(len(rangoDama), 7+6)

    def testRangoMovDama(self):
        e1 = self.t.EQUIPOS[0]
        e2 = self.t.EQUIPOS[1]
        self.t.fichasDelEquipo[e1][(3, 3)] = self.t.DAMA
        self.t.fichasDelEquipo[e1][(1, 1)] = self.t.PEON

        self.t.fichasDelEquipo[e2][(6, 6)] = self.t.PEON
        self.t.fichasDelEquipo[e2][(5, 1)] = self.t.PEON
        self.t.fichasDelEquipo[e2][(1, 5)] = self.t.PEON

        print(self.t)
        rangoDama = rangoFichaEnTablero(3, 3, self.t)
        self.assertEqual(len(rangoDama), 2+2+2+3)




if __name__ == "__main__":
    unittest.main()
