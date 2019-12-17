def enPosicion(x, y, longTablero):
    if x >= 0 and x < longTablero:
        if y >= 0 and y < longTablero:
            if (x + y) % 2 == 0:
                return True
    return False
