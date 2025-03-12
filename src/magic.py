
def mask_bishop_attacks(square):
    # Inicializa o bitboard de ataques
    attacks = 0

    # Calcula a linha (rank) e coluna (file) do quadrado
    tr = square // 8
    tf = square % 8

    # Máscara para as diagonais superiores (direita e esquerda)
    r, f = tr + 1, tf + 1
    while r <= 6 and f <= 6:
        attacks |= (1 << (r * 8 + f))
        r += 1
        f += 1

    r, f = tr + 1, tf - 1
    while r <= 6 and f >= 1:
        attacks |= (1 << (r * 8 + f))
        r += 1
        f -= 1

    # Máscara para as diagonais inferiores (direita e esquerda)
    r, f = tr - 1, tf + 1
    while r >= 1 and f <= 6:
        attacks |= (1 << (r * 8 + f))
        r -= 1
        f += 1

    r, f = tr - 1, tf - 1
    while r >= 1 and f >= 1:
        attacks |= (1 << (r * 8 + f))
        r -= 1
        f -= 1

    # Retorna o mapa de ataques
    return attacks

def mask_rook_attacks(square):
    # Inicializa o bitboard de ataques
    attacks = 0

    # Calcula a linha (rank) e coluna (file) do quadrado
    tr = square // 8
    tf = square % 8

    # Máscara para as linhas e colunas
    for r in range(tr + 1, 7):
        attacks |= (1 << (r * 8 + tf))

    for r in range(tr - 1, 0, -1):
        attacks |= (1 << (r * 8 + tf))

    for f in range(tf + 1, 7):
        attacks |= (1 << (tr * 8 + f))

    for f in range(tf - 1, 0, -1):
        attacks |= (1 << (tr * 8 + f))

    # Retorna o mapa de ataques
    return attacks

def mask_queen_attacks(square):
    return mask_bishop_attacks(square) | mask_rook_attacks(square)

def rook_valid_moves(square):
    # Inicializa o bitboard de movimentos
 ...