import numpy as np

from src.pieces import Pawn, Knight

class ChessBoard:
    """Clase para representar el tablero con bitboards"""
    
    def __init__(self):
        self.white_pieces = {
            "pawns_white": Pawn("white", 65280),  # Peones blancos en fila 2
            "knights_white": Knight("white", 0x4200000000000000),  # Caballos blancos en b1 y g1
        }
        
        self.black_pieces = {
            "pawns_black": Pawn("black", 71776119061217280),  # Peones negros en fila 7
            "knights_black": Knight("black", 0x0000000000000042),  # Caballos negros en b8 y g8
        }
        
        self.pieces = self.black_pieces | self.white_pieces
        
        self.occupied = self.compute_occupied()

    def compute_occupied(self, color = None):
        """Actualiza el bitboard de casillas ocupadas para un color"""
        if color == "white":
            return sum(piece.bitboard for piece in self.white_pieces.values())
        elif color == "black":
            return sum(piece.bitboard for piece in self.black_pieces.values())
        else:
            return sum(piece.bitboard for piece in self.pieces.values())
        
    def move_piece(self, from_square, to_square, piece_name: str = None):
        """Mueve una pieza en el tablero"""
        if piece_name not in self.pieces:
            raise ValueError("Pieza no encontrada o nombre de pieza inválido")
        
        if piece_name[-5:] == "white":
            self.white_pieces[piece_name].move(from_square, to_square)
        elif piece_name[-5:] == "black":
            self.black_pieces[piece_name].move(from_square, to_square)
        else:
            ValueError("Nombre de pieza inválido")
        
            
            
board = ChessBoard()

# Mover un peón blanco de e2 (posición 12) a e4 (posición 28)
board.move_piece(12, 20, "pawns_white")

# Mostrar el bitboard después del movimiento
print(f"Pawns White: {board.pieces['pawns_white'].bitboard:064b}")
