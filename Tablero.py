from Fichas import *
import ReglasDamas

class Tablero():
    def __init__(self, equipos=("Blanco", "Negro"), longTablero=8, relacionCasillasFichas=0.4, nuevoTablero=True):
        self.EQUIPOS = equipos
        self.LONG_TABLERO = longTablero
        self.RELACION_CASILLAS_FICHAS = relacionCasillasFichas
        self.FILAS_PEONES = int(self.LONG_TABLERO * self.RELACION_CASILLAS_FICHAS)

        self.PEON = nuevoPeon()
        self.DAMA = nuevaDama(self.LONG_TABLERO)

        self.filaObjetivoPorEquipo = {self.EQUIPOS[0]:0, self.EQUIPOS[1]:self.LONG_TABLERO-1}
        self.turnoActual = 0
        self.fichasDelEquipo = {e:{} for e in self.EQUIPOS}
        self.fichasComidasPorElEquipo = {e:[] for e in self.EQUIPOS}

        if nuevoTablero:
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
                for x in iter(x for x in range(self.LONG_TABLERO) if ReglasDamas.posicionValida(x, y, self.LONG_TABLERO)):
                    self.fichasDelEquipo[e][(x, y)] = self.PEON

    def __str__(self):
        string = "\n"

        for y in range(self.LONG_TABLERO):
            for x in range(self.LONG_TABLERO):
                ficha = None
                e = self.equipoEnCoordenadas(x, y)
                if e:
                    ficha = self.fichasDelEquipo[e][(x, y)]

                if isinstance(ficha, Peon):
                    string += e[0].lower()
                elif isinstance(ficha, Dama):
                    string += e[0].capitalize()
                else:
                    string += "_"

            string += "\n"

        string = "|".join(string)
        string = "_" * (2*self.LONG_TABLERO + 1) + string

        return string

    def __copy__(self):
        t = Tablero(self.EQUIPOS, self.LONG_TABLERO, self.RELACION_CASILLAS_FICHAS, False)
        t.turnoActual = self.turnoActual

        for e in self.EQUIPOS:
            for coor, ficha in self.fichasDelEquipo[e].items():
                if isinstance(ficha, Peon):
                    t.fichasDelEquipo[e][coor] = t.PEON
                elif isinstance(ficha, Dama):
                    t.fichasDelEquipo[e][coor] = t.DAMA

            for ficha in self.fichasComidasPorElEquipo[e]:
                if isinstance(ficha, Peon):
                    t.fichasComidasPorElEquipo[e].append(t.PEON)
                elif isinstance(ficha, Dama):
                    t.fichasComidasPorElEquipo[e].append(t.DAMA)
        return t

    def equipoEnCoordenadas(self, x, y):
        EH = None
        if not ReglasDamas.posicionValida(x, y, self.LONG_TABLERO):
            return EH

        for e, fichasEquipo in self.fichasDelEquipo.items():
            if (x, y) in fichasEquipo:
                return e
        else:
            return EH



if __name__ == "__main__":
    t = Tablero()
    t.fichasDelEquipo["Negro"].pop( (0, 0) )
    tCopia = t.__copy__()
    t.fichasDelEquipo["Negro"].pop( (2, 0) )
    print(t)
    print(tCopia)
