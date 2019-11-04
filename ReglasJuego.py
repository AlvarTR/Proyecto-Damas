class ReglasJuego():
    def __init__(self, longTablero=8, relacionFichasCasillas=0.4):
        if relacionFichasCasillas < 0.5:
            self.LONG_TABLERO = longTablero
            self.FILAS_PEONES = int(self.LONG_TABLERO * relacionFichasCasillas)

    def enPosicion(self, x, y):
        if x >= 0 and x < self.LONG_TABLERO:
            if y >= 0 and y < self.LONG_TABLERO:
                if (x + y) % 2 == 0:
                    return True
        return False
