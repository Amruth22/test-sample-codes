# Advanced Tic-Tac-Toe with AI

A super cool, feature-rich implementation of the classic Tic-Tac-Toe game with advanced AI opponents, multiple game modes, and exciting features!

![Tic-Tac-Toe Game](https://raw.githubusercontent.com/Amruth22/test-sample-codes/advanced-features/screenshots/game_preview.png)

## 🎮 Features

### Game Modes
- **Player vs AI**: Test your skills against AI opponents of varying difficulty
- **Player vs Player**: Challenge your friends in local multiplayer
- **AI vs AI Demo**: Watch AI opponents battle it out
- **Tournament Mode**: Compete in a tournament against multiple AI opponents

### Board Options
- **Multiple Board Sizes**: Choose from 3x3, 5x5, or 7x7 boards
- **Customizable Win Conditions**: Adjust how many marks in a row are needed to win

### AI Difficulty Levels
- **Easy**: Makes mostly random moves with occasional good plays
- **Medium**: Plays strategically, blocks your winning moves
- **Hard**: Uses limited-depth minimax algorithm for challenging gameplay
- **Impossible**: Uses full minimax algorithm for optimal play

### Visual Enhancements
- **Colored Text**: Visually distinguish X and O players (requires colorama)
- **Highlighted Moves**: Last move and winning combinations are highlighted
- **ASCII Art**: Cool game title and visual elements
- **Coordinate System**: Enter moves using coordinates (e.g., A1, B2) or position numbers

### Gameplay Features
- **Undo Moves**: Made a mistake? Undo your last move!
- **Game Statistics**: Track your performance over time
- **Move History**: Review the sequence of moves in the current game
- **Help System**: Built-in help command for new players

### Sound Effects (Optional)
- Move sounds
- Win/lose/tie sounds
- (Requires pygame and sound files in the 'sounds' directory)

## 🚀 Installation

1. Clone this repository:
   ```
   git clone https://github.com/Amruth22/test-sample-codes.git
   cd test-sample-codes
   ```

2. Install optional dependencies for enhanced experience:
   ```
   pip install colorama pygame
   ```

3. Run the game:
   ```
   python tic_tac_toe_advanced.py
   ```

## 📋 How to Play

1. From the main menu, select your desired game mode
2. Configure game settings (board size, difficulty, etc.)
3. Make moves by entering:
   - Position number (0-8 for 3x3 board)
   - Coordinates (e.g., A1 for top-left, B2 for center)

### Special Commands
- `undo`: Undo the last move
- `help`: Display help information
- `quit` or `exit`: Exit the game

## 🎯 Game Rules

- Players take turns placing their mark (X or O) on the board
- The first player to get a specified number of marks in a row (horizontally, vertically, or diagonally) wins
- If the board fills up with no winner, the game is a tie

## 🏆 Tournament Mode

Test your skills in Tournament Mode:
1. Compete against multiple AI opponents
2. Play multiple rounds against each opponent
3. Earn points (3 for a win, 1 for a tie)
4. See final rankings and determine the tournament champion

## 📊 Statistics Tracking

The game keeps track of:
- Total games played
- Win/loss/tie records
- Win rates
- Game history

## 🎵 Adding Sound Effects

To enable sound effects:
1. Install pygame: `pip install pygame`
2. Create a 'sounds' directory in the game folder
3. Add the following sound files:
   - move.wav - played when a move is made
   - win.wav - played when a player wins
   - lose.wav - played when a player loses
   - tie.wav - played when the game ends in a tie

## 🛠️ Requirements

- Python 3.6 or higher
- Optional: colorama (for colored text)
- Optional: pygame (for sound effects)

## 🤝 Contributing

Contributions are welcome! Feel free to submit pull requests or open issues to improve the game.

## 📝 License

This project is open source and available under the MIT License.

---

Enjoy the game! 🎮