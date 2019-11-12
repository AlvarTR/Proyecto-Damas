import unittest
from ReglasJuego import ReglasJuego
from Fichas import *

class Tablero(ReglasJuego):
    #----------INIT----------
    def __init__(self, longTablero=8):
        super().__init__(longTablero)

        self.equipos = ("Blanco", "Negro")
        self.filaObjetivoPorEquipo = {self.equipos[0]:0, self.equipos[1]:self.LONG_TABLERO-1}
        self.turnoActual = 0
        self.fichasPorEquipo = {}
        self.fichasComidasPorEquipo = {}

        def ponerPiezas():
            self.fichasPorEquipo = {self.equipos[0]:set([]), self.equipos[1]:set([])}
            self.fichasComidasPorEquipo = {self.equipos[0]:[], self.equipos[1]:[]}
            primeraFila = 0
            ultimaFila = self.LONG_TABLERO - 1

            for x in range(self.LONG_TABLERO):
                for e in self.filaObjetivoPorEquipo:
                    inicial = primeraFila
                    final = ultimaFila
                    if self.filaObjetivoPorEquipo[e] == primeraFila:
                        inicial = self.LONG_TABLERO - self.FILAS_PEONES
                    elif self.filaObjetivoPorEquipo[e] == ultimaFila:
                        final = primeraFila + self.FILAS_PEONES-1 #-1 para hacer 0 -> self.FILAS_PEONES-1 (2) en el bucle

                    for y in range(inicial, final+1): #+1 porque "final" es el ultimo valor que queremos rellenar
                        if self.enPosicion(x, y):
                            nuevaFicha = Peon(x, y, e,
                                self.filaObjetivoPorEquipo[e], self.LONG_TABLERO)
                            self.fichasPorEquipo[e].add(nuevaFicha)

        ponerPiezas()

    #----------CHECKS----------
    def fichaEstaEnTablero(self, *fichas):
        EH = False
        for ficha in fichas:
            if not isinstance(ficha, Ficha):
                return EH
            if ficha.equipo not in self.equipos:
                return EH
            if ficha not in self.fichasPorEquipo[ficha.equipo]:
                return EH

        return True

    def fichaEnCoordenadas(self, x, y):
        EH = None
        if not self.enPosicion(x, y):
            return EH

        for e in self.fichasPorEquipo:
            for ficha in self.fichasPorEquipo[e]:
                if ficha.x == x and ficha.y == y:
                    return ficha
        return EH

    def puedeComer(self, fichaCome, fichaAComer):
        EH = False
        if not self.fichaEstaEnTablero(fichaCome, fichaAComer):
            return EH
        if fichaCome.equipo is fichaAComer.equipo:
            return EH
        if (fichaAComer.x, fichaAComer.y) not in fichaCome.movimientosPosibles():
            return EH

        return True

    #----------CAMBIAR FICHAS EN TABLERO----------
    def colocaFicha(self, ficha):
        EH = False
        if not isinstance(ficha, Ficha):
            return EH
        if not self.enPosicion(ficha.x, ficha.y):
            return EH
        if self.fichaEnCoordenadas(ficha.x, ficha.y):
            return EH
        if ficha.equipo not in self.equipos:
            return EH

        self.fichasPorEquipo[ficha.equipo].add(ficha)
        return True


    def colocaFichaEnCoordenadas(self, tipo, x, y, equipo, movimientos=0, fichasComidas=[]):
        EH = False
        if not self.enPosicion(x, y):
            return EH
        if not issubclass(tipo, Ficha):
            return EH
        if not equipo in self.equipos:
            return EH

        ficha = tipo(x, y, equipo, self.filaObjetivoPorEquipo[equipo],
            self.LONG_TABLERO, movimientos, fichasComidas)

        return self.colocaFicha(ficha)

    def quitaFicha(self, ficha):
        EH = False
        if not self.fichaEstaEnTablero(ficha):
            return EH

        self.fichasPorEquipo[ficha.equipo].remove(ficha)
        return True


    def retiraFichaComida(self, fichaCome, fichaComida):
        EH = False
        if not self.puedeComer(fichaCome, fichaComida):
            return EH

        self.fichasComidasPorEquipo[fichaCome.equipo].append(fichaComida)
        quitaFicha(fichaComida)
        fichaCome.comeA(fichaComida, self.turnoActual)
        return True

    #----------MOVIMIENTO----------
    def movPosiblesFicha(self, ficha):
        EH = set([])
        if not isinstance(ficha, Ficha):
            return EH
        if not self.fichaEstaEnTablero(ficha):
            return EH

        movimientos = set( ficha.movimientosPosibles() )

        if isinstance(ficha, Dama):
            coordenadasConFicha = set([])
            for x, y in movimientos:
                if self.fichaEnCoordenadas(x, y):
                    coordenadasConFicha.add( (x, y) )

            for x, y in coordenadasConFicha:
                dirX = -1 if x - ficha.x < 0 else 1
                dirY = -1 if y - ficha.y < 0 else 1
                iX = x
                iY = y
                fichaEncontrada = self.fichaEnCoordenadas(x, y)
                if self.posicionAlComer(ficha, fichaEncontrada):
                    iX += dirX
                    iY += dirY
                while self.enPosicion(iX, iY):
                    movimientos.discard( (iX, iY) )
                    iX += dirX
                    iY += dirY

        return movimientos

    def movValidosFicha(self, ficha):
        EH = set([])
        if not self.fichaEstaEnTablero(ficha):
            return EH

        movimientosValidos = set([])
        for xObjetivo, yObjetivo in self.movPosiblesFicha(ficha):
            valido = False
            fichaEncontrada = self.fichaEnCoordenadas(xObjetivo, yObjetivo)
            if fichaEncontrada:
                coordenadasAlComer = self.posicionAlComer(ficha, fichaEncontrada)
                if coordenadasAlComer:
                    for coor in self.movPosiblesAlComer(ficha):
                        movimientosValidos.add( coor )
            else:
                movimientosValidos.add( (xObjetivo, yObjetivo) )

        return movimientosValidos

    def movValidosEquipo(self, equipo):
        EH = {}
        if not equipo in self.equipos:
            return EH

        dictMovimientos = {}
        for f in self.fichasPorEquipo[equipo]:
            posibles = self.movValidosFicha(f)
            if posibles != set([]):
                dictMovimientos[ (f.x, f.y) ] = posibles

        return dictMovimientos

    def mueveFicha(self, ficha, xObjetivo, yObjectivo):
        EH = False
        if not self.fichaEstaEnTablero(ficha):
            return EH
        if (xObjetivo, yObjectivo) not in movPosiblesFicha(ficha):
            return EH

        fichaEnObjetivo = self.fichaEnCoordenadas(xObjetivo, yObjetivo)
        if fichaEnObjetivo:
            pass
        else:
            ficha.moverA(xObjetivo, yObjetivo)

        return True

    #----------COMER----------
    def posicionAlComer(self, fichaCome, fichaAComer):
        EH = ()
        if not self.puedeComer(fichaCome, fichaAComer):
            return EH

        dirX = -1 if fichaAComer.x - fichaCome.x < 0 else 1
        dirY = -1 if fichaAComer.y - fichaCome.y < 0 else 1
        saltoX = fichaCome.x + 2*dirX
        saltoY = fichaCome.y + 2*dirY
        if self.fichaEnCoordenadas(saltoX, saltoY):
            return EH

        return (saltoX, saltoY)

    def movPosiblesAlComer(self, ficha):
        EH = set([])
        if not self.fichaEstaEnTablero(ficha):
            return EH

        movAlComer = set([])
        for x, y in self.movPosiblesFicha(ficha):
            fichaObjetivo = self.fichaEnCoordenadas(x, y)
            if not fichaObjetivo:
                continue

            coordenadasAlComer = self.posicionAlComer(ficha, fichaObjetivo)
            if not coordenadasAlComer:
                continue

            movAlComer.add( coordenadasAlComer )
            if isinstance(ficha, Peon) and x == ficha.filaObjetivo:
                return movAlComer

            copiaFicha = ficha.__copy__()
            copiaFicha.x = coordenadasAlComer[0]
            copiaFicha.y = coordenadasAlComer[1]
            colocada = self.colocaFicha( copiaFicha )
            for coordenadas in self.movPosiblesAlComer(copiaFicha):
                movAlComer.add(coordenadas)
            self.quitaFicha(copiaFicha)

        return movAlComer


    def comeFicha(self, fichaCome, fichaAComer):
        pass

    def __str__(self):
        tablero = []
        for fila in range(self.LONG_TABLERO):
            tablero.append([])
            for casilla in range(self.LONG_TABLERO):
                tablero[-1].append(None)

        for e in self.fichasPorEquipo:
            for f in self.fichasPorEquipo[e]:
                tablero[f.x][f.y] = f

        TODO_TABLERO = 2*self.LONG_TABLERO
        string = ""

        for i in range(TODO_TABLERO +1):
            string += "_"
        string += "\n"

        for y in range(self.LONG_TABLERO):
            fila = ""
            for x in range(self.LONG_TABLERO):
                if x != 0:
                    fila += '|'
                ficha = tablero[x][y]
                if ficha is None:
                    fila += "_"
                else:
                    fila += ficha.__repr__()

            string += "|" + fila + "| \n"

        return string

#---------------PRUEBAS---------------
class PruebasInsertarEnTablero(unittest.TestCase):
    def setUp(self):
        self.t = Tablero()
        self.e = self.t.equipos

    def testIniciaTableroCorrectamente(self):
        self.assertEqual(len(self.t.fichasPorEquipo), 2)
        for e in self.t.fichasPorEquipo:
            self.assertEqual(len(self.t.fichasPorEquipo[e]), 3*4)

    def testColocaPeon(self):
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 3, 3, self.e[0]))
        self.assertEqual(len(self.t.fichasPorEquipo[self.e[0]]), 3*4+1)

    def testNoPuedeColocarFicha(self):
        self.assertFalse(self.t.colocaFichaEnCoordenadas(Peon, 8, 0, self.e[0]))
        self.assertFalse(self.t.colocaFichaEnCoordenadas(Peon, 0, 8, self.e[0]))
        self.assertFalse(self.t.colocaFichaEnCoordenadas(Peon, 7, 7, self.e[0]))
        self.assertFalse(self.t.colocaFichaEnCoordenadas(Tablero, 3, 3, self.e[0]))
        self.assertFalse(self.t.colocaFichaEnCoordenadas(Peon, 3, 3, "Rosa"))
        self.assertEqual(len(self.t.fichasPorEquipo[self.e[0]]), 3*4)

    def testQuitaPeon(self):
        self.assertTrue(self.t.quitaFicha(self.t.fichaEnCoordenadas(7,7)))
        self.assertEqual(len(self.t.fichasPorEquipo[self.e[0]]), 3*4-1)

    def testColocaDamaQuitaDama(self):
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Dama, 3, 3, self.e[0]))
        self.assertEqual(len(self.t.fichasPorEquipo[self.e[0]]), 3*4+1)
        self.assertTrue(self.t.quitaFicha(self.t.fichaEnCoordenadas(3, 3)))
        self.assertEqual(len(self.t.fichasPorEquipo[self.e[0]]), 3*4)

    def testNoPuedeQuitarFicha(self):
        self.assertFalse(self.t.quitaFicha(self.t.fichaEnCoordenadas(3, 3)))


class PruebasMoverseEnTablero(unittest.TestCase):
    def setUp(self):
        self.t = Tablero()
        self.e = self.t.equipos

    def testMovPeonBloqueado(self):
        movPeon = set(self.t.movValidosFicha(self.t.fichaEnCoordenadas(0, 0)))
        self.assertEqual(len(movPeon), 0)

    def testMovPeonSolo(self):
        for e in self.t.fichasPorEquipo:
            self.t.fichasPorEquipo[e] = set([])
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 2, 2, self.e[0]))
        movPeon = set(self.t.movPosiblesFicha(self.t.fichaEnCoordenadas(2, 2)))
        self.assertEqual(len(movPeon), 2)

    def testMovDamaBloqueada(self):
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Dama, 3, 3, self.e[0]))
        movDama = set(self.t.movPosiblesFicha(self.t.fichaEnCoordenadas(3, 3)))
        self.assertEqual(len(movDama), 2)

    def testMovDamaSola(self):
        for e in self.t.fichasPorEquipo:
            self.t.fichasPorEquipo[e] = set([])
        self.t.colocaFichaEnCoordenadas(Dama, 3, 3, self.e[0])
        movDama = set(self.t.movPosiblesFicha(self.t.fichaEnCoordenadas(3, 3)))
        self.assertEqual(len(movDama), 3+3+3+4)


class PruebasComerEnTablero(unittest.TestCase):
    def setUp(self):
        self.t = Tablero()
        for e in self.t.fichasPorEquipo:
            self.t.fichasPorEquipo[e] = set([])
        self.e = self.t.equipos

    def testCome1Pieza(self):
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 1, 1, self.e[1]))

        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 2, 2, self.e[0]))
        movAlComer = self.t.movValidosFicha(self.t.fichaEnCoordenadas(1, 1))
        self.assertEqual(len(movAlComer), 1+1)

    def testNoPuedeComer1Pieza(self):
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 1, 1, self.e[1]))

        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 2, 2, self.e[0]))
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 3, 3, self.e[0]))
        movAlComer = self.t.movValidosFicha(self.t.fichaEnCoordenadas(1, 1))
        self.assertEqual(len(movAlComer), 1)

    def testComeSecuenciaPiezasZigZag(self):
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 1, 1, self.e[1]))

        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 2, 2, self.e[0]))
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 2, 4, self.e[0]))
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 2, 6, self.e[0]))
        movAlComer = self.t.movValidosFicha(self.t.fichaEnCoordenadas(1, 1))
        self.assertEqual(len(movAlComer), 1+3)

    def testComeSecuenciaPiezasZigZagPeroBloqueado(self):
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 1, 1, self.e[1]))

        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 2, 2, self.e[0]))
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 2, 4, self.e[0]))
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 1, 5, self.e[0]))
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 2, 6, self.e[0]))
        movAlComer = self.t.movValidosFicha(self.t.fichaEnCoordenadas(1, 1))
        self.assertEqual(len(movAlComer), 1+1)

    def testComeSecuenciaPiezasLinea(self):
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 1, 1, self.e[1]))

        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 2, 2, self.e[0]))
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 4, 4, self.e[0]))
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 6, 6, self.e[0]))
        movAlComer = self.t.movValidosFicha(self.t.fichaEnCoordenadas(1, 1))
        self.assertEqual(len(movAlComer), 1+3)

    def testComePiezasConCaminosConver(self):
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 3, 1, self.e[1]))

        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 2, 2, self.e[0]))
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 2, 4, self.e[0]))
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 4, 2, self.e[0]))
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 4, 4, self.e[0]))
        movAlComer = self.t.movValidosFicha(self.t.fichaEnCoordenadas(3, 1))
        self.assertEqual(len(movAlComer), 3)

    def testComePiezasHastaObjetivo(self):
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 1, 1, self.e[1]))

        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 2, 2, self.e[0]))
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 2, 4, self.e[0]))
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 2, 6, self.e[0]))
        self.assertTrue(self.t.colocaFichaEnCoordenadas(Peon, 5, 5, self.e[0]))
        movAlComer = self.t.movValidosFicha(self.t.fichaEnCoordenadas(1, 1))
        self.assertEqual(len(movAlComer), 1+3)


if __name__ == "__main__":
    unittest.main()
