from ReglasJuego import ReglasJuego
from copy import copy, deepcopy

class Ficha(ReglasJuego):
    def __init__(self, x, y, equipo, filaObjetivo, LONG_TABLERO=8, movimientos=0, fichasComidas=[]):
        #super() hace de self, asi que solo queda 1 argumento
        super().__init__(LONG_TABLERO)
        if self.enPosicion(x, y):
            self.equipo = equipo
            self.filaObjetivo = filaObjetivo
            self.x = x
            self.y = y
            self.movimientos = movimientos
            self.fichasComidas = fichasComidas
            self.turnoComida = -1

    def movimientosPosibles(self):
        pass

    def moverA(self, xObjetivo, yObjetivo):
        if not self.enPosicion(xObjetivo, yObjetivo):
            return
        self.x = xObjetivo
        self.y = yObjetivo

    def comida(self, turno):
        self.x = self.LONG_TABLERO
        self.y = self.LONG_TABLERO
        self.turnoComida = turno

    def comeA(self, ficha, turno):
        EH = False
        if not isinstance(ficha, Ficha):
            return EH
        if (ficha.x, ficha.y) not in self.movimientosPosibles():
            return EH
        if self.equipo == ficha.equipo:
            return EH

        fichaComida = ficha.__copy__()
        fichaComida.turnoComida = turno
        self.fichasComidas.append( fichaComida )
        ficha.comida(turno)
        return True

    def __str__(self):
        string = "%s, equipo %s, posicion (%d, %d)" % (type(self), self.equipo, self.x, self.y)
        if self.turnoComida >= 0:
            string += ", comida el turno %d" % self.turnoComida
        return string

    def __copy__(self):
        return type(self)(self.x, self.y, self.equipo, self.filaObjetivo, self.LONG_TABLERO, self.movimientos)

class Peon(Ficha):
    def movimientosPosibles(self):
        CASILLAS_MOV = 1
        direccionPermitida = -1 if self.filaObjetivo - self.y < 0 else 1

        for i in range(-CASILLAS_MOV, CASILLAS_MOV + 1):
            if i == 0:
                continue

            x = self.x - i
            for y in [self.y - i, self.y + i]:
                direccionMov = -1 if y - self.y < 0 else 1
                if direccionMov == direccionPermitida:
                    if self.enPosicion(x, y):
                        yield (x, y)

    def __repr__(self):
        return self.equipo[0].lower()

class Dama(Ficha):
    def movimientosPosibles(self):
        i = 0 - self.x
        auxX = self.x + i
        while auxX < self.LONG_TABLERO:
            if i != 0:
                for auxY in [self.y + i, self.y - i]:
                    if self.enPosicion(auxX, auxY):
                        yield (auxX, auxY)

            i += 1
            auxX = self.x + i

    def __repr__(self):
        return self.equipo[0].capitalize()

if __name__ == "__main__":
    a = Peon(0,0, "a", 0)
    b = Peon(1,1, "b", 7)
    print(a.comeA(b, 1))
    print(a)
    print(b)
