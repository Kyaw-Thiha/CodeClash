# Bot Design
## Overview
Team Nokemon's 2nd-place winning Chess bot utilizes the following high-level algorithm to aggressively attack opponents:
1. Find available Chess moves
2. Prioritize moves from most to least aggressive
3. Select the most aggressive move

## Deeper Dive
### Piece class
The chess-move identification algorithm utilizes the *Strategy design pattern* based on the Piece superclass.
<br>
**Strategy getAvailableMoves(self, state)**
<br>
returns a list of move tuples (moveValue, targetType) where moveValue is a number encoded to subclass-specific values representing the chess-piece's movement, and targetType is a string indicating what occupies the target-tile (e.g. the piece will move to a tile occupied by a chess piece or unoccupied).

### Move prioritization
Moves are prioritized in the following order (first-to-last):
1. Opponent King attack
2. Oppoent piece attack (not King)
3. No attack

### Selecting a move
Now that the moves have been identified and sorted by priority, the bot now chooses the move with the highest priority.