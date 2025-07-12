# Documentation
## Rules
- Board: 5x5
- Pieces per team: 1 King, 2 Rook, 2 Bishop, 3 Pawn
- Pawn can turn into queen if reach to enemy back row
- White player starts first

## Abilities
Note that we can enable only 1 ability per turn.
- Fog: Opponent only see the player units in movement tiles of the opponents' unit. Last 3 turns.
- Pawn Reset: Reset the pawns to their original position
- Prevent a specific piece from being killed for this turn

## Code
The main places to write code are `setup_phase()` and `play_phase()` inside `/bot/start_code/python/bot.py`

- For setup_phase(), it will be called 5 times for 5 steps.
* Need to look at setupStep of game state to decide which step we are on.
1. Place King
2. Block enemy position
3. Place 2 Rooks (put rook type)
4. Place 2 bishops & 3 pawns (put type)

## JSON Schema
### Game State
```json
{
  "phase": "setup" | "play",
  "playerColor": "white" | "black",
  "board": [
    [ { "type": "K|Q|R|B|P", "color": "white|black" } | null, ... ],
    ... (5 rows) ...
  ],
  "abilitiesRemaining": {
    "fog": true|false,
    "pawnReset": true|false,
    "shield": true|false
  },
  "abilitiesActivated": [
    { "name": "fog|pawnReset|shield", "turnsLeft": <int>, "target": <tuple> | null },
    ...
  ],
  "turnNumber": <int>,
  "setupStep": 1|2|3|4,
  "blockedTiles": [ [row, col], ... ]
}
```

* **`phase`**: `"setup"` for placement, `"play"` for active moves.
* **`playerColor`**: Indicates which side your bot controls this turn.
* **`board`**: 5×5 array; empty squares are `null`.
* **`abilitiesRemaining`**: Flags for one-time-use abilities.
* **`abilitiesActivated`**: Abilities activated against you by your opponent.
* **`turnNumber`**: Sequential turn index (starts at 0 or 1 after setup).
* **`setupStep`**: Placement phase step.
* **`blockedTiles`**: Coordinates unavailable during setup.

## Links
[https://docs.pytorch.org/tutorials/intermediate/reinforcement_q_learning.html](https://docs.pytorch.org/tutorials/intermediate/reinforcement_q_learning.html)
