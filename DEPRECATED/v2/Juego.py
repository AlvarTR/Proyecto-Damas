from Tablero import *

class Juego():
    def __init__(self, tablero):
        self.tablero = None
        if isinstance(tablero, Tablero):
            self.tablero = tablero

    
