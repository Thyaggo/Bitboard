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
    
    def _bitscan_forward(self, bitboard):
        """Encuentra el índice del bit más bajo en el bitboard"""
        return np.int64(np.log2(bitboard & -bitboard))
            
        

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

class Bishop(Piece):
    """Clase para alfiles"""
    
    def generate_moves(self, from_square, occupied, enemy):
        """Genera los movimientos del alfil"""
        
        m = Constants.NUM_COLS
        longitud = Constants.NUM_SQUARES
        
        _, col = divmod(from_square, m)
        
        # Modificar la diagonal principal (↘) moviéndonos en pasos de (m+1)
        diag_pos = from_square + (m + 1)
        while diag_pos < longitud and diag_pos % m >= col:
            valor |= (1 << diag_pos)
            diag_pos += m + 1

        # Modificar la diagonal principal (↘) hacia atrás
        diag_pos = from_square - (m + 1)
        while diag_pos >= 0 and diag_pos % m <= col:
            valor |= (1 << diag_pos)
            diag_pos -= m + 1

        # Modificar la diagonal secundaria (↙) moviéndonos en pasos de (m-1)
        diag_pos = from_square + (m - 1)
        while diag_pos < longitud and diag_pos % m <= col:
            valor |= (1 << diag_pos)
            diag_pos += m - 1

        # Modificar la diagonal secundaria (↙) hacia atrás
        diag_pos = from_square - (m - 1)
        while diag_pos >= 0 and diag_pos % m >= col:
            valor |= (1 << diag_pos)
            diag_pos -= m - 1
        

            
if __name__ == "__main__":
    """Función de prueba"""
    
    def printbit(bitboard):
        """Imprime el tablero con las piezas"""
        bits = np.binary_repr(bitboard, width=64)  # Invertimos el orden de los bits
        for fila in range(8):  # Recorremos de arriba hacia abajo
            print(" ".join(bits[(fila) * 8:(fila + 1) * 8]))  # Dividimos en filas de 8
    
    
    # Bishop
    bishop = Bishop("white", 0x0000000000000020)
    print("Alfil blanco en e4")
    printbit(bishop.bitboard)
    print("\n\n")
    moves, capture = bishop.generate_moves(36, 0x0000000000000000, 0x0000000000000000)
    print("Movimientos")
    printbit(moves)
    print("\n\n")
    print("Capturas")
    printbit(capture)