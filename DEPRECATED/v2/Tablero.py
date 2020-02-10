from Fichas import *
import ReglasDamas
import unittest

Movimientos = namedtuple("Movimientos", ["coordenada", "movs"])

class Tablero():
    def __init__(self, longTablero=8, relacionCasillasFichas=0.4, equipos=("Blanco", "Negro")):
        self.LONG_TABLERO = longTablero
        self.RELACION_CASILLAS_FICHAS = relacionCasillasFichas
        self.FILAS_PEONES = int(self.LONG_TABLERO * self.RELACION_CASILLAS_FICHAS)

        self.EQUIPOS = equipos

        self.PEON = nuevoPeon()
        self.DAMA = nuevaDama(self.LONG_TABLERO)

        self.filaObjetivoPorEquipo = {self.EQUIPOS[0]:0, self.EQUIPOS[1]:self.LONG_TABLERO-1}
        self.turnoActual = 0
        self.fichasDelEquipo = {e:{} for e in self.EQUIPOS}
        self.fichasComidasPorElEquipo = {e:[] for e in self.EQUIPOS}

    def ponFicha(self, ficha, equipo, x, y):
        EH = False
        if not ReglasDamas.posicionValida(x, y, self.LONG_TABLERO):
            return EH
        if equipo not in self.EQUIPOS:
            return EH
        if ficha is not (self.PEON or self.DAMA):
            return EH
        if not self.equipoEnCoordenadas(x, y):
            return EH

        self.fichasDelEquipo[equipo][(x, y)] = ficha
        return True

    def quitaFicha(self, x, y):
        EH = None

        equipo = self.equipoEnCoordenadas(x, y)
        if not equipo:
            return EH

        ficha = self.fichasDelEquipo[equipo][ (x,y) ]
        self.fichasDelEquipo[equipo][ (x, y) ] = None
        return ficha

    def ponFichasIniciales(self):
        primeraFila = 0
        ultimaFila = self.LONG_TABLERO - 1

        for e in self.filaObjetivoPorEquipo:
            inicial = primeraFila
            final = ultimaFila
            if self.filaObjetivoPorEquipo[e] == primeraFila:
                inicial = self.LONG_TABLERO - self.FILAS_PEONES
            elif self.filaObjetivoPorEquipo[e] == ultimaFila:
                final = primeraFila + self.FILAS_PEONES-1 #-1 para hacer 0 -> self.FILAS_PEONES-1 (2) en el bucle

            for y in range(inicial, final+1): #+1 porque "final" es el ultimo valor que queremos rellenar
                for x in iter(x for x in range(self.LONG_TABLERO) if ReglasDamas.posicionValida(x, y, self.LONG_TABLERO)):
                    self.fichasDelEquipo[e][(x, y)] = self.PEON

    def numFichasEnTablero(self):
        contador = 0
        for e in self.fichasDelEquipo:
            # Se podria hacer con sum(), pero me parece mas complicado
            contador += len( self.fichasDelEquipo[e] )
        return contador

    def equipoEnCoordenadas(self, x, y):
        EH = None
        if not ReglasDamas.posicionValida(x, y, self.LONG_TABLERO):
            return EH

        for e, fichasEquipo in self.fichasDelEquipo.items():
            if (x, y) in fichasEquipo:
                return e
        else:
            return EH


    def movimientosEnCoordenadas(self, x, y):
        EH = None

        equipo = self.equipoEnCoordenadas(x, y)
        if not equipo:
            return EH

        return self._movimientosValidosFicha(equipo, x, y)


    def _movimientosValidosFicha(self, equipo, x, y):
        """
        Se espera que el equipo ya este comprobado de antemano.
        """
        EH = None

        dictEquipo = self.fichasDelEquipo.get(equipo, None)
        if not dictEquipo:
            return EH

        ficha = dictEquipo.get( (x, y), None )
        if not ficha:
            return EH

        movimientos = self._movimientosFicha(equipo, x, y)
        movimientosValidos = Movimientos(coordenada=(x, y), movs=[])

        ficha = self.quitaFicha(x, y)
        for xMov, yMov in movimientos.movs:
            equipoDeFichaObjetivo = self.equipoEnCoordenadas(xMov, yMov)
            if not equipoDeFichaObjetivo:
                movimientosValidos.movs.append( (xMov, yMov) )
            else:
                if equipoDeFichaObjetivo is not equipo:
                    #TODO mejorar
                    movimientosValidos.movs.append(self._fichaComeA(ficha, equipo, x, y, xMov, yMov))
        self.ponFicha(ficha, equipo, x, y)

        if not movimientosValidos.movs:
            return EH

        return movimientosValidos

    def _movimientosFicha(self, equipo, x, y):
        """
        Se espera que el equipo ya este comprobado de antemano.
        """
        EH = None
        dictEquipo = self.fichasDelEquipo.get(equipo, None)
        if not dictEquipo:
            return EH

        ficha = dictEquipo.get( (x, y), None )
        if not ficha:
            return EH

        dirY = -1 if self.filaObjetivoPorEquipo[equipo] - y < 0 else 1
        movs = []
        i = 0
        while i < ficha.movMax:
            i += 1

            yAlante = y + i*dirY
            yAtras = y - i*dirY

            for auxY in (yAlante, yAtras):
                if auxY == yAtras and not ficha.puedeIrAtras:
                    continue

                for auxX in (x - i, x + i):
                    if not ReglasDamas.posicionValida(auxX, auxY, self.LONG_TABLERO):
                        continue

                    movs.append( (auxX, auxY) )

        return Movimientos( coordenada=(x, y), movs=movs )


    def _fichaComeA(self, ficha, equipo, xInicial, yInicial, xObjetivo, yObjetivo):
        EH = []
        if xInicial == xObjetivo:
            return EH
        if yInicial == yObjetivo:
            return EH
        #En posicion objetivo tiene que haber una ficha
        equipoObjetivo = self.equipoEnCoordenadas(xObjetivo, yObjetivo)
        if not equipoObjetivo:
            return EH
        if equipo == equipoObjetivo:
            return EH
        #TODO: + ERROR HANDLING
        dirX = -1 if xObjetivo - xInicial < 0 else 1
        dirY = -1 if yObjetivo - yInicial < 0 else 1

        if self.equipoEnCoordenadas(xObjetivo + dirX, yObjetivo + dirY):
            return EH
        coorDespuesDeComer = (xObjetivo + dirX, yObjetivo + dirY)

        self.ponFicha(ficha, equipo, coorDespuesDeComer[0], coorDespuesDeComer[1])
        movsPosiblesDespuesDeComer = self._movimientosFicha(equipo, coorDespuesDeComer[0], coorDespuesDeComer[1])
        self.quitaFicha(coorDespuesDeComer[0], coorDespuesDeComer[1])

        movimientosRecursivos = Movimientos(coordenada=coorDespuesDeComer, movs=[])
        if movsPosiblesDespuesDeComer:
            for xMov, yMov in movsPosiblesDespuesDeComer.movs:
                equipoDeFichaObjetivo = self.equipoEnCoordenadas(xMov, yMov)
                if not equipoDeFichaObjetivo:
                    continue
                if equipoDeFichaObjetivo is equipo:
                    continue

                movimientosRecursivos.movs.append(self._fichaComeA(ficha, equipo, coorDespuesDeComer[0], coorDespuesDeComer[1], xMov, yMov))

        resultado = []
        resultado.append( [coorDespuesDeComer] )
        for mov in movimientosRecursivos.movs:
            resultado[-1].append(movimientosRecursivos.movs)
            resultado.append( [coorDespuesDeComer] )
        return resultado



    def movimientosEquipo(self, equipo):
        EH = None

        if equipo not in self.EQUIPOS:
            return EH

        for (x, y) in self.fichasDelEquipo[equipo]:
            movimientosValidos = self._movimientosValidosFicha(equipo, x, y)
            if movimientosValidos:
                yield movimientosValidos


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
        t = Tablero(self.LONG_TABLERO, self.RELACION_CASILLAS_FICHAS, self.EQUIPOS)
        t.turnoActual = self.turnoActual

        for e in self.EQUIPOS:
            for coor, ficha in self.fichasDelEquipo[e].items():
                if ficha is self.PEON:
                    t.fichasDelEquipo[e][coor] = t.PEON
                elif ficha is self.DAMA:
                    t.fichasDelEquipo[e][coor] = t.DAMA

            for ficha in self.fichasComidasPorElEquipo[e]:
                if ficha is self.PEON:
                    t.fichasComidasPorElEquipo[e].append(t.PEON)
                elif ficha is self.DAMA:
                    t.fichasComidasPorElEquipo[e].append(t.DAMA)
        return t


class PruebasTablero(unittest.TestCase):
    def setUp(self):
        self.t = Tablero()
        self.t.ponFichasIniciales()

    def testCopiaEliminandoUnaFicha(self):
        copiaT = self.t.__copy__()
        coor = (0, 0)
        e = copiaT.equipoEnCoordenadas(coor[0], coor[1])
        copiaT.fichasDelEquipo[e].pop( coor )
        self.assertTrue(self.t.numFichasEnTablero() > copiaT.numFichasEnTablero())

    def testMovsIniciales(self):
        listaMovimientos = []
        for e in self.t.fichasDelEquipo:
            listaMovimientos = list(self.t.movimientosEquipo(e))
            self.assertEqual(len(listaMovimientos), 4)

            casillasPosiblesAlMover = []
            for movimiento in listaMovimientos:
                for m in movimiento.movs:
                    casillasPosiblesAlMover.append(m)

            self.assertEqual(len(casillasPosiblesAlMover), 7)

    def testComerEncadenado(self):
        t = Tablero()
        t.fichasDelEquipo[ t.EQUIPOS[0] ][ (0, 0) ] = t.PEON
        t.fichasDelEquipo[ t.EQUIPOS[1] ][ (1, 1) ] = t.PEON
        t.fichasDelEquipo[ t.EQUIPOS[1] ][ (3, 3) ] = t.PEON
        t.fichasDelEquipo[ t.EQUIPOS[1] ][ (5, 5) ] = t.PEON
        movimientos = t.movimientosEnCoordenadas(0, 0)
        print(t)
        print(movimientos)
        self.assertTrue(movimientos)
        self.assertTrue(movimientos.movs)
        self.assertEqual(len(movimientos.movs), 1)
        self.assertEqual(len(movimientos.movs[0]), 3)



if __name__ == "__main__":
    unittest.main()
