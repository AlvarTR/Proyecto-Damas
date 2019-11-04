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
                        final = primeraFila + self.FILAS_PEONES-1 #-1 para que se comporte bien el bucle

                    for y in range(inicial, final+1): #+1 porque "final" es el ultimo valor que queremos rellenar
                        if self.enPosicion(x, y):
                            nuevaFicha = Peon(x, y, e, self.filaObjetivoPorEquipo[e], self.LONG_TABLERO)
                            self.fichasPorEquipo[e].add(nuevaFicha)

        ponerPiezas()

    #----------CHECKS----------
    def fichaEstaEnTablero(self, *fichas):
        EH = False
        for ficha in fichas:
            if not isinstance(ficha, Ficha):
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
                iX = x + dirX
                iY = y + dirY
                while self.enPosicion(iX, iY):
                    movimientos.remove( (iX, iY) )
                    iX += dirX
                    iY += dirY

        return movimientos

    def movValidosFicha(self, ficha):
        EH = set([])
        if not self.fichaEstaEnTablero(ficha):
            return EH

        movimientosValidos = set([])
        movimientos = self.movPosiblesFicha(ficha)
        for xObjetivo, yObjetivo in movimientos:
            valido = False
            fichaEncontrada = self.fichaEnCoordenadas(xObjetivo, yObjetivo)
            destinosValidos = set([])
            if fichaEncontrada:
                if self.posicionAlComer(ficha, fichaEncontrada):
                    pass
            else:
                destinosValidos.add( (xObjetivo, yObjetivo) )
            if destinosValidos:
                for destino in destinosValidos:
                    movimientosValidos.add( destino )

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

        if self.fichaEnCoordenadas(xObjetivo, yObjetivo):
            pass
        else:
            ficha.moverA(xObjetivo, yObjetivo)

        return True

    #----------COMER----------
    def posicionAlComer(self, fichaCome, fichaAComer):
        EH = ()
        if self.fichaEstaEnTablero(fichaCome, fichaAComer):
            return EH
        if fichaCome.equipo is fichaAComer.equipo:
            return EH
        if (fichaAComer.x, fichaAComer.y) not in fichaCome.movimientosPosibles():
            return EH

        dirX = -1 if fichaAComer.x - fichaComida.x < 0 else 1
        dirY = -1 if fichaAComer.y - fichaComida.y < 0 else 1
        saltoX = fichaCome.x + 2*dirX
        saltoY = fichaCome.y + 2*dirY
        if self.fichaEnCoordenadas(saltoX, saltoY):
            return EH

        return (saltoX, saltoY)

    def movPosiblesAlComer(self, ficha, historico=[]):
        EH = set([])
        if not self.fichaEstaEnTablero(ficha):
            return EH

        movimientos = self.movPosiblesFicha(self, ficha)
        pass

    def comeFicha(self, fichaCome, fichaAComer):
        pass

    def retiraFichaComida(self, fichaCome, fichaComida):
        EH = False
        if not puedeComer(fichaCome, fichaComida):
            return EH

        self.fichasComidasPorEquipo[fichaCome.equipo].append(fichaAComer)
        self.fichasPorEquipo[fichaComida.equipo].remove(fichaAComer)
        fichaCome.comeA(fichaComida, self.turnoActual)
        return True

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

if __name__ == "__main__":
    t = Tablero()
    print(t)
    print("Mov negro:", t.movValidosEquipo("Negro"))
    for e in t.fichasPorEquipo:
        for f in t.fichasPorEquipo[e]:
            print(f, t.fichaEstaEnTablero(f))
