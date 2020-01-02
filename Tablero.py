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


    def movimientosFichaEnCoordenadas(self, x, y):
        EH = None

        equipo = self.equipoEnCoordenadas(x, y)
        if not equipo:
            return EH

        return self._movimientosFicha(equipo, x, y)

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
        movs = set([])
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

                    equipoFichaEncontrada = self.equipoEnCoordenadas(auxX, auxY)
                    if equipoFichaEncontrada:
                        if equipoFichaEncontrada is equipo:
                            continue
                        # TODO comer fichas
                        continue

                    movs.add( (auxX, auxY) )

        return Movimientos( coordenada=(x, y), movs=movs )


    def movimientosEquipo(self, equipo):
        EH = None

        if equipo not in self.EQUIPOS:
            return EH

        for (x, y) in self.fichasDelEquipo[equipo]:
            movsFicha = self._movimientosFicha(equipo, x, y)
            if movsFicha.movs:
                yield self._movimientosFicha(equipo, x, y)



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




if __name__ == "__main__":
    t = Tablero()
    t.ponFichasIniciales()

    unittest.main()
