from Fichas import *
from ReglasJuego import *

class Tablero():
    def __init__(self, equipos=("Blanco", "Negro"), longTablero=8, relacionCasillasFichas=0.4, nuevoTablero=True):
        self.EQUIPOS = equipos
        self.LONG_TABLERO = longTablero
        self.RELACION_CASILLAS_FICHAS = relacionCasillasFichas
        self.FILAS_PEONES = int(self.LONG_TABLERO * self.RELACION_CASILLAS_FICHAS)

        self.peonDelEquipo = {e:nuevoPeon(e) for e in self.EQUIPOS}
        self.damaDelEquipo = {e:nuevaDama(e, self.LONG_TABLERO) for e in self.EQUIPOS}

        self.filaObjetivoPorEquipo = {self.EQUIPOS[0]:0, self.EQUIPOS[1]:self.LONG_TABLERO-1}
        self.turnoActual = 0
        self.fichasDelEquipo = {e:{} for e in self.EQUIPOS}
        self.fichasComidasPorElEquipo = {e:[] for e in self.EQUIPOS}

        if nuevoTablero:
            self.ponerPiezas()

    def ponerPiezas(self):
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
                for x in iter(x for x in range(self.LONG_TABLERO) if enPosicion(x, y, self.LONG_TABLERO)):
                    self.fichasDelEquipo[e][(x, y)] = self.peonDelEquipo[e]


    def __str__(self):
        tablero = []
        for fila in range(self.LONG_TABLERO):
            tablero.append([])
            for casilla in range(self.LONG_TABLERO):
                tablero[-1].append(None)

        for e in self.fichasDelEquipo:
            for (x, y), f in self.fichasDelEquipo[e].items():
                tablero[x][y] = f

        string = "_" * (2*self.LONG_TABLERO + 1) + "\n"

        for y in range(self.LONG_TABLERO):
            fila = ""
            for x in range(self.LONG_TABLERO):
                if tablero[x][y] is not None:
                    fila += tablero[x][y].__repr__()
                else:
                    fila += "_"

            fila = "|".join(fila)
            string += "|" + fila + "| \n"

        return string

    def __copy__(self):
        t = Tablero(self.EQUIPOS, self.LONG_TABLERO, self.RELACION_CASILLAS_FICHAS, False)
        t.turnoActual = self.turnoActual
        for e in self.EQUIPOS:
            peon = t.peonDelEquipo[e]
            dama = t.damaDelEquipo[e]

            for coor, ficha in self.fichasDelEquipo[e].items():
                if isinstance(ficha, Peon):
                    t.fichasDelEquipo[e][coor] = peon
                elif isinstance(ficha, Dama):
                    t.fichasDelEquipo[e][coor] = dama

            for ficha in self.fichasComidasPorElEquipo[e]:
                if ficha.isinstance(Peon):
                    t.fichasComidasPorElEquipo[coor] = peon
                elif ficha.isinstance(Dama):
                    t.fichasComidasPorElEquipo[coor] = dama

        return t

if __name__ == "__main__":
    t = Tablero()
    t.fichasDelEquipo["Negro"].pop( (0, 0) )
    tCopia = t.__copy__()
    t.fichasDelEquipo["Negro"].pop( (2, 0) )
    print(t)
    print(tCopia)
