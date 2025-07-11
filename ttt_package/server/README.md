# Code Clash Tic Tac Toe Game Runner

This guide explains how to run the **Tic Tac Toe Game Server** and view the game using the provided **UI viewer**. Two server interfaces are available: a CLI and a GUI.

---

## 1. Run the Tic Tac Toe Server

The server simulates a full game between two bots and outputs a JSON game log.

### Option A: CLI Version

Use the CLI server (`main_cli.py`) to run games from the command line.

#### Usage

```bash
python main_cli.py [--bot-x path/to/bot_x] [--bot-o path/to/bot_o] [--test]
```

#### Options:

* `--bot-x` — Path to the bot playing as X
* `--bot-o` — Path to the bot playing as O
* `--test` — (Optional) Enable test mode:

  * If a bot is missing or makes an invalid move, the server will make a random move instead.
* `--board-size` is optional (default is 10)

#### Example

```bash
python main_cli.py --bot-x my_bots/x.exe --bot-o my_bots/o.exe --test
```

At the end of the match, a file named `ttt_game_output.json` will be created in the current directory containing the full match log.

### Option B: GUI Version

The GUI server provides a tkinter interface to run the match interactively.

#### Steps:

1. Launch the GUI executable (e.g., `ttt_server_gui_windows.exe`)
2. Use the interface to:

   * Browse for Bot X and Bot O executables
   * (Optionally) check the **Test Mode** box
3. Click **Run Game**
4. The match will be played and saved to `ttt_game_output.json`

---

## 2. View the Game Using the UI

Use the viewer UI to visually replay any generated match log.

### Steps:

1. Run the UI executable (e.g., `ttt_viewer_windows.exe`)
2. Click **"Upload Game"**
3. Select `ttt_game_output.json`
4. You will see the game board and can step through each move interactively

---

## Notes

* The board size is fixed at 10×10.
* The win condition is to get 5 in a row, column, or diagonal.
* You can use either the CLI or GUI server interchangeably, both produce the same `ttt_game_output.json` format.
* Make sure your bot executables are valid and follow the `Tic Tac Toe Bot Development Guide`.
* If a bot fails and test mode is **not** enabled, the match will terminate with an error.

---

Happy coding and good luck!