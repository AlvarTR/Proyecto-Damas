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
        for e, fichasEquipo in self.fichasDelEquipo.items():
            if (x, y) in fichasEquipo:
                return e
        return EH

    def fichasPorEquipo(self, equipo):
        EH = -1
        if equipo not in self.EQUIPOS:
            return EH
        return len(self.fichasDelEquipo[equipo])


    def rangoFichaEnTablero(self, x, y):
        EH = []
        if not self.posicionValida(x, y):
            return EH

        equipo = self.equipoEnCoordenadas(x, y)
        if not equipo:
            return EH

        ficha = self.fichasDelEquipo[equipo][ (x, y) ]

        dirFicha = -1 if self.filaObjetivoDelEquipo[equipo] - y < 0 else 1

        rangoPosible = []
        direccionesConFichaBloqueando = set()
        i = 1
        while i <= ficha.movMax:
            opcionesY = (y + dirFicha*i, )

            if ficha.puedeIrAtras:
                opcionesY = (y - i, y + i)

            for posibleY in opcionesY:
                dirPosibleY = -1 if posibleY - y < 0 else 1

                for posibleX in (x - i, x + i):
                    if not self.posicionValida(posibleX, posibleY):
                        continue

                    dirPosibleX = -1 if posibleX - x < 0 else 1
                    if (dirPosibleX, dirPosibleY) in direccionesConFichaBloqueando:
                        continue

                    if self.equipoEnCoordenadas(posibleX, posibleY):
                        direccionesConFichaBloqueando.add( (dirPosibleX, dirPosibleY) )

                    rangoPosible.append( (posibleX, posibleY) )
            i += 1

        return rangoPosible

    def desplazamientoFichaEnTablero(self, x, y):
        EH = []
        rangoMov = self.rangoFichaEnTablero(x, y)
        if not rangoMov:
            return EH

        desplazamiento = []
        for xObjetivo, yObjetivo in rangoMov:
            if self.equipoEnCoordenadas(xObjetivo, yObjetivo):
                continue
            desplazamiento.append( (xObjetivo, yObjetivo) )

        return desplazamiento

    def opcionesComerFichaEnTablero(self, x, y):
        EH = {}
        rangoMov = self.rangoFichaEnTablero(x, y)
        if not rangoMov:
            return EH

        equipo = self.equipoEnCoordenadas(x, y)

        fichasQuePuedeComerYMovResultante = {}
        for xObjetivo, yObjetivo in rangoMov:
            equipoObjetivo = self.equipoEnCoordenadas(xObjetivo, yObjetivo)
            if not equipo:
                continue
            if equipo == equipoObjetivo:
                continue

            dirX = -1 if xObjetivo - x < 0 else 1
            dirY = -1 if yObjetivo - y < 0 else 1
            xSiguiente = xObjetivo + dirX
            ySiguiente = yObjetivo + dirY
            if not self.posicionValida(xSiguiente, ySiguiente):
                continue
            if self.equipoEnCoordenadas(xObjetivo + dirX, yObjetivo + dirY):
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

        fichasComibles = self.opcionesComerFichaEnTablero(xFicha, yFicha)
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

    def comerEnCadenaFichaEnTablero(self, x, y):
        pass
        
    def movimientosFichaEnTablero(self, x, y):
        EH = []

        desplazamiento = self.desplazamientoFichaEnTablero(x, y)

        opcionesComer = self.opcionesComerFichaEnTablero(x, y)
        pass


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

class PruebasMovimiento(unittest.TestCase):
    def setUp(self):
        self.t = Tablero()

    def testRangoMovDamaSola(self):
        coordenadasConRespuestas = {
        (0, 0): 7,
        (1, 1): 1+1+1+6,
        (3, 3):3+3+3+4
        }
        for x, y in coordenadasConRespuestas:
            self.t.fichasDelEquipo["Blanco"][(x, y)] = self.t.DAMA
            rangoDama = self.t.rangoFichaEnTablero(x, y)
            self.assertEqual(len(rangoDama), coordenadasConRespuestas[ (x, y) ])

            self.t.fichasDelEquipo["Blanco"].pop( (x, y) )

    def testRangoMovDamaConFichas(self):
        e1 = self.t.EQUIPOS[0]
        e2 = self.t.EQUIPOS[1]
        self.t.fichasDelEquipo[e1][(3, 3)] = self.t.DAMA
        self.t.fichasDelEquipo[e1][(1, 1)] = self.t.PEON

        self.t.fichasDelEquipo[e2][(6, 6)] = self.t.PEON
        self.t.fichasDelEquipo[e2][(5, 1)] = self.t.DAMA
        self.t.fichasDelEquipo[e2][(1, 5)] = self.t.PEON

        rangoDama = self.t.rangoFichaEnTablero(3, 3)
        self.assertEqual(len(rangoDama), 2+2+2+3)

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

class PruebasComer(unittest.TestCase):
    def setUp(self):
        self.t = Tablero()

    def testPeonNoPuedeComerPeon(self):
        coorN = (3, 3)
        self.t.fichasDelEquipo["Negro"][ coorN ] = self.t.PEON
        coorB = (4, 4)
        self.t.fichasDelEquipo["Blanco"][ coorB ] = self.t.PEON
        self.t.fichasDelEquipo["Blanco"][ (5, 5) ] = self.t.PEON

        self.assertEqual(len(self.t.fichasDelEquipo["Negro"]), 1)
        self.assertEqual(len(self.t.fichasDelEquipo["Blanco"]), 2)

        simulacion = self.t.tableroEnElQueFichaComeAFicha( coorN[0], coorN[1], coorB[0], coorB[1] )
        self.assertIsNone(simulacion)

    def testPeonComePeon(self):
        coorN = (3, 3)
        self.t.fichasDelEquipo["Negro"][ coorN ] = self.t.PEON
        coorB = (4, 4)
        self.t.fichasDelEquipo["Blanco"][ coorB ] = self.t.PEON

        self.assertEqual(len(self.t.fichasDelEquipo["Negro"]), 1)
        self.assertEqual(len(self.t.fichasDelEquipo["Blanco"]), 1)

        simulacion = self.t.tableroEnElQueFichaComeAFicha( coorN[0], coorN[1], coorB[0], coorB[1] )
        self.assertEqual(len(self.t.fichasDelEquipo["Negro"]), 1)
        self.assertEqual(len(self.t.fichasDelEquipo["Blanco"]), 1)

        self.assertEqual(len(simulacion.fichasDelEquipo["Negro"]), 1)
        self.assertEqual(len(simulacion.fichasDelEquipo["Blanco"]), 0)

if __name__ == "__main__":
    unittest.main()
