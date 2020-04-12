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
        iteradorEquipoActual = self.turno % self.NUM_EQUIPOS
        self.equipoActual = self.tablero.EQUIPOS[iteradorEquipoActual]

        if iteradorEquipoActual == 0:
            self.ronda = int(self.turno / self.NUM_EQUIPOS)
        self.turno += 1

    def moverFicha(self, xFicha, yFicha, xObjetivo, yObjetivo):
        if not any( coor for coor in self.tablero.movimientosFicha(xFicha, yFicha) if coor == (xObjetivo, yObjetivo) ):
            return None

        return self.tablero.tableroTrasMovimientoFicha(xFicha, yFicha, xObjetivo, yObjetivo)


    def turnoJugador(self):
        x = -1
        while x < 0:
            #Comprueba de quien es el turno
            self.io.output(self)

            #Comprueba coordenadas que se introducen
            x = self.io.recogeCoordenada("Coordenada x de la ficha que quiere mover ")
            y = self.io.recogeCoordenada("Coordenada y de la ficha que quiere mover ")

            if not (x, y) in self.tablero.fichasDelEquipo[self.equipoActual]:
                self.io.output("Esas coordenadas no tienen una ficha de tu equipo")
                x = -1
                continue
            if not any( coor for coor in self.tablero.movimientosFicha(x, y) ):
                self.io.output("Esa ficha no tiene movimiento")
                x = -1
                continue

            self.io.output(self.tablero.tableroConMovimientosFicha(x, y))

            xObjetivo = self.io.recogeCoordenada("Coordenada x donde quiere mover ")
            yObjetivo = self.io.recogeCoordenada("Coordenada y donde quiere mover ")
            if not any( coor for coor in self.tablero.movimientosFicha(x, y) if coor == (xObjetivo, yObjetivo) ):
                self.io.output("Esas coordenadas no corresponden con un destino de esta ficha")
                x = -1
                continue

        #Haz un movimiento (comer o desplazarse)
        nuevoTablero = self.moverFicha(x, y, xObjetivo, yObjetivo)

        #Comprueba si alguna ficha del equipo esta en posicion de dama
        damaColocada = nuevoTablero.peonesPorDamas()
            #Si es asi, actualiza esa ficha y termina el turno
        if damaColocada:
            self.turnoConcluido()
            return damaColocada

        i = 1
        viejoTablero = self.tablero
        while (xObjetivo, yObjetivo) in viejoTablero.movimientosTrasComerFicha(x, y) and any(nuevoTablero.movimientosTrasComerFicha(xObjetivo, yObjetivo)):
            if i == 1:
                self.io.output("Combo!!")
            elif i > 1:
                self.io.output("Combo x"+str(i)+"!!")

            x, y = xObjetivo, yObjetivo
            self.tablero = nuevoTablero

            xObjetivo = -1
            while xObjetivo < 0:
                self.io.output(self.tablero.tableroConComidaFicha(x, y))

                xObjetivo = self.io.recogeCoordenada("Coordenada x donde quiere mover ")
                yObjetivo = self.io.recogeCoordenada("Coordenada y donde quiere mover ")
                if not any( coor for coor in self.tablero.movimientosTrasComerFicha(x, y) if coor == (xObjetivo, yObjetivo) ):
                    self.io.output("Esas coordenadas no corresponden con un destino de esta ficha")
                    xObjetivo = -1
                    continue

            nuevoTablero = self.moverFicha(x, y, xObjetivo, yObjetivo)

            #Comprueba si alguna ficha del equipo esta en posicion de dama
            damaColocada = nuevoTablero.peonesPorDamas()
                #Si es asi, actualiza esa ficha y termina el turno
            if damaColocada:
                self.turnoConcluido()
                return damaColocada

        #Comer implica seguir comiendo siempre que sea posible
        #Termina el turno
        self.turnoConcluido()
        return nuevoTablero

    def turnoIA(self):
        nuevoTablero = None
        ## TODO
        self.turnoConcluido()
        return nuevoTablero


    def equipoGanador(self):
        ganador = None
        for equipo in self.tablero.EQUIPOS:
            if not self.tablero.fichasDelEquipo[equipo]:
                continue
            if any(self.tablero.movimientosEquipo(equipo)):
                continue

            if ganador:
                ganador = None
                break

            ganador = equipo
        return ganador

    def imprimeEquipoGanador(self):
        self.io.output(self.equipoGanador() + "ha ganado")


    def jugadorContraIA(self):
        while not self.equipoGanador():
            self.tablero = self.turnoJugador()
            if self.equipoGanador():
                break

            self.tablero = self.turnoIA()
        self.imprimeEquipoGanador()

    def jugadorContraJugador(self):
        while not self.equipoGanador():
            self.tablero = self.turnoJugador()
        self.imprimeEquipoGanador()


    def __str__(self):
        string = ""
        string += str(self.tablero) + "\n"
        string += "Turno del equipo " + self.equipoActual + "\n"
        return string


    def imprimeEquipoPerdedor(self):
        ## DEPRECATED
        e = self.equipoSinFichas()
        if e:
            self.io.output(e + " ha perdido")
        return e

    def equipoSinFichas(self):
        ## DEPRECATED
        for e in self.tablero.EQUIPOS:
            if not self.tablero.fichasDelEquipo[e]:
                return e

class PruebasTurnos(unittest.TestCase):
    def setUp(self):
        self.gturnos = GestorTurnos()
        self.gturnos.jugadorContraJugador()

    def testInicial(self):
        pass

if __name__ == "__main__":
    unittest.main()
