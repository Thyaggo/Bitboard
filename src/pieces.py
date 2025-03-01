from abc import ABC, abstractmethod
from constants import Constants
import numpy as np

class Piece(ABC):
    """Clase base para todas las piezas de ajedrez"""
    
    def __init__(self, color, bitboard):
        self.color = color  # "white" o "black"
        self.bitboard = bitboard  # Representación en bitboard
        

    @abstractmethod
    def generate_moves(self, occupied):
        """Genera los movimientos posibles de la pieza"""
        pass

    def move(self, from_square, to_square):
        """Realiza un movimiento en el bitboard"""
        mask_from = 1 << from_square
        mask_to = 1 << to_square
        
        if self.bitboard & mask_from:  # Verifica si la pieza está en 'from_square'
            self.bitboard &= ~mask_from  # Apaga la casilla de origen
            self.bitboard |= mask_to  # Enciende la casilla destino
            
        

class Pawn(Piece):
    """Clase para peones"""
    
    def generate_moves(self, from_square, occupied, enemy):
        """Genera los movimientos del peón"""
        #Set Bitboard
        square = 1 << from_square
        
        if self.color == "white":
            if square & Constants.RANK2:
                # Movimiento doble desde la segunda fila
                moves = square << 16 | square << 8
            else:
                # Movimiento simple
                moves = square << 8
            # Capturas
            capture_left = square << 7
            capture_right = square << 9
        else:
            if square & Constants.RANK7:
                # Movimiento doble desde la séptima fila
                moves = square >> 16 | square >> 8
            else:
                # Movimiento simple
                moves = square >> 8
            # Capturas
            capture_left = square >> 9
            capture_right = square >> 7
        # Generar movimientos
        
        # Filtrar movimientos ocupados
        moves &= ~occupied
        # Filtrar movimientos de captura
        capture_left &= enemy
        capture_right &= enemy
        # Combinar movimientos
        capures = capture_left | capture_right
        return moves, capures
    
        
class Knight(Piece):
    """Clase para caballos"""
    
    def generate_moves(self, from_square, occupied, enemy):
        """Genera los movimientos del caballo"""
        
        square = 1 << from_square
        
        # Movimientos posibles del caballo
        moves = (square << 17) if (square & ~Constants.FILE_A) & (square & ~(Constants.RANK8 | Constants.RANK7)) else 0
        moves |= (square << 15) if (square & ~Constants.FILE_H) & (square & ~(Constants.RANK8 | Constants.RANK7)) else 0
        moves |= (square << 6) if (square & ~(Constants.FILE_G | Constants.FILE_H)) & (square & ~(Constants.RANK8)) else 0
        moves |= (square << 10) if (square & ~(Constants.FILE_A | Constants.FILE_B)) & (square & ~(Constants.RANK8)) else 0
        moves |= (square >> 17) if (square & ~Constants.FILE_H) & (square & ~(Constants.RANK1 | Constants.RANK2)) else 0
        moves |= (square >> 15) if (square & ~Constants.FILE_A) & (square & ~(Constants.RANK1 | Constants.RANK2)) else 0
        moves |= (square >> 6) if (square & ~(Constants.FILE_A | Constants.FILE_B)) & (square & ~(Constants.RANK1)) else 0
        moves |= (square >> 10) if (square & ~(Constants.FILE_G | Constants.FILE_H)) & (square & ~(Constants.RANK1)) else 0
        
        # Filtrar movimientos ocupados
        moves &= ~occupied
        # Filtrar movimientos de captura
        capture = moves & enemy
            
        return moves, capture

            
if __name__ == "__main__":
    """Función de prueba"""
    
    def printbit(bitboard):
        """Imprime el tablero con las piezas"""
        bits = np.binary_repr(bitboard, width=64)  # Invertimos el orden de los bits
        for fila in range(8):  # Recorremos de arriba hacia abajo
            print(" ".join(bits[(fila) * 8:(fila + 1) * 8]))  # Dividimos en filas de 8
    
    
    # Caball0 blanco en b1 a g1
    knight = Knight("white", 1 << 56)
    printbit(knight.bitboard)
    print("\n\n")
    
    moves, caputes = knight.generate_moves(56, 0, 0)
    print("Movimientos posibles del caballo:")
    printbit(moves)
    print("\n\n")
    print("Capturas posibles del caballo:")
    printbit(caputes)
    print("\n\n")
    
    if (1 << 6) & moves:
        print("El caballo puede moverse a la posición 6")
        knight.move(56, 6)
        printbit(knight.bitboard)
    else:
        print("El caballo no puede moverse a la posición 6")
        printbit(knight.bitboard)