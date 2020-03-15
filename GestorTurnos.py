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

        self.io.intro()


    def turnoConcluido(self):
        self.turno += 1
        iteradorEquipoActual = self.turno % self.NUM_EQUIPOS
        self.equipoActual = self.tablero.EQUIPOS[iteradorEquipoActual]

        if iteradorEquipoActual == 0:
            self.ronda = int(self.turno / self.NUM_EQUIPOS)


    def equipoSinFichas(self):
        for e in self.tablero.EQUIPOS:
            if self.tablero.fichasPorEquipo[e]:
                return e


    def moverFicha(self, xFicha, yFicha, xObjetivo, yObjetivo):
        if not any( coor for coor in self.tablero.movimientosFicha(xFicha, yFicha) if coor == (xObjetivo, yObjetivo) ):
            return None

        return self.tablero.tableroTrasMovimientoFicha(xFicha, yFicha, xObjetivo, yObjetivo)


    def turnoJugador(self):
        #Comprueba de quien es el turno
        self.io.output(self)
        #Haz un movimiento (comer o desplazarse)
        x, y = self.io.recogeCoordenadas("Indique las coordenadas de la ficha que quiere mover ")
        #Comprueba si alguna ficha del equipo esta en posicion de dama
            #Si es asi, actualiza esa ficha y termina el turno
        #Comer implica
        #Termina el turno
        self.turnoConcluido()

    def turnoIA(self):
        pass


    def jugadorContraIA(self):
        e = None
        while True:
            self.turnoJugador()
            e = self.equipoSinFichas()
            if e:
                self.io.output(e, "ha perdido")
            self.turnoIA()
            if e:
                self.io.output(e, "ha perdido")

    def jugadorContraJugador(self):
        e = None
        while True:
            self.turnoJugador()
            e = self.equipoSinFichas()
            if e:
                self.io.output(e, "ha perdido")
            self.turnoJugador()
            if e:
                self.io.output(e, "ha perdido")


    def __str__(self):
        string = "Turno del equipo " + self.equipoActual + "\n"
        string += self.tablero.tableroConMovimientosEquipo(self.equipoActual) + "\n"
        return string

class PruebasTurnos(unittest.TestCase):
    def setUp(self):
        self.gturnos = GestorTurnos()

    def testInicial(self):
        pass

if __name__ == "__main__":
    unittest.main()
