import ValoresPorDefecto as vpd
from Fichas import *
import unittest

class Tablero():
    def __init__(self, longTablero=vpd.LONG_TABLERO, equipos=vpd.EQUIPOS):
        self.LONG_TABLERO = 8
        self.EQUIPOS = equipos

        self.PEON = nuevoPeon()
        self.DAMA = nuevaDama(self.LONG_TABLERO)

        self.filaObjetivoDelEquipo = {self.EQUIPOS[0]:0, self.EQUIPOS[1]:self.LONG_TABLERO - 1}
        self.fichasDelEquipo = {e:{} for e in self.EQUIPOS}

    def colocaFichasIniciales(self, relacionCasillasFichas=0.4):
        filasPeones = int(self.LONG_TABLERO*relacionCasillasFichas)

        primeraFila = 0
        ultimaFila = self.LONG_TABLERO - 1

        for e in self.fichasDelEquipo:
            self.fichasDelEquipo[e].clear()

        for e in self.filaObjetivoDelEquipo:
            inicio = primeraFila
            fin = ultimaFila
            if self.filaObjetivoDelEquipo[e] == primeraFila:
                inicio = self.LONG_TABLERO - filasPeones
            elif self.filaObjetivoDelEquipo[e] == ultimaFila:
                fin = filasPeones-1 #-1 para hacer 0 -> self.FILAS_PEONES-1 (2) en el bucle

            for y in range(inicio, fin+1): #+1 porque "final" es el ultimo valor que queremos rellenar
                for x in iter(x for x in range(self.LONG_TABLERO) if self.posicionValida(x, y)):
                    self.fichasDelEquipo[e][(x, y)] = self.PEON

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
        for x, y in self.fichasDelEquipo[equipo]:
            if not self.posicionValida(x, y):
                continue
            coordenadasValidas += 1

        return coordenadasValidas


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
            yield ( (xObjetivo, yObjetivo), )

    def opcionesComerFicha(self, x, y):
        EH = {}
        equipo = self.equipoEnCoordenadas(x, y)
        if not equipo:
            return EH

        fichasQuePuedeComerYMovResultante = {}
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

            fichasQuePuedeComerYMovResultante[ (xObjetivo, yObjetivo) ] = (xSiguiente, ySiguiente)

        return fichasQuePuedeComerYMovResultante

    def tableroEnElQueFichaComeAFicha(self, xFicha, yFicha, xObjetivo, yObjetivo):
        EH = None
        equipo = self.equipoEnCoordenadas(xFicha, yFicha)
        if not equipo:
            return EH

        equipoObjetivo = self.equipoEnCoordenadas(xObjetivo, yObjetivo)
        if not equipoObjetivo:
            return EH

        fichasComibles = self.opcionesComerFicha(xFicha, yFicha)
        if not fichasComibles:
            return EH
        if not (xObjetivo, yObjetivo) in fichasComibles:
            return EH

        simulacion = self.copia()

        ficha = simulacion.fichasDelEquipo[equipo].pop( (xFicha, yFicha) )

        xFichaComiendo, yFichaComiendo = fichasComibles[ (xObjetivo, yObjetivo) ]
        simulacion.fichasDelEquipo[equipo][ (xFichaComiendo, yFichaComiendo) ] = ficha

        simulacion.fichasDelEquipo[equipoObjetivo].pop( (xObjetivo, yObjetivo) )

        return simulacion

    def movimientosComerFicha(self, x, y):
        for (xObjetivo, yObjetivo), (xTrasComer, yTrasComer) in self.opcionesComerFicha(x, y).items():
            t = self.tableroEnElQueFichaComeAFicha(x, y, xObjetivo, yObjetivo)
            if not t:
                continue

            contadorSecuencias = 0
            for secuencia in t.movimientosComerFicha( xTrasComer, yTrasComer ):
                listaEditada = ( (xTrasComer, yTrasComer), )
                for salto in secuencia:
                    listaEditada += (salto, )
                yield listaEditada
                contadorSecuencias += 1

            if contadorSecuencias == 0:
                yield ( (xTrasComer, yTrasComer), )

    def movimientosFicha(self, x, y):
        yield from self.movimientosComerFicha(x, y)
        yield from self.desplazamientoFicha(x, y)

    def movimientosPorEquipo(self, equipo):
        EH = iter(())
        if not equipo in self.EQUIPOS:
            return EH

        for (x, y) in self.fichasPorEquipo[equipo]:
            for movimiento in self.movimientosFicha(x, y):
                yield ((x, y), movimiento)


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
        for x, y in coordenadasConRespuestas:
            self.t.fichasDelEquipo[self.blanco][(x, y)] = self.t.DAMA
            rangoDama = tuple(self.t.rangoFicha(x, y))
            self.assertEqual(len( rangoDama ), coordenadasConRespuestas[ (x, y) ], "Fallo en coordenadas " + str(x) + ", " + str(y))

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

        simulacion = self.t.tableroEnElQueFichaComeAFicha( coorN[0], coorN[1], coorB[0], coorB[1] )
        self.assertIsNone(simulacion)

    def testPeonComePeon(self):
        coorN = (3, 3)
        self.t.fichasDelEquipo[self.negro][ coorN ] = self.t.PEON
        coorB = (4, 4)
        self.t.fichasDelEquipo[self.blanco][ coorB ] = self.t.PEON

        self.assertEqual(len(self.t.fichasDelEquipo[self.negro]), 1)
        self.assertEqual(len(self.t.fichasDelEquipo[self.blanco]), 1)

        simulacion = self.t.tableroEnElQueFichaComeAFicha( coorN[0], coorN[1], coorB[0], coorB[1] )
        self.assertEqual(len(self.t.fichasDelEquipo[self.negro]), 1)
        self.assertEqual(len(self.t.fichasDelEquipo[self.blanco]), 1)

        print(self.t)
        print(tuple(self.t.movimientosFicha(3, 3)))

        self.assertEqual(len(simulacion.fichasDelEquipo[self.negro]), 1)
        self.assertEqual(len(simulacion.fichasDelEquipo[self.blanco]), 0)

    def testComerEnDiagonal(self):
        self.t.fichasDelEquipo[self.negro][ (0, 0) ] = self.t.PEON
        for i in range(1, self.t.LONG_TABLERO, 2):
            self.t.fichasDelEquipo[self.blanco][ (i, i) ] = self.t.PEON

        comerEnCadena = tuple(self.t.movimientosComerFicha(0, 0))
        self.assertEqual(len( comerEnCadena ), 1)

    def testComerConBifurcacion(self):
        self.t.fichasDelEquipo[self.negro][ (0, 0) ] = self.t.PEON
        for i in range(1, self.t.LONG_TABLERO, 2):
            self.t.fichasDelEquipo[self.blanco][ (i, i) ] = self.t.PEON
        self.t.fichasDelEquipo[self.blanco][ (1, 3) ] = self.t.PEON

        comerEnCadena = tuple(self.t.movimientosComerFicha(0, 0))
        self.assertEqual(len( comerEnCadena ), 2)

    def testComerConBifurcacionesConvergentes(self):
        x, y = (2, 0)
        self.t.fichasDelEquipo[self.negro][ (x, y) ] = self.t.PEON
        for i in range(1, self.t.LONG_TABLERO, 2):
            for j in range(1, self.t.LONG_TABLERO, 2):
                self.t.fichasDelEquipo[self.blanco][ (i, j) ] = self.t.PEON

        comerEnCadena = tuple(self.t.movimientosComerFicha(x, y))
        #print(comerEnCadena)
        self.assertEqual(len( comerEnCadena ), 5)
        for salto in comerEnCadena:
            self.assertEqual(len(salto), 3)


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




if __name__ == "__main__":
    unittest.main()
