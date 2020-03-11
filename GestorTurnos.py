import ValoresPorDefecto as vpd
import Tablero
import unittest

class GestorTurnos():
    def __init__(self, longTablero=vpd.LONG_TABLERO, equipos=vpd.EQUIPOS):
        self.NUM_EQUIPOS = len(equipos)
        self.tablero = Tablero.Tablero(longTablero, equipos)
        self.tablero.colocaFichasIniciales()

        self.turno = 0
        self.ronda = 0

        self.equipoActual = None
        self.actualizaContadores()


    def actualizaContadores(self):
        iteradorEquipoActual = self.turno % self.NUM_EQUIPOS
        self.equipoActual = self.tablero.EQUIPOS[iteradorEquipoActual]

        if iteradorEquipoActual == 0:
            self.ronda = int(self.turno / self.NUM_EQUIPOS)

    def moverFicha(self, xFicha, yFicha, xObjetivo, yObjetivo):
        for secuencia in self.tablero.movimientosFicha(xFicha, yFicha):
            for coordenada in secuencia:
                pass

        pass

    def turno(self, xFicha, yFicha, xObjetivo, yObjetivo):
        #Comprueba de quien es el turno
        #Haz un movimiento (comer o desplazarse)

        #Comprueba si alguna ficha del equipo esta en posicion de dama
            #Si es asi, actualiza esa ficha
        #Termina el turno modificando variables
        self.turno += 1
        self.actualizaContadores()

    def __str__(self):
        string = "Turno del equipo " + self.equipoActual + "\n"
        string += self.tablero.__str__() + "\n"
        return string

class PruebasTurnos(unittest.TestCase):
    def setUp(self):
        self.gturnos = GestorTurnos()

    def testInicial(self):
        pass

if __name__ == "__main__":
    unittest.main()
