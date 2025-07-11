# Bot Development Guide – Tic Tac Toe Server Compatibility

This document provides detailed instructions for participants to Code Clash Tic Tac Toe bots compatible with the Code Clash Game Server. Follow each section carefully to ensure your bot can compete properly.

---

## 1. Bot Invocation

* **Execution:** The server will call your bot as follows:

  ```bash
  /path/to/your_bot /path/to/state.json
  ```

* **Argument:** Single positional argument:

  * `state.json` file path containing the current game state.

* **Working Directory:** Assume current working directory is where `state.json` is located. Your bot must read this file and write the output to **standard output**.

* **Time Limit:** 5 seconds wall-clock per run. Exceeding this will be treated as a timeout.

* **Exit Codes:**

  * `0` — Successful move (valid JSON, legal move, no crash)
  * Non-zero — Treated as disqualification

---

## 2. JSON Schemas

### 2.1 `state.json`

```json
{
  "board": [
    ["X", "", "O", "", "", ..., ""],
    ... (10 rows total) ...
  ],
  "player": "X"
}
```

* **`board`**: 10×10 2D array of strings. Values are either "X", "O", or an empty string `""`.
* **`player`**: A string, either "X" or "O", indicating which player the bot is controlling.

### 2.2 Expected Output

Your bot must print exactly one line to `stdout`, formatted as a JSON array:

```json
[row, col]
```

* Coordinates must be **zero-based integers**.
* For example, a valid output would be:

```json
[1, 2]
```

---

## 3. Move Validity

* The move must be to an empty cell.
* The row and column must be valid integers from `0` to `9`.
* Any invalid move results in **immediate disqualification**.

---

## 4. Executable Requirements

* Your bot must be a **single file executable** that can be launched via the command line.
* It must accept one argument (the path to `state.json`) and print a valid move to standard output.

---

## 5. Execution Constraints

* Your bot must:

  * Finish within 5 seconds
  * Exit with code `0`
  * Not crash or produce errors

---

## 6. Output Format and Cleanliness

* **Only output the `[row, col]` JSON array to stdout**.
* Do not print anything else to stdout.
* If you need to log or debug, use `stderr` instead.

---

## 7. Platform and Language

* Bots may be written in any language that compiles to a single file and meets the interface requirements.

---

## 8. Game Rules

* **Board Size:** The board is 10×10 squares.
* **Win Condition:** The first player to get **five in a row**, **five in a column**, or **five diagonally** (either direction) wins.

---

## 9. Submission

Please bundle the following into a single ZIP and upload to the CREATE Playground:

1. **Executable**

   * A one-file executable compiled for Ubuntu 24.04.
   * (Tip: You can use a Docker container matching that environment—ask our mentors if you need help.)

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

Follow this guide step-by-step to build a compliant bot. Good luck and may the smartest player win!