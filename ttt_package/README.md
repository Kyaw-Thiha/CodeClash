# Documentation 
- We are playing on 10x10 board.
- We win if we have 5 consecutive on row, column or diagonal.

## GUI
To run the game, 
- in Linux, go into `server`, and run
```bash
./ttt_server_linux
```
- in Windows, go into `server`, and run
```bash
./ttt_server_windows
```

## CLI
- in Linux, go into `server`, and run
```bash
./ttt_server_linux_cli
```

- in Windows, go into `server`, and run
```bash
./ttt_server_windows
```

## Main Place to Code
- Edit the code in `bot/starter_code/python/bot.py` inside the `choose_move()` function
- The bot.py must output (row, col) as output. That is the only requirement.


## Simon Strategies
- Check if you have 4 in a row not blocked, if so, extend it
- Check if enemy have 4 in a row not blocked, block 1 side
- Check if you have 3 in a row, if so extend it
- Check if enemy have 3 in a row with both sides not blocked, block 1 side
- Check if you have any 2 in a row or 1 extendable, if so, extend it.

## Functions to implement
- Function check connected rows
- Function check connected cols
- Function check connected diagonals
- Function that checks of lines of n length for self
- Function that checks of lines of n length for enemy

## Data Type
### Position
- Tuple of (row, col)
### Line
- Number of pieces on the line (int)
- Number of sides blocked (int)
- Array of positions [size of array have to be number of pieces of the line]
### Connection
- Returned from functions finding connected row/col/diagonal
- Key of no. of connection
- Value of Array of [[Lines]]
