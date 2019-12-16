from Fichas import nuevoPeon, nuevaDama

class Tablero():
    def __init__(self, equipos=("Blanco", "Negro"), longTablero=8, relacionCasillasFichas=0.4):
        self.LONG_TABLERO = longTablero
        self.FILAS_PEONES = int(self.LONG_TABLERO * relacionCasillasFichas)
        self.equipos = equipos

        self.peonDelEquipo = {e:nuevoPeon(e) for e in self.equipos}
        self.damaDelEquipo = {e:nuevaDama(e, self.LONG_TABLERO) for e in self.equipos}

        self.filaObjetivoPorEquipo = {self.equipos[0]:0, self.equipos[1]:self.LONG_TABLERO-1}
        self.turnoActual = 0
        self.fichasPorEquipo = {}
        self.fichasComidasPorEquipo = {}

        def ponerPiezas():
            self.fichasPorEquipo = {self.equipos[0]:{}, self.equipos[1]:{}}
            self.fichasComidasPorEquipo = {self.equipos[0]:[], self.equipos[1]:[]}
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
                    for x in iter(x for x in range(self.LONG_TABLERO) if self.enPosicion(x, y)):
                        self.fichasPorEquipo[e][(x, y)] = self.peonDelEquipo[e]

        ponerPiezas()

    def enPosicion(self, x, y):
        if x >= 0 and x < self.LONG_TABLERO:
            if y >= 0 and y < self.LONG_TABLERO:
                if (x + y) % 2 == 0:
                    return True
        return False

    def __str__(self):
        tablero = []
        for fila in range(self.LONG_TABLERO):
            tablero.append([])
            for casilla in range(self.LONG_TABLERO):
                tablero[-1].append(None)

        for e in self.fichasPorEquipo:
            for (x, y), f in self.fichasPorEquipo[e].items():
                tablero[x][y] = f

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
if __name__ == "__main__":
    t = Tablero()
    print(t)
