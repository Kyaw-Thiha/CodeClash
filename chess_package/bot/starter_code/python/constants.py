"""
Constants that both the server and the bots will use in Code Clash Special Chess Game.
"""

# Piece types at setup phase (bots will use these to place pieces)
PIECE_TYPES_SETUP = {
    "K": [0, 0], # King
    "Q": [0, 1], # Queen
    "R": [0, 2], # Rook
    "B": [0, 3], # Bishop
    "P": [0, 4], # Pawn
}

# Fog constant (If a tile is invisible from your view, the following piece will be there)
FOG_PIECE = {"color": "fog", "type": "F"}