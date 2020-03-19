import ValoresPorDefecto as vpd
import DamasPorConsola
import Tablero
import unittest

class GestorTurnos():
    def __init__(self, longTablero=vpd.LONG_TABLERO, equipos=vpd.EQUIPOS):
        self.NUM_EQUIPOS = len(equipos)

        self.tablero = Tablero.Tablero(longTablero, equipos)
        self.tablero.colocaFichasIniciales()

        self.io = DamasPorConsola.DamasPorConsola()

        self.turno = 0
        self.ronda = 0

        self.equipoActual = None
        self.turnoConcluido()
        print(self.equipoActual)

        self.io.intro()


    def turnoConcluido(self):
        self.turno += 1
        iteradorEquipoActual = self.turno % self.NUM_EQUIPOS
        self.equipoActual = self.tablero.EQUIPOS[iteradorEquipoActual]

        if iteradorEquipoActual == 0:
            self.ronda = int(self.turno / self.NUM_EQUIPOS)

    def equipoSinFichas(self):
        for e in self.tablero.EQUIPOS:
            if not self.tablero.fichasDelEquipo[e]:
                return e


    def moverFicha(self, xFicha, yFicha, xObjetivo, yObjetivo):
        if not any( coor for coor in self.tablero.movimientosFicha(xFicha, yFicha) if coor == (xObjetivo, yObjetivo) ):
            return None

        return self.tablero.tableroTrasMovimientoFicha(xFicha, yFicha, xObjetivo, yObjetivo)


    def turnoJugador(self):
        #Comprueba de quien es el turno
        self.io.output(self)

        #Comprueba coordenadas que se introducen
        x, y = (-1, -1)
        while x < 0 or y < 0:
            x = self.io.recogeCoordenada("Coordenada x de la ficha que quiere mover ")
            y = self.io.recogeCoordenada("Coordenada y de la ficha que quiere mover ")

            if not (x, y) in self.tablero.fichasDelEquipo[self.equipoActual]:
                self.io.output("Esas coordenadas no tienen una ficha de tu equipo")
                x, y = (-1, -1)
                continue
            if not any( coor for coor in self.tablero.movimientosFicha(x, y) ):
                self.io.output("Esa ficha no tiene movimiento")
                x, y = (-1, -1)
                continue

            self.io.output(self.tablero.tableroConMovimientosFicha(x, y))

            xObjetivo = self.io.recogeCoordenada("Coordenada x donde quiere mover ")
            yObjetivo = self.io.recogeCoordenada("Coordenada y donde quiere mover ")
            if not any( coor for coor in self.tablero.movimientosFicha(x, y) if coor == (xObjetivo, yObjetivo) ):
                self.io.output("Esas coordenadas no corresponden con un destino de esta ficha")
                x, y = (-1, -1)
                continue
        #Haz un movimiento (comer o desplazarse)


        #Comprueba si alguna ficha del equipo esta en posicion de dama
            #Si es asi, actualiza esa ficha y termina el turno
        #Comer implica seguir comiendo siempre que sea posible
        #Termina el turno
        self.turnoConcluido()

    def turnoIA(self):
        pass

    def equipoQueHaPerdido(self):
        e = self.equipoSinFichas()
        if e:
            self.io.output(e + " ha perdido")
        return e

    def jugadorContraIA(self):
        while True:
            self.turnoJugador()
            if self.equipoQueHaPerdido():
                break
            self.turnoIA()
            if self.equipoQueHaPerdido():
                break

    def jugadorContraJugador(self):
        while True:
            self.turnoJugador()
            if self.equipoQueHaPerdido():
                break
            self.turnoJugador()
            if self.equipoQueHaPerdido():
                break


    def __str__(self):
        string = "Turno del equipo " + self.equipoActual + "\n"
        string += self.tablero.tableroConMovimientosEquipo(self.equipoActual) + "\n"
        return string

class PruebasTurnos(unittest.TestCase):
    def setUp(self):
        self.gturnos = GestorTurnos()
        self.gturnos.jugadorContraJugador()

    def testInicial(self):
        pass

if __name__ == "__main__":
    unittest.main()
