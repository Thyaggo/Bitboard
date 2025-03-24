import numpy as np
from typing import Callable
import random

def mask_bishop_attacks(square : int, edge: bool =False, bitscan: bool =False, ray: list =["northwest", "northeast", "southwest", "southeast"]):
    # Inicializa o bitboard de ataques
    edges = 0 if not edge else 1
    
    northwest, northeast, southwest, southeast = np.uint64(0), np.uint64(0), np.uint64(0), np.uint64(0)

    # Calcula a linha (rank) e coluna (file) do quadrado
    tr = square // 8
    tf = square % 8

    # Máscara para as diagonais superiores (direita e esquerda)
    if "northwest" in ray:
        r, f = tr + 1, tf + 1
        while r <= 6 + edges and f <= 6 + edges:
            northwest |= (np.uint64(1) << np.uint64(r * 8 + f))
            r += 1
            f += 1

    if "northeast" in ray:
        r, f = tr + 1, tf - 1
        while r <= 6 + edges and f >= 1 - edges:
            northeast |= (np.uint64(1) << np.uint64(r * 8 + f))
            r += 1
            f -= 1

    # Máscara para as diagonais inferiores (direita e esquerda)
    if "southwest" in ray:
        r, f = tr - 1, tf + 1
        while r >= 1 - edges and f <= 6 + edges:
            southwest |= (np.uint64(1) << np.uint64(r * 8 + f))
            r -= 1
        f += 1

    if "southeast" in ray:
        r, f = tr - 1, tf - 1
        while r >= 1 - edges and f >= 1 - edges:
            southeast |= (np.uint64(1) << np.uint64(r * 8 + f))
            r -= 1
            f -= 1

    # Retorna o mapa de ataques
    if bitscan:
        return {
            "northwest" : northwest,
            "northeast" : northeast,
            "southwest" : southwest,
            "southeast" : southeast
        }
    else:
        return northwest | northeast | southwest | southeast

def mask_rook_attacks(square, edge: bool=False, bitscan: bool =False, ray: list =["north", "south", "west", "east"]):
    # Inicializa o bitboard de ataques
    edges = 0 if not edge else 1
    
    north, south, east, west = np.uint64(0), np.uint64(0), np.uint64(0), np.uint64(0)

    # Calcula a linha (rank) e coluna (file) do quadrado
    tr = square // 8
    tf = square % 8
    
    if "south" in ray:
    # Máscara para as linhas e colunas
        for r in range(tr + 1, 7 + edges):
            south |= (np.uint64(1) << np.uint64(r * 8 + tf))

    if "north" in ray:
        for r in range(tr - 1, 0 - edges, -1):
            north |= (np.uint64(1) << np.uint64(r * 8 + tf))

    if "west" in ray:
        for f in range(tf + 1, 7 + edges):
            west |= (np.uint64(1) << np.uint64(tr * 8 + f))

    if "east" in ray:
        for f in range(tf - 1, 0 - edges, -1):
            east |= (np.uint64(1) << np.uint64(tr * 8 + f))

    # Retorna o mapa de ataques
    if bitscan:
        return {
            "north" : north,
            "south" : south,
            "east" : east,
            "west" : west
        }
    else:
        return north | south | east | west

def mask_queen_attacks(square, edge=False, bitscan=False , ray= ["north", "south", "west", "east", "northwest", "northeast", "southwest", "southeast"]):
    """Genera la máscara de ataques de la reina."""
    if bitscan:
        rook_attacks = mask_rook_attacks(square, edge, bitscan, ray)
        bishop_attacks = mask_bishop_attacks(square, edge, bitscan, ray)
        return {**rook_attacks, **bishop_attacks}  # Merge dictionaries
    else:
        return mask_rook_attacks(square, edge, bitscan, ray) | mask_bishop_attacks(square, edge, bitscan, ray)

def count_bits(bitboard):
    """Conta o número de bits ativos no bitboard."""
    count = 0
    while bitboard:
        count += 1
        bitboard &= bitboard - 1
    return count

def get_ls1b_index(bitboard):
    """Obtiene el índice del bit menos significativo activo (LSB)."""
    return count_bits((bitboard & -bitboard) - 1)

def get_ms1b_index(bitboard):
    """Obtiene el índice del bit más significativo activo (MSB)."""
    if bitboard == 0:
        return None
    
    position = 0
    while bitboard > 0:
        bitboard >>= np.uint64(1)
        position += 1
        
    return position - 1

def set_bit(bitboard, square):
    """Activa el bit en la posición 'square'."""
    return bitboard | np.uint64((1 << square))

def pop_bit(bitboard, square):
    """Desactiva el bit en la posición 'square'."""
    return bitboard & ~np.uint64((1 << square))

def set_occupancy(index, bits_in_mask, attack_mask):
    """Genera el mapa de ocupación basado en el índice y la máscara de ataque."""
    occupancy = np.uint64(0)

    for count in range(bits_in_mask):
        # Obtener el índice del bit menos significativo activo
        square = get_ls1b_index(attack_mask)

        # Desactivar el bit en la máscara de ataque
        attack_mask = pop_bit(attack_mask, square)

        # Verificar si el bit en la posición 'count' de 'index' está activo
        if index & (1 << count):
            # Activar el bit correspondiente en el mapa de ocupación
            occupancy |= (np.uint64(1) << np.uint64(square))
            
    return occupancy

def valid_moves(occupancy: np.uint64, square: int, piece_mask_func: Callable):
    """Genera los movimientos válidos para una pieza en 'square'."""
    # Máscara de ataque
    attacks = piece_mask_func(square, edge=True, bitscan=True)
    
    valid_move = np.uint64(0)
        
    for direction, ray in attacks.items():
        # Máscara de ataque
        blokers = ray & occupancy
        
        # The first blocker, if any, is the least significant one-bit of the intersection
        if blokers:
            if direction in ["south", "east", "southeast", "southwest"]:
                first_blocker = get_ms1b_index(blokers)
            else:
                first_blocker = get_ls1b_index(blokers)
            # Only if the blocker is not the last square
            valid = ray ^ piece_mask_func(first_blocker, edge=True, bitscan=True, ray=[direction])[direction]
            valid_move |= valid
        else:
            valid_move |= ray
            
    # Movimientos válidos
    return valid_move

def find_magic_index(occupancy, magic):
    """Encuentra el índice mágico."""
    attemps = 10000
    for _ in range(attemps):
        magic_number = np.uint64(random.getrandbits(64) & random.getrandbits(64) & random.getrandbits(64))
        
    return False

if "__main__" == __name__:
    
    def print_bitboard(board):
        for rank in range(8):
            row = ""
            for file in range(8):
                square = rank * 8 + file
                row += "1 " if (board & (np.uint64(1) << np.uint64(square))) else ". "
            print(row)
        print("\n")
    
    mask = mask_rook_attacks(28, edge=True)
    blocker = mask & np.uint64(0b1010101010101010101010101010101010101010101010101010101010101010)
    print_bitboard(blocker)
    print_bitboard(valid_moves(blocker, 28, mask_rook_attacks))