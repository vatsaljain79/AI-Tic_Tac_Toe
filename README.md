# Tic Tac Toe Game

A fun and interactive **Tic Tac Toe** game made with Python and Pygame. Play against the computer at varying difficulty levels, listen to soothing background music, and enjoy sound effects for clicks and wins.

## Features

- **Three Difficulty Levels**: Easy, Medium, and Hard, using the Minimax algorithm.
- **Sound Effects**: Background music, click sounds, and win sounds enhance the gameplay.
- **Dynamic UI**: Restart options and win/draw counters.
- **CSV Integration**: The game learns from previous games and can make smarter decisions over time by storing board states and best moves in a CSV file.

## How to Play

1. **Run the Game**:
    - Ensure you have Python and Pygame installed on your system.
    - Run the `tic_tac_toe.py` script.

2. **Select Difficulty**:
    - You will be prompted to select the difficulty level: Easy, Medium, or Hard.

3. **Gameplay**:
    - Player 'X' goes first.
    - Click on an empty cell to place your 'X' and compete against the computer's 'O'.
    - The game ends when either player wins or the board is full (draw).

4. **Restart**:
    - After a game ends, the restart screen will appear, showing the number of wins for both the player and the computer, as well as the number of draws. 
    - You can restart or change the difficulty at any time.

## Game Rules

- The game is played on a 3x3 grid.
- Player 'X' and Computer 'O' take turns marking their cells.
- The goal is to be the first to get three marks in a row (horizontally, vertically, or diagonally).

## Files

- `calm_music.mp3`: Background music played during the game.
- `tch.wav`: Click sound for selecting a cell.
- `win.wav`: Sound played when a player wins.
- `state.csv`: Stores board states and optimal moves for learning and future reference.

## Installation

1. **Install Pygame**:
    ```bash
    pip install pygame
    ```
2. **Run the Game**:
    ```bash
    python tic_tac_toe.py
    ```

## Future Enhancements

- Implement additional themes for different visual experiences.
- Add multiplayer functionality to compete against a friend.

## Credits

- Code created by **Vatsal Jain**.
