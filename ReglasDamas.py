def posicionValida(x, y, longTablero):
    EH = False
    if x < 0 or x >= longTablero:
        return EH
    if y < 0 or y >= longTablero:
        return EH
    if (x + y) % 2 != 0:
        return EH

    return True
