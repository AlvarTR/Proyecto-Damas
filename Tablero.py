from Fichas import *
from ReglasDamas import *

class Tablero():
    def __init__(self, equipos=("Blanco", "Negro"), longTablero=8, relacionCasillasFichas=0.4, nuevoTablero=True):
        self.EQUIPOS = equipos
        self.LONG_TABLERO = longTablero
        self.RELACION_CASILLAS_FICHAS = relacionCasillasFichas
        self.FILAS_PEONES = int(self.LONG_TABLERO * self.RELACION_CASILLAS_FICHAS)

        self.peon = nuevoPeon()
        self.dama = nuevaDama(self.LONG_TABLERO)

        self.filaObjetivoPorEquipo = {self.EQUIPOS[0]:0, self.EQUIPOS[1]:self.LONG_TABLERO-1}
        self.turnoActual = 0
        self.fichasDelEquipo = {e:{} for e in self.EQUIPOS}
        self.fichasComidasPorElEquipo = {e:[] for e in self.EQUIPOS}

        self.ponFichasIniciales()

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
                for x in iter(x for x in range(self.LONG_TABLERO) if enPosicion(x, y, self.LONG_TABLERO)):
                    self.fichasDelEquipo[e][(x, y)] = self.peon

    def __str__(self):
        string = "_" * (2*self.LONG_TABLERO + 1) + "\n"

        for y in range(self.LONG_TABLERO):
            fila = ""
            for x in range(self.LONG_TABLERO):
                for e in self.fichasDelEquipo:
                    ficha = self.fichasDelEquipo[e].get( (x, y), None )
                    if ficha:
                        if isinstance(ficha, Peon):
                            fila += e[0].lower()
                        elif isinstance(ficha, Dama):
                            fila += e[0].capitalize()
                        break
                else:
                    fila += "_"

            fila = "|".join(fila)
            string += "|" + fila + "| \n"

        return string

    def __copy__(self):
        t = Tablero(self.EQUIPOS, self.LONG_TABLERO, self.RELACION_CASILLAS_FICHAS)
        t.turnoActual = self.turnoActual
        t.fichasDelEquipo = {e:{} for e in self.EQUIPOS}
        t.fichasComidasPorElEquipo = {e:[] for e in self.EQUIPOS}
        for e in self.EQUIPOS:
            for coor, ficha in self.fichasDelEquipo[e].items():
                if isinstance(ficha, Peon):
                    t.fichasDelEquipo[e][coor] = t.peon
                elif isinstance(ficha, Dama):
                    t.fichasDelEquipo[e][coor] = t.dama

            for ficha in self.fichasComidasPorElEquipo[e]:
                if ficha.isinstance(Peon):
                    t.fichasComidasPorElEquipo[coor] = t.peon
                elif ficha.isinstance(Dama):
                    t.fichasComidasPorElEquipo[coor] = t.dama
        return t

if __name__ == "__main__":
    t = Tablero()
    t.fichasDelEquipo["Negro"].pop( (0, 0) )
    tCopia = t.__copy__()
    t.fichasDelEquipo["Negro"].pop( (2, 0) )
    print(t)
    print(tCopia)
