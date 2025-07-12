# CREATE Chess Game Runner

This guide explains how to run the **Code Clash Chess Game Server** and view the game using the provided **UI viewer**.

---

## Prerequisites

* Two compiled bot executables (one for White, one for Black)
* Your platform's chess server executable (e.g., `chess_server_windows.exe`)
* The UI executable (e.g., `chess_ui_windows.exe`)

---

## 1. Run the Chess Server

The chess server runs the full game between two bots and outputs a JSON log file.

### Usage

```bash
chess_server_<platform> \
  --white-bot path/to/white_bot \
  --black-bot path/to/black_bot \
  --output-log path/to/output.json
```

### Example (Windows)

```bash
chess_server_windows.exe \
  --white-bot bots/my_white_bot.exe \
  --black-bot bots/my_black_bot.exe \
  --output-log match_log.json
```

* `--white-bot`: Path to the bot playing as White
* `--black-bot`: Path to the bot playing as Black
* `--output-log`: File to write the full match log (JSON)

Once complete, you'll have a `match_log.json` containing the game's moves, abilities, and final result.

---

## 2. View the Game Using the UI

The UI lets you load and replay a game stored in a JSON log file.

### Steps:

1. Run the UI executable for your OS (e.g., `chess_ui_windows.exe`)
2. Click the **"Upload Game"** button
3. Select your `match_log.json` file
4. The game board and move history will appear, and you can step through the game visually

---

## Notes

* The server and UI executables are platform-specific (e.g., `windows`, `linux`, `macos`)
* Make sure all executables have the necessary permissions (e.g., make them executable on Linux/macOS using `chmod +x`)
* The bots must conform to the server's invocation protocol (see `Bot Development Guide` in `chess bot` directory)
* You can find the full rules of the game in the `Bot Development Guide` as well.

---

Happy Clashing!