import GestorTurnos

def intro():
    return "---------\n| DAMAS |\n---------"

if __name__ == "__main__":
    print(intro())
    input("Pulsa intro para comenzar\n")
    
    gestor = GestorTurnos.GestorTurnos()
    print(gestor)
