import ValoresPorDefecto as vpd
from Fichas import *
import unittest

class Tablero():
    def __init__(self, longTablero=vpd.LONG_TABLERO, equipos=vpd.EQUIPOS):
        self.LONG_TABLERO = longTablero
        self.EQUIPOS = equipos

        self.PEON = nuevoPeon()
        self.DAMA = nuevaDama(self.LONG_TABLERO)

        self.filaObjetivoDelEquipo = {self.EQUIPOS[0]:0, self.EQUIPOS[1]:self.LONG_TABLERO - 1}
        self.fichasDelEquipo = {e:{} for e in self.EQUIPOS}


    def colocaFichasIniciales(self, relacionCasillasFichas=0.4):
        filasPeones = int(self.LONG_TABLERO*relacionCasillasFichas)

        primeraFila = 0
        ultimaFila = self.LONG_TABLERO - 1

        for e in self.EQUIPOS:
            self.fichasDelEquipo[e].clear()

            inicio = primeraFila
            fin = ultimaFila
            if self.filaObjetivoDelEquipo[e] == primeraFila:
                inicio = self.LONG_TABLERO - filasPeones
            elif self.filaObjetivoDelEquipo[e] == ultimaFila:
                fin = filasPeones-1 #-1 para hacer 0 -> self.FILAS_PEONES-1 (2) en el bucle

            for y in range(inicio, fin+1): #+1 porque "final" es el ultimo valor que queremos rellenar
                for x in (x for x in range(self.LONG_TABLERO) if self.posicionValida(x, y)):
                    self.fichasDelEquipo[e][ (x, y) ] = self.PEON


    def posicionValida(self, x, y):
        EH = False
        if x < 0 or x >= self.LONG_TABLERO:
            return EH
        if y < 0 or y >= self.LONG_TABLERO:
            return EH
        if (x + y) % 2 != 0:
            return EH

        return True

    def equipoEnCoordenadas(self, x, y):
        EH = None

        if not self.posicionValida(x, y):
            return EH

        equipoEncontrado = None
        for e, fichasEquipo in self.fichasDelEquipo.items():
            if (x, y) in fichasEquipo:
                if equipoEncontrado is not None:
                    return EH
                equipoEncontrado = e


        return equipoEncontrado

    def fichasPorEquipo(self, equipo):
        EH = -1
        if equipo not in self.EQUIPOS:
            return EH

        coordenadasValidas = 0
        for (x, y) in self.fichasDelEquipo[equipo] :
            if not self.posicionValida(x, y):
                continue
            coordenadasValidas += 1

        return coordenadasValidas

    def peonesPorDamas(self):
        EH = None

        def peonesEnPosDama(self):
            tableroCambiado = False
            for e in self.EQUIPOS:
                filaDama = self.filaObjetivoDelEquipo[e]
                if any(x for x in range(self.LONG_TABLERO) if ((x, filaDama), self.PEON) in self.fichasDelEquipo[e].items()):
                    tableroCambiado = True
                    break
            return tableroCambiado

        tableroCambiado = self.peonesEnPosDama()

        if not tableroCambiado:
            return EH

        tableroNuevasDamas = self.copia()
        for e in self.EQUIPOS:
            filaDama = self.filaObjetivoDelEquipo[e]
            for x in (x for x in range(self.LONG_TABLERO) if ((x, filaDama), self.PEON) in self.fichasDelEquipo[e].items()):
                tableroNuevasDamas.fichasDelEquipo[e][ (x, filaDama) ] = tableroNuevasDamas.DAMA

        return tableroNuevasDamas

    def rangoFicha(self, x, y):
        EH = iter(())

        equipo = self.equipoEnCoordenadas(x, y)
        if not equipo:
            return EH

        ficha = self.fichasDelEquipo[equipo][ (x, y) ]
        dirFicha = -1 if self.filaObjetivoDelEquipo[equipo] - y < 0 else 1

        direccionesConFichaBloqueando = set()
        i = 0
        while i < ficha.movMax:
            i += 1

            opcionesY = (y + dirFicha*i, )
            if ficha.puedeIrAtras:
                opcionesY = (y - i, y + i)

            for posibleY in opcionesY:
                if not self.posicionValida(posibleY%2, posibleY):
                    continue

                dirPosibleY = -1 if posibleY - y < 0 else 1
                for posibleX in (x - i, x + i):
                    if not self.posicionValida(posibleX, posibleY):
                        continue

                    dirPosibleX = -1 if posibleX - x < 0 else 1
                    if (dirPosibleX, dirPosibleY) in direccionesConFichaBloqueando:
                        continue

                    if self.equipoEnCoordenadas(posibleX, posibleY):
                        direccionesConFichaBloqueando.add( (dirPosibleX, dirPosibleY) )

                    yield (posibleX, posibleY)

    def desplazamientoFicha(self, x, y):
        for xObjetivo, yObjetivo in self.rangoFicha(x, y):
            if self.equipoEnCoordenadas(xObjetivo, yObjetivo):
                continue
            yield (xObjetivo, yObjetivo)

    def movimientosTrasComerFicha(self, x, y):
        EH = iter(())
        equipo = self.equipoEnCoordenadas(x, y)
        if not equipo:
            return EH

        for xObjetivo, yObjetivo in self.rangoFicha(x, y):
            equipoObjetivo = self.equipoEnCoordenadas(xObjetivo, yObjetivo)
            if not equipoObjetivo:
                continue
            if equipo == equipoObjetivo:
                continue

            dirX = -1 if xObjetivo - x < 0 else 1
            dirY = -1 if yObjetivo - y < 0 else 1
            xSiguiente = xObjetivo + dirX
            ySiguiente = yObjetivo + dirY
            if not self.posicionValida(xSiguiente, ySiguiente):
                continue
            if self.equipoEnCoordenadas(xSiguiente, ySiguiente):
                continue

            yield (xSiguiente, ySiguiente)

    def movimientosFicha(self, x, y):
        yield from self.movimientosTrasComerFicha(x, y)
        yield from self.desplazamientoFicha(x, y)

    def movimientosEquipo(self, equipo):
        EH = iter(())
        if not equipo in self.EQUIPOS:
            return EH

        for (x, y) in self.fichasDelEquipo[equipo]:
            yield from self.movimientosFicha(x, y)


    def tableroTrasMovimientoFicha(self, xFicha, yFicha, xObjetivo, yObjetivo):
        EH = None
        equipo = self.equipoEnCoordenadas(xFicha, yFicha)
        if not equipo:
            return EH

        if not (xObjetivo, yObjetivo) in self.movimientosFicha(xFicha, yFicha):
            return EH

        sim = self.copia()

        ficha = sim.fichasDelEquipo[equipo].pop( (xFicha, yFicha) )
        sim.fichasDelEquipo[equipo][ (xObjetivo, yObjetivo) ] = ficha

        dirX = -1 if xObjetivo - xFicha < 0 else 1
        dirY = -1 if yObjetivo - yFicha < 0 else 1
        xAnterior = xObjetivo - dirX
        yAnterior = yObjetivo - dirY

        if (xAnterior, yAnterior) == (xFicha, yFicha):
            return sim

        equipoObjetivo = self.equipoEnCoordenadas(xAnterior, yAnterior)
        if not equipoObjetivo:
            return sim

        sim.fichasDelEquipo[equipoObjetivo].pop( (xAnterior, yAnterior) )
        return sim


    def tableroConResaltes(self, coordenadasAResaltar=()):
        CARACTER_RESALTE = "■" #chr(9632)

        setCoordenadas = set(coordenadasAResaltar)
        string = ""
        for y in range(self.LONG_TABLERO):
            string += "\n" + str(y)
            for x in range(self.LONG_TABLERO):

                if (x, y) in setCoordenadas:
                    string += CARACTER_RESALTE
                    continue

                e = self.equipoEnCoordenadas(x, y)
                if e:
                    ficha = self.fichasDelEquipo[e][(x, y)]
                    string += ficha.impresion(e[0])
                    continue

                string += "_"

        string += "\n "
        for i in range(self.LONG_TABLERO):
            string += str(i)
        string += "\n"

        string = "|".join(string)
        string = "_" * (2*(self.LONG_TABLERO + 1) + 1) + string

        return string

    def tableroConMovimientosFicha(self, x, y):
        return self.tableroConResaltes(self.movimientosFicha(x, y))

    def tableroConComidaFicha(self, x, y):
        return self.tableroConResaltes(self.movimientosTrasComerFicha(x, y))

    def tableroConMovimientosEquipo(self, equipo):
        return self.tableroConResaltes(self.movimientosEquipo(equipo))

    def __str__(self):
        return self.tableroConResaltes()


    def __eq__(self, other):
        EH = False
        if not instanceof(other, Tablero):
            return EH

        if self.LONG_TABLERO != other.LONG_TABLERO:
            return EH

        if self.EQUIPOS != other.EQUIPOS:
            return EH

        for e in self.EQUIPOS:
            if self.fichasDelEquipo[e] != other.fichasDelEquipo[e]:
                return EH

        return True


    def __copy__(self):
        t = Tablero(self.LONG_TABLERO, self.EQUIPOS)

        for e in self.EQUIPOS:
            for coordenada in self.fichasDelEquipo[e]:
                ficha = self.fichasDelEquipo[e][ coordenada ]
                if ficha.tipoFicha == self.PEON.tipoFicha:
                    t.fichasDelEquipo[e][ coordenada ] = t.PEON
                elif ficha.tipoFicha == self.DAMA.tipoFicha:
                    t.fichasDelEquipo[e][ coordenada ] = t.DAMA
        return t

    def copia(self):
        return self.__copy__()


class PruebasFichasIniciales(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.t = Tablero()

    def setUp(self):
        self.t.colocaFichasIniciales()

    def testFichasInicialesBienPuestas(self):
        #print(self.t)
        for e in self.t.fichasDelEquipo:
            self.assertEqual(self.t.fichasPorEquipo(e), 12)

    def testRangoMovFichasIniciales(self):
        for e in self.t.fichasDelEquipo:
            for x, y in self.t.fichasDelEquipo[e]:
                rangoFicha = tuple(self.t.rangoFicha(x, y))
                self.assertGreater(len(rangoFicha), 0)
                self.assertLessEqual(len(rangoFicha), 2)

    def testTableroBienImpreso(self):
        print(self.t)

    def testTableroResaltandoBlanco(self):
        print(self.t.tableroConMovimientosEquipo("Blanco"))


class PruebasDesplazamiento(unittest.TestCase):
    def setUp(self):
        self.t = Tablero()
        self.blanco = self.t.EQUIPOS[0]
        self.negro = self.t.EQUIPOS[1]

    def testRangoMovDamaSola(self):
        coordenadasConRespuestas = {
        (0, 0): 7,
        (1, 1): 1+1+1+6,
        (2, 2): 2+2+2+5,
        (3, 3): 3+3+3+4,
        (8, 0): 0,
        (0, 8): 0,
        (-1, 0): 0,
        (0, -1): 0,
        (2, 3): 0
        }
        for (x, y) in coordenadasConRespuestas:
            self.t.fichasDelEquipo[self.blanco][(x, y)] = self.t.DAMA
            rangoDama = tuple(self.t.rangoFicha(x, y))
            self.assertEqual(len( rangoDama ), coordenadasConRespuestas[ (x, y) ], "Fallo en coordenadas " + str(x) + ", " + str(y))

            #print(self.t)

            self.t.fichasDelEquipo[self.blanco].pop( (x, y) )

    def testRangoMovDamaConFichas(self):
        self.t.fichasDelEquipo[self.blanco][(3, 3)] = self.t.DAMA
        self.t.fichasDelEquipo[self.blanco][(1, 1)] = self.t.PEON

        self.t.fichasDelEquipo[self.negro][(6, 6)] = self.t.PEON
        self.t.fichasDelEquipo[self.negro][(5, 1)] = self.t.DAMA
        self.t.fichasDelEquipo[self.negro][(1, 5)] = self.t.PEON

        rangoDama = tuple(self.t.rangoFicha(3, 3))
        self.assertEqual(len( rangoDama ), 2+2+2+3)


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

    def testEHFichasPorEquipo(self):
        self.assertEqual(self.t.fichasPorEquipo("Random"), -1)
        self.assertEqual(self.t.fichasPorEquipo(3), -1)


class PruebasComer(unittest.TestCase):
    def setUp(self):
        self.t = Tablero()
        self.blanco = self.t.EQUIPOS[0]
        self.negro = self.t.EQUIPOS[1]

    def testPeonNoPuedeComerPeon(self):
        coorN = (3, 3)
        self.t.fichasDelEquipo[self.negro][ coorN ] = self.t.PEON
        coorB = (4, 4)
        self.t.fichasDelEquipo[self.blanco][ coorB ] = self.t.PEON
        self.t.fichasDelEquipo[self.blanco][ (5, 5) ] = self.t.PEON

        self.assertEqual(len(self.t.fichasDelEquipo[self.negro]), 1)
        self.assertEqual(len(self.t.fichasDelEquipo[self.blanco]), 2)

        simulacion = self.t.tableroTrasMovimientoFicha( coorN[0], coorN[1], coorB[0], coorB[1] )
        self.assertIsNone(simulacion)

    def testPeonComePeon(self):
        coorN = (3, 3)
        self.t.fichasDelEquipo[self.negro][ coorN ] = self.t.PEON
        coorB = (4, 4)
        self.t.fichasDelEquipo[self.blanco][ coorB ] = self.t.PEON

        self.assertEqual(len(self.t.fichasDelEquipo[self.negro]), 1)
        self.assertEqual(len(self.t.fichasDelEquipo[self.blanco]), 1)

        simulacion = self.t.tableroTrasMovimientoFicha( coorN[0], coorN[1], coorB[0]+1, coorB[1]+1 )
        self.assertEqual(len(self.t.fichasDelEquipo[self.negro]), 1)
        self.assertEqual(len(self.t.fichasDelEquipo[self.blanco]), 1)

        self.assertEqual(len(simulacion.fichasDelEquipo[self.negro]), 1)
        self.assertEqual(len(simulacion.fichasDelEquipo[self.blanco]), 0)

    def testComerEnDiagonal(self):
        self.t.fichasDelEquipo[self.negro][ (0, 0) ] = self.t.PEON
        for i in range(1, self.t.LONG_TABLERO, 2):
            self.t.fichasDelEquipo[self.blanco][ (i, i) ] = self.t.PEON

        comerEnCadena = tuple(self.t.movimientosTrasComerFicha(0, 0))
        self.assertEqual(len( comerEnCadena ), 1)

    def testComerConBifurcacion(self):
        self.t.fichasDelEquipo[self.negro][ (0, 0) ] = self.t.PEON
        for i in range(1, self.t.LONG_TABLERO, 2):
            self.t.fichasDelEquipo[self.blanco][ (i, i) ] = self.t.PEON
        self.t.fichasDelEquipo[self.blanco][ (1, 3) ] = self.t.PEON

        #print(self.t.tableroConMovimientosFicha(0, 0))
        comerEnCadena = tuple(self.t.movimientosTrasComerFicha(0, 0))
        self.assertEqual(len( comerEnCadena ), 1)

    def testComerConBifurcacionesConvergentes(self):
        x, y = (2, 0)
        self.t.fichasDelEquipo[self.negro][ (x, y) ] = self.t.PEON
        for i in range(1, self.t.LONG_TABLERO, 2):
            for j in range(1, self.t.LONG_TABLERO, 2):
                self.t.fichasDelEquipo[self.blanco][ (i, j) ] = self.t.PEON

        #print(self.t.tableroConMovimientosFicha(x, y))
        comerEnCadena = tuple(self.t.movimientosTrasComerFicha(x, y))
        #print(comerEnCadena)
        self.assertEqual(len( comerEnCadena ), 2)


class PruebasMovimiento(unittest.TestCase):
    def setUp(self):
        self.t = Tablero()
        self.blanco = self.t.EQUIPOS[0]
        self.negro = self.t.EQUIPOS[1]

    def testMovimientosDamaConFichas(self):
        self.t.fichasDelEquipo[self.blanco][(3, 3)] = self.t.DAMA
        self.t.fichasDelEquipo[self.blanco][(1, 1)] = self.t.PEON

        self.t.fichasDelEquipo[self.negro][(6, 6)] = self.t.PEON
        self.t.fichasDelEquipo[self.negro][(5, 1)] = self.t.DAMA
        self.t.fichasDelEquipo[self.negro][(1, 5)] = self.t.PEON

        movDama = tuple(self.t.movimientosFicha(3, 3))
        self.assertEqual(len( movDama ), 8)

    def testMovimientosEquipoVacio(self):
        for equipo in self.t.EQUIPOS:
            self.assertFalse( any(self.t.movimientosEquipo(equipo)) )

    def testMovimientoFichasBloqueadas(self):
        self.t = Tablero(longTablero=2)
        self.t.fichasDelEquipo[self.blanco][(0, 0)] = self.t.PEON
        self.t.fichasDelEquipo[self.negro][(1, 1)] = self.t.PEON
        for equipo in self.t.EQUIPOS:
            self.assertFalse( any(self.t.movimientosEquipo(equipo)) )


if __name__ == "__main__":
    unittest.main()
