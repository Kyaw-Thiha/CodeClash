# Bot Development Guide – Code Clash Chess Server Compatibility

This document provides detailed instructions for participants to create chess bots compatible with the Code Clash Club Chess Game Server CLI. Follow each section to ensure your bot will interoperate correctly with the server.

---

## 1. Bot Invocation

* **Execution:** The server will call your bot as follows:

  ```bash
  /path/to/your_bot /path/to/game_dir/state.json
  ```

* **Argument:** Single positional argument:

    * `state.json` file path containing the current game state.

* **Working Directory:** Assume current working directory is `game_dir`. Your bot reads `state.json` and writes `move.json` in the same directory.

* **Time Limit:** 5 seconds wall-clock per turn. Exceeding this will be treated as a timeout.

* **Exit Codes:**

    * `0` — Successful move (valid JSON and legal move).
    * `1` — Malformed or invalid JSON input.
    * `2` — Legal JSON but illegal move/ability usage.
    * `3` — Internal error (e.g., uncaught exception).

---

## 2. JSON Schemas

### 2.1 `state.json`

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

### 2.2 `move.json`

After computing its move, your bot must write **exactly** one UTF-8 encoded file named `move.json` in the same directory:

```json
{
  "move": {
    "from": [<row>, <col>],
    "to":   [<row>, <col>]
  },
  "ability": {
    "name": "fog" | "pawnReset" | "shield",
    "target": [<row>,<col>] | null
  }
}
```

* **`move`**: Required.

    * For **setup** actions, use `to` to specify the square you want to place your piece and use `from` for specifying the piece type in stage 4 for placing remaining pieces. (You can find the piece type section 4)
* **`ability`**: Optional. When unused, set `"name": null, "target": null` or omit entire `ability` object.

---

## 3. Setup Phase Behavior

In `phase: "setup"`, your bot must follow `setupStep`:

| `setupStep` | Action                                                              |
| ----------- | ------------------------------------------------------------------- |
| 1           | Place King: select one empty square in your back two rows.          |
| 2           | Block Opponent Tile: choose one square in opponent's back two rows. |
| 3           | Place 2 Rooks: select two distinct valid squares.                   |
| 4           | Place Remaining: place 2 Bishops and 3 Pawns in any order.          |

* **Coordinate System:** 0-based `[row, col]`, rows top-to-bottom (0–4), cols left-to-right (0–4).
* **Row Constraints:** White places in rows `0` and `1`; Black in rows `3` and `4`.
* **Blocked Tiles:** Provided by `blockedTiles`; you must not place or move there.

**Examples `move.json` for setup:**

Step 1 (Place King):
```json
{
  "move": {
    "from": [0, 0],  // Piece type: King (Or leave out)
    "to": [0, 2]     // Place King at (0, 2)
  }
}
```

Step 2 (Block Opponent Tile):
```json
{
  "move": {
    "to": [4, 2]     // Block opponent tile at (4, 2)
  }
}
```

Step 3 (Place Rooks):
```json
{
  "move": {
    "from": [0, 2],  // Piece type: Rook (Or leave out)
    "to": [0, 0]     // Place first Rook at (0, 0)
  }
}
```

Step 4 (Place Bishops and Pawns):
```json
{
  "move": {
    "from": [0, 2],  // Piece type: Bishop
    "to": [0, 1]     // Place first Bishop at (0, 1)
  }
}
```

---

## 4. Pieces and Their Types

| Piece Name                     | Symbol on Board | Type for setup phase             |
|--------------------------------|-----------------|----------------------------------|
| King (Only 1)                  | K               | [0, 0] (Not needed to specify)   |
| Queen (Not placed but reached) | Q               | [0, 1] (Not needed to specify)   |
| Rook (Only 2)                  | R               | [0, 2] (Not needed to specify)   |
| Bishop (Only 2)                | B               | [0, 3] (Specify in setup step 4) |
| Pawn (Only 3)                  | P               | [0, 4] (Specify in setup step 4) |

## 5. Play Phase Behavior

In `phase: "play"`, each turn your bot receives `state.json` with current board and ability info.

1. **Parse** `state.json` fully before decision logic.
2. **Choose a move** under standard chess rules, adapted to 5×5:

    * King: one square any direction
    * Rook: straight lines
    * Bishop: diagonal
    * Pawn: one square forward (no two-square nor en passant)
    * Promotion to Queen upon reaching enemy back row
3. **Optionally** activate one available ability:

    * **Fog**: no `target` needed
    * **Pawn Reset**: no `target` needed
    * **Shield**: `target` = coordinates of piece to shield
4. **Write `move.json`** before time limit.
5. **Exit** with exit code `0` if valid, `1` for JSON error, `2` for move error.

---

## 6. Abilities Reference

| Ability    | Usage Limit | Effect                                                                                                                                                      | `ability.target` |
| ---------- | ----------- |-------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|
| Fog        | 1 use       | Opponent sees only attackable tiles for 3 of the opponent’s turns. Normally, empty tiles are `null`. During Fog, all non-visible tiles are marked with `{"color": "fog", "type": "F"}`. | null             |
| Pawn Reset | 1 use       | Attempts to return all pawns to their original starting positions, if those positions are unoccupied.                                                       | null             |
| Shield     | 1 use       | Prevents the specified piece from being captured during the opponent's next turn.                                                                           | `[row,col]`      |

* Abilities may only be activated if `abilitiesRemaining[ability]` is `true`
* After use, the server decrements its usage count and logs it in `abilitiesActivated`.

---

## 7. General Rules

* **Board**: 5×5 squares, significantly smaller than traditional 8×8 chess.

* **Win Condition**: Capture the opposing king (not checkmate). Game ends immediately upon king capture.

* **Movement**:
    * All pieces move according to standard chess rules
    * Pawns only move one square forward (no initial two-square move)
    * Pawns promote to Queen upon reaching opponent's back row
    * No castling or en passant allowed
    * The King can move into check (i.e., it may move into a threatened square).

* **Abilities**:
    * Only one ability can be activated in the same turn
    * Each ability (Fog, Shield, Pawn Reset) can only be used once per game
    * For Pawn Reset:
        * Attempts to return all pawns to their starting positions
        * If a starting square is occupied, it is skipped. Pawns are selected at random and placed into unoccupied original positions.
        * If there are fewer free starting squares than pawns on the board, only some pawns will be reset.
    * Abilities take effect immediately when played

* **Turn Structure**:
    * Players alternate turns, starting with White
    * Each turn consists of:
        1. Moving exactly one piece
        2. Optionally activate one available ability

---

## 8. Submission

Please bundle the following into a single ZIP and upload to the CREATE Playground:

1. **Executable**

   * A one-file executable compiled for Ubuntu 24.04.
   * (Tip: You can use a Docker container matching that environment. Ask our mentors if you need help.)

2. **Source Code**

   * All source files required to build your bot.

3. **README**

   * A short `README.md` or `README.txt` that includes:

     * Brief description of your algorithm and overall approach.
     * Build instructions in case the provided executable fails.

4. **Optional Data File**

   * Your bot may create **one** additional file (≤ 10 MB) during play to maintain state across turns.
   * In your README, specify the filename, format, and its purpose.

5. **ZIP Archive**

   * Package all of the above into a single `.zip` file and upload it.


---

Follow this guide step-by-step to build a compliant bot. Good luck and may the best bot win!