def get_legal_moves(board, position, piece):
    r, c = position
    moves = []

    def on_board(x, y):
        return 0 <= x < 5 and 0 <= y < 5

    directions = {
        "R": [(1, 0), (-1, 0), (0, 1), (0, -1)],
        "B": [(1, 1), (-1, -1), (1, -1), (-1, 1)],
        "Q": [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)],
        "K": [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)],
        "P": [(1, 0)] if piece.color == "white" else [(-1, 0)],
    }

    for dr, dc in directions[piece.type]:
        for step in range(1, 2 if piece.type in ["K", "P"] else 5):
            nr, nc = r + dr * step, c + dc * step
            if not on_board(nr, nc):
                break
            target = board[nr][nc]
            if target is None:
                moves.append((nr, nc))
            else:
                if target.color != piece.color:
                    moves.append((nr, nc))
                break
    return moves


# Skills
def use_fog(state):
    if state.abilities_remaining["fog"]:
        state.abilities_remaining["fog"] = False
        state.abilities_activated.append(
            {"name": "fog", "turnsLeft": 3, "target": None}
        )


def use_pawn_reset(state):
    if state.abilities_remaining["pawnReset"]:
        state.abilities_remaining["pawnReset"] = False
        for r in range(5):
            for c in range(5):
                p = state.board[r][c]
                if p and p.type == "P" and p.color == state.turn:
                    # Reset to stored initial position
                    for init_r, init_c in state.pawn_initial_positions[state.turn]:
                        if state.board[init_r][init_c] is None:
                            state.board[init_r][init_c] = p
                            state.board[r][c] = None
                            break


def use_shield(state, target):
    if state.abilities_remaining["shield"]:
        r, c = target
        piece = state.board[r][c]
        if piece and piece.color == state.turn:
            state.abilities_remaining["shield"] = False
            piece.shielded = True
            state.abilities_activated.append(
                {"name": "shield", "turnsLeft": 1, "target": (r, c)}
            )
