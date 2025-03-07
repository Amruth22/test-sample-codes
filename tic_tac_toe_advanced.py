#!/usr/bin/env python3

import random
import time
import os
import json
import datetime
from enum import Enum
import math
import sys

# Try to import colorama for colored text
try:
    from colorama import init, Fore, Back, Style
    COLORS_AVAILABLE = True
    init()  # Initialize colorama
except ImportError:
    COLORS_AVAILABLE = False

# Try to import pygame for sound effects
try:
    import pygame
    SOUND_AVAILABLE = True
    pygame.mixer.init()
    # Load sound effects
    MOVE_SOUND = pygame.mixer.Sound('sounds/move.wav') if os.path.exists('sounds/move.wav') else None
    WIN_SOUND = pygame.mixer.Sound('sounds/win.wav') if os.path.exists('sounds/win.wav') else None
    LOSE_SOUND = pygame.mixer.Sound('sounds/lose.wav') if os.path.exists('sounds/lose.wav') else None
    TIE_SOUND = pygame.mixer.Sound('sounds/tie.wav') if os.path.exists('sounds/tie.wav') else None
except ImportError:
    SOUND_AVAILABLE = False

# Define game difficulty levels
class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    IMPOSSIBLE = "impossible"

# Define game modes
class GameMode(Enum):
    PLAYER_VS_AI = "player_vs_ai"
    PLAYER_VS_PLAYER = "player_vs_player"
    AI_VS_AI = "ai_vs_ai"
    TOURNAMENT = "tournament"

# Define board sizes
class BoardSize(Enum):
    SMALL = 3  # 3x3 board
    MEDIUM = 5  # 5x5 board
    LARGE = 7  # 7x7 board

class TicTacToe:
    def __init__(self, board_size=BoardSize.SMALL, win_length=3):
        self.board_size = board_size.value
        self.win_length = min(win_length, self.board_size)
        # Initialize the board as a grid with empty spaces
        self.board = [' ' for _ in range(self.board_size * self.board_size)]
        self.current_winner = None  # Keep track of winner
        self.last_move = None  # Keep track of last move for highlighting
        self.move_history = []  # Track all moves for undo feature
        self.winning_combo = []  # Store winning positions for highlighting

    def print_board(self):
        """Print the game board in a nice format with colors and highlights"""
        # Clear the screen for better visualization
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Print game title with cool ASCII art
        self._print_title()
        
        # Print the board
        for i in range(self.board_size):
            # Print horizontal separator
            print('  ' + '+---' * self.board_size + '+')
            
            # Print row with cells
            print(f"{i+1} ", end='')
            for j in range(self.board_size):
                index = i * self.board_size + j
                cell = self.board[index]
                
                # Determine cell styling
                if COLORS_AVAILABLE:
                    if index == self.last_move:
                        # Highlight last move
                        cell_str = self._get_colored_cell(cell, highlight=True)
                    elif index in self.winning_combo:
                        # Highlight winning combo
                        cell_str = self._get_winning_cell(cell)
                    else:
                        # Normal cell
                        cell_str = self._get_colored_cell(cell)
                else:
                    cell_str = cell
                
                print(f"| {cell_str} ", end='')
            print('|')
        
        # Print bottom border
        print('  ' + '+---' * self.board_size + '+')
        
        # Print column labels
        print('   ', end='')
        for j in range(self.board_size):
            print(f" {chr(65+j)}  ", end='')
        print()

    def _print_title(self):
        """Print a cool ASCII art title"""
        if COLORS_AVAILABLE:
            title = f"""
{Fore.CYAN}╔════╦╗{Fore.WHITE}        {Fore.YELLOW}╔════╦╗{Fore.WHITE}        {Fore.GREEN}╔════╦╗{Fore.WHITE}        {Fore.MAGENTA}╔═══╗{Fore.WHITE}
{Fore.CYAN}║╔╗╔╗║║{Fore.WHITE}        {Fore.YELLOW}║╔╗╔╗║║{Fore.WHITE}        {Fore.GREEN}║╔╗╔╗║║{Fore.WHITE}        {Fore.MAGENTA}║╔═╗║{Fore.WHITE}
{Fore.CYAN}╚╝║║╚╝║{Fore.WHITE}        {Fore.YELLOW}╚╝║║╚╝║{Fore.WHITE}        {Fore.GREEN}╚╝║║╚╝║{Fore.WHITE}        {Fore.MAGENTA}║║{Fore.WHITE} {Fore.MAGENTA}║║{Fore.WHITE}
{Fore.CYAN}  ║║  ║{Fore.WHITE}╔══╦══╗ {Fore.YELLOW}  ║║  ║{Fore.WHITE}╔══╦══╗ {Fore.GREEN}  ║║  ║{Fore.WHITE}╔══╦══╗ {Fore.MAGENTA}║║{Fore.WHITE} {Fore.MAGENTA}║║{Fore.WHITE}
{Fore.CYAN}  ║║  ║{Fore.WHITE}║╔╗║╔╗║ {Fore.YELLOW}  ║║  ║{Fore.WHITE}║╔╗║╔╗║ {Fore.GREEN}  ║║  ║{Fore.WHITE}║╔╗║╔╗║ {Fore.MAGENTA}║╚═╝║{Fore.WHITE}
{Fore.CYAN}  ╚╝  ╚{Fore.WHITE}╝╚╝║╚╝║ {Fore.YELLOW}  ╚╝  ╚{Fore.WHITE}╝╚╝║╚╝║ {Fore.GREEN}  ╚╝  ╚{Fore.WHITE}╝╚╝║╚╝║ {Fore.MAGENTA}╚═══╝{Fore.WHITE}
{Fore.WHITE}        ╚══╝         ╚══╝         ╚══╝        
{Style.RESET_ALL}"""
        else:
            title = """
 _____  _        _____             _____            
|_   _|(_)  ___ |_   _|__ _  ___  |_   _|___   ___ 
  | |  | | / __|| | | / _` |/ __|   | | / _ \ / _ \\
  | |  | || (__ | | || (_| |\__ \   | || (_) |  __/
  |_|  |_| \___||_| | \__,_||___/   |_| \___/ \___|
                                                   
"""
        print(title)
        
        # Print game info
        print(f"Board Size: {self.board_size}x{self.board_size} | Win Condition: {self.win_length} in a row")
        print()

    def _get_colored_cell(self, cell, highlight=False):
        """Return a colored cell based on X or O"""
        if cell == 'X':
            return f"{Fore.RED}{Style.BRIGHT if highlight else ''}{cell}{Style.RESET_ALL}"
        elif cell == 'O':
            return f"{Fore.BLUE}{Style.BRIGHT if highlight else ''}{cell}{Style.RESET_ALL}"
        else:
            return f"{Fore.WHITE}{cell}{Style.RESET_ALL}"

    def _get_winning_cell(self, cell):
        """Return a highlighted winning cell"""
        if cell == 'X':
            return f"{Fore.RED}{Back.YELLOW}{Style.BRIGHT}{cell}{Style.RESET_ALL}"
        elif cell == 'O':
            return f"{Fore.BLUE}{Back.YELLOW}{Style.BRIGHT}{cell}{Style.RESET_ALL}"
        else:
            return f"{Fore.WHITE}{cell}{Style.RESET_ALL}"

    def print_board_nums(self):
        """Print the board with position references"""
        print("Position Reference:")
        
        # Print column labels
        print('   ', end='')
        for j in range(self.board_size):
            print(f" {chr(65+j)}  ", end='')
        print()
        
        for i in range(self.board_size):
            # Print horizontal separator
            print('  ' + '+---' * self.board_size + '+')
            
            # Print row with position references
            print(f"{i+1} ", end='')
            for j in range(self.board_size):
                index = i * self.board_size + j
                print(f"| {index:2}", end=' ')
            print('|')
        
        # Print bottom border
        print('  ' + '+---' * self.board_size + '+')
        
        # Print coordinate explanation
        print("\nYou can enter moves as:")
        print("1. Position number (0-{})".format(self.board_size * self.board_size - 1))
        print("2. Coordinates (e.g., A1, B2, C3)")
        print()

    def available_moves(self):
        """Returns a list of available moves (indexes of empty spaces)"""
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        """Returns True if there are empty squares on the board"""
        return ' ' in self.board

    def num_empty_squares(self):
        """Returns the number of empty squares on the board"""
        return self.board.count(' ')

    def make_move(self, square, letter):
        """Make a move on the board"""
        # If the move is valid, make the move and check for a winner
        if self.board[square] == ' ':
            self.board[square] = letter
            self.last_move = square
            self.move_history.append((square, letter))
            
            # Play sound effect if available
            if SOUND_AVAILABLE and MOVE_SOUND:
                MOVE_SOUND.play()
            
            # Check if this move results in a win
            winning_combo = self.check_winner(square, letter)
            if winning_combo:
                self.current_winner = letter
                self.winning_combo = winning_combo
                
                # Play win sound if available
                if SOUND_AVAILABLE:
                    if WIN_SOUND:
                        WIN_SOUND.play()
            
            return True
        return False

    def undo_move(self):
        """Undo the last move"""
        if self.move_history:
            last_square, _ = self.move_history.pop()
            self.board[last_square] = ' '
            self.current_winner = None
            self.winning_combo = []
            
            # Update last move to previous move if exists
            if self.move_history:
                self.last_move = self.move_history[-1][0]
            else:
                self.last_move = None
            
            return True
        return False

    def check_winner(self, square, letter):
        """Check if the last move resulted in a win and return winning positions"""
        # Get row and column of the square
        row = square // self.board_size
        col = square % self.board_size
        
        # Check row
        row_indices = [row * self.board_size + i for i in range(self.board_size)]
        row_win = self._check_line(row_indices, letter)
        if row_win:
            return row_win
        
        # Check column
        col_indices = [col + i * self.board_size for i in range(self.board_size)]
        col_win = self._check_line(col_indices, letter)
        if col_win:
            return col_win
        
        # Check diagonals
        # Only need to check if the move is on a diagonal
        
        # Check main diagonal (top-left to bottom-right)
        if row == col:
            diag_indices = [i * self.board_size + i for i in range(self.board_size)]
            diag_win = self._check_line(diag_indices, letter)
            if diag_win:
                return diag_win
        
        # Check other diagonal (top-right to bottom-left)
        if row + col == self.board_size - 1:
            anti_diag_indices = [i * self.board_size + (self.board_size - 1 - i) for i in range(self.board_size)]
            anti_diag_win = self._check_line(anti_diag_indices, letter)
            if anti_diag_win:
                return anti_diag_win
        
        # For larger boards, check for win_length consecutive marks in any direction
        if self.board_size > 3:
            # Check horizontal sequences
            for c in range(col - self.win_length + 1, col + 1):
                if c < 0 or c + self.win_length > self.board_size:
                    continue
                indices = [row * self.board_size + (c + i) for i in range(self.win_length)]
                line_win = self._check_exact_line(indices, letter)
                if line_win:
                    return line_win
            
            # Check vertical sequences
            for r in range(row - self.win_length + 1, row + 1):
                if r < 0 or r + self.win_length > self.board_size:
                    continue
                indices = [(r + i) * self.board_size + col for i in range(self.win_length)]
                line_win = self._check_exact_line(indices, letter)
                if line_win:
                    return line_win
            
            # Check diagonal sequences (top-left to bottom-right)
            for r, c in [(row - i, col - i) for i in range(self.win_length)]:
                if r < 0 or c < 0 or r + self.win_length > self.board_size or c + self.win_length > self.board_size:
                    continue
                indices = [(r + i) * self.board_size + (c + i) for i in range(self.win_length)]
                line_win = self._check_exact_line(indices, letter)
                if line_win:
                    return line_win
            
            # Check diagonal sequences (top-right to bottom-left)
            for r, c in [(row - i, col + i) for i in range(self.win_length)]:
                if r < 0 or c >= self.board_size or r + self.win_length > self.board_size or c - self.win_length + 1 < 0:
                    continue
                indices = [(r + i) * self.board_size + (c - i) for i in range(self.win_length)]
                line_win = self._check_exact_line(indices, letter)
                if line_win:
                    return line_win
        
        # If all checks fail, no winner yet
        return []

    def _check_line(self, indices, letter):
        """Check if there are win_length consecutive marks in the given line"""
        line = [self.board[i] for i in indices]
        
        # Count consecutive occurrences
        count = 0
        winning_indices = []
        
        for i, mark in enumerate(line):
            if mark == letter:
                count += 1
                winning_indices.append(indices[i])
                if count >= self.win_length:
                    return winning_indices[-self.win_length:]
            else:
                count = 0
                winning_indices = []
        
        return []

    def _check_exact_line(self, indices, letter):
        """Check if all positions in the given indices have the same letter"""
        if all(self.board[i] == letter for i in indices):
            return indices
        return []

    def is_board_full(self):
        """Check if the board is full"""
        return ' ' not in self.board


class Player:
    def __init__(self, letter, name=None):
        # letter is X or O
        self.letter = letter
        self.name = name or f"Player {letter}"
        self.wins = 0
        self.losses = 0
        self.ties = 0

    def get_move(self, game):
        """Get the player's move"""
        pass

    def update_stats(self, result):
        """Update player statistics"""
        if result == self.letter:  # Win
            self.wins += 1
        elif result is None:  # Tie
            self.ties += 1
        else:  # Loss
            self.losses += 1

    def get_stats(self):
        """Get player statistics"""
        total_games = self.wins + self.losses + self.ties
        win_rate = (self.wins / total_games * 100) if total_games > 0 else 0
        return {
            "name": self.name,
            "wins": self.wins,
            "losses": self.losses,
            "ties": self.ties,
            "total_games": total_games,
            "win_rate": win_rate
        }


class HumanPlayer(Player):
    def __init__(self, letter, name=None):
        super().__init__(letter, name or f"Human {letter}")

    def get_move(self, game):
        """Get a valid move from the human player"""
        valid_square = False
        val = None
        
        while not valid_square:
            # Show prompt with player's letter
            if COLORS_AVAILABLE:
                color = Fore.RED if self.letter == 'X' else Fore.BLUE
                prompt = f"{color}{self.name}'s turn ({self.letter}){Style.RESET_ALL}. Enter move: "
            else:
                prompt = f"{self.name}'s turn ({self.letter}). Enter move: "
            
            square_input = input(prompt)
            
            # Check for special commands
            if square_input.lower() == 'quit' or square_input.lower() == 'exit':
                print("Thanks for playing!")
                sys.exit()
            elif square_input.lower() == 'undo':
                if game.undo_move():
                    game.print_board()
                    continue
                else:
                    print("Cannot undo any further!")
                    continue
            elif square_input.lower() == 'help':
                self._show_help()
                game.print_board_nums()
                continue
            
            # Try to parse as coordinate (e.g., A1, B2)
            if len(square_input) == 2 and square_input[0].isalpha() and square_input[1].isdigit():
                try:
                    col = ord(square_input[0].upper()) - ord('A')
                    row = int(square_input[1]) - 1
                    
                    if 0 <= row < game.board_size and 0 <= col < game.board_size:
                        val = row * game.board_size + col
                        if val in game.available_moves():
                            valid_square = True
                        else:
                            print("That position is already taken. Try again.")
                    else:
                        print(f"Invalid coordinates. Must be between A1 and {chr(64 + game.board_size)}{game.board_size}.")
                except ValueError:
                    print("Invalid input. Try again.")
            else:
                # Try to parse as position number
                try:
                    val = int(square_input)
                    if val not in game.available_moves():
                        raise ValueError
                    valid_square = True
                except ValueError:
                    print(f"Invalid square. Enter a number between 0 and {game.board_size * game.board_size - 1}, or coordinates like A1.")
        
        return val

    def _show_help(self):
        """Show help information"""
        print("\n=== HELP ===")
        print("Enter your move in one of these formats:")
        print("1. Position number (0-8 for 3x3 board)")
        print("2. Coordinates (e.g., A1 for top-left, B2 for center)")
        print("\nSpecial commands:")
        print("- 'undo': Undo the last move")
        print("- 'quit' or 'exit': Exit the game")
        print("- 'help': Show this help message")
        print("============\n")
        input("Press Enter to continue...")


class AIPlayer(Player):
    def __init__(self, letter, difficulty=Difficulty.MEDIUM, name=None):
        super().__init__(letter, name or f"AI {letter} ({difficulty.value})")
        self.difficulty = difficulty
        # Set the opponent's letter
        self.opponent_letter = 'O' if letter == 'X' else 'X'
        # Add thinking delay for more natural gameplay
        self.min_thinking_time = 0.5
        self.max_thinking_time = 2.0

    def get_move(self, game):
        """Get the AI's move based on difficulty level"""
        # Simulate "thinking" with a delay
        thinking_time = self._get_thinking_time()
        print(f"{self.name} is thinking", end="", flush=True)
        for _ in range(3):
            time.sleep(thinking_time / 3)
            print(".", end="", flush=True)
        print()
        
        if self.difficulty == Difficulty.EASY:
            # Easy AI makes random moves with occasional mistakes
            return self._get_easy_move(game)
        
        elif self.difficulty == Difficulty.MEDIUM:
            # Medium AI checks for winning moves and blocks opponent's winning moves
            return self._get_medium_move(game)
        
        elif self.difficulty == Difficulty.HARD:
            # Hard AI uses minimax but with limited depth
            return self._get_hard_move(game)
        
        elif self.difficulty == Difficulty.IMPOSSIBLE:
            # Impossible AI uses full minimax algorithm for optimal play
            return self.minimax(game, True)['position']
        
        else:
            # Default to random move if difficulty is not recognized
            return self.random_move(game)

    def _get_thinking_time(self):
        """Get a random thinking time based on difficulty"""
        if self.difficulty == Difficulty.EASY:
            return random.uniform(self.min_thinking_time, self.min_thinking_time + 0.5)
        elif self.difficulty == Difficulty.MEDIUM:
            return random.uniform(self.min_thinking_time, self.min_thinking_time + 1.0)
        else:
            return random.uniform(self.min_thinking_time, self.max_thinking_time)

    def _get_easy_move(self, game):
        """Easy AI strategy - mostly random with occasional good moves"""
        # 20% chance to make a good move
        if random.random() < 0.2:
            return self._get_medium_move(game)
        else:
            return self.random_move(game)

    def _get_medium_move(self, game):
        """Medium AI strategy - checks for wins and blocks"""
        # First check if AI can win in the next move
        for move in game.available_moves():
            # Try the move
            game.board[move] = self.letter
            if game.check_winner(move, self.letter):
                game.board[move] = ' '  # Undo the move
                return move
            game.board[move] = ' '  # Undo the move
        
        # Check if opponent can win in their next move and block them
        for move in game.available_moves():
            game.board[move] = self.opponent_letter
            if game.check_winner(move, self.opponent_letter):
                game.board[move] = ' '  # Undo the move
                return move
            game.board[move] = ' '  # Undo the move
        
        # If center is available, take it (for 3x3 board)
        center = game.board_size * game.board_size // 2
        if game.board_size % 2 == 1 and center in game.available_moves():
            return center
        
        # Take corners if available
        corners = [0, game.board_size-1, 
                  game.board_size*(game.board_size-1), 
                  game.board_size*game.board_size-1]
        available_corners = [c for c in corners if c in game.available_moves()]
        if available_corners:
            return random.choice(available_corners)
        
        # If no strategic move, make a random move
        return self.random_move(game)

    def _get_hard_move(self, game):
        """Hard AI strategy - uses minimax with limited depth"""
        # For larger boards, limit the search depth to make it challenging but not perfect
        if game.board_size > 3:
            max_depth = 3
            return self.minimax_with_depth(game, True, max_depth)['position']
        else:
            # For 3x3 board, use full minimax but occasionally make a mistake
            if random.random() < 0.15:  # 15% chance to make a non-optimal move
                return self._get_medium_move(game)
            else:
                return self.minimax(game, True)['position']

    def random_move(self, game):
        """Make a random move from available moves"""
        return random.choice(game.available_moves())

    def minimax(self, state, is_maximizing):
        """
        Minimax algorithm implementation for optimal AI play
        Returns a dictionary with the best position and score
        """
        # Get opponent letter
        other_player = self.opponent_letter
        
        # Check if the previous move was a winner
        if state.current_winner == other_player:
            # We lose, so return negative score
            return {'position': None, 'score': -1 * (state.num_empty_squares() + 1)}
        elif state.current_winner == self.letter:
            # We win, so return positive score
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            # No more moves, it's a tie
            return {'position': None, 'score': 0}
        
        # Initialize best move
        if is_maximizing:
            # If maximizing, we want to maximize our score
            best = {'position': None, 'score': float('-inf')}
            player_letter = self.letter
        else:
            # If minimizing, we want to minimize opponent's score
            best = {'position': None, 'score': float('inf')}
            player_letter = other_player
        
        # Try all possible moves and evaluate them
        for possible_move in state.available_moves():
            # Make the move
            state.board[possible_move] = player_letter
            
            # Check if this move results in a win
            winning_combo = state.check_winner(possible_move, player_letter)
            if winning_combo:
                state.current_winner = player_letter
            
            # Simulate the game after this move using recursion
            sim_score = self.minimax(state, not is_maximizing)
            
            # Undo the move and reset winner
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move
            
            # Update the best move if needed
            if is_maximizing and sim_score['score'] > best['score']:
                best = sim_score
            elif not is_maximizing and sim_score['score'] < best['score']:
                best = sim_score
        
        return best

    def minimax_with_depth(self, state, is_maximizing, depth):
        """
        Minimax algorithm with depth limit for larger boards
        Returns a dictionary with the best position and score
        """
        # Get opponent letter
        other_player = self.opponent_letter
        
        # Check if the previous move was a winner or we reached max depth
        if state.current_winner == other_player:
            return {'position': None, 'score': -1 * (state.num_empty_squares() + 1)}
        elif state.current_winner == self.letter:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares() or depth == 0:
            # No more moves, it's a tie or we reached max depth
            return {'position': None, 'score': 0}
        
        # Initialize best move
        if is_maximizing:
            best = {'position': None, 'score': float('-inf')}
            player_letter = self.letter
        else:
            best = {'position': None, 'score': float('inf')}
            player_letter = other_player
        
        # Try all possible moves and evaluate them
        for possible_move in state.available_moves():
            # Make the move
            state.board[possible_move] = player_letter
            
            # Check if this move results in a win
            winning_combo = state.check_winner(possible_move, player_letter)
            if winning_combo:
                state.current_winner = player_letter
            
            # Simulate the game after this move using recursion with reduced depth
            sim_score = self.minimax_with_depth(state, not is_maximizing, depth - 1)
            
            # Undo the move and reset winner
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move
            
            # Update the best move if needed
            if is_maximizing and sim_score['score'] > best['score']:
                best = sim_score
            elif not is_maximizing and sim_score['score'] < best['score']:
                best = sim_score
        
        return best


class GameStats:
    def __init__(self):
        self.stats_file = "game_stats.json"
        self.stats = self._load_stats()
    
    def _load_stats(self):
        """Load statistics from file"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self._initialize_stats()
        else:
            return self._initialize_stats()
    
    def _initialize_stats(self):
        """Initialize empty statistics"""
        return {
            "games_played": 0,
            "player_wins": 0,
            "ai_wins": 0,
            "ties": 0,
            "game_history": []
        }
    
    def update_stats(self, winner, player1, player2, board_size, game_mode):
        """Update game statistics"""
        self.stats["games_played"] += 1
        
        # Update win counts
        if winner is None:
            self.stats["ties"] += 1
        elif isinstance(player1, HumanPlayer) and player1.letter == winner:
            self.stats["player_wins"] += 1
        elif isinstance(player2, HumanPlayer) and player2.letter == winner:
            self.stats["player_wins"] += 1
        else:
            self.stats["ai_wins"] += 1
        
        # Add game to history
        game_record = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "winner": "Tie" if winner is None else f"Player {winner}",
            "player1": player1.name,
            "player2": player2.name,
            "board_size": f"{board_size}x{board_size}",
            "game_mode": game_mode
        }
        self.stats["game_history"].append(game_record)
        
        # Save updated stats
        self._save_stats()
    
    def _save_stats(self):
        """Save statistics to file"""
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def display_stats(self):
        """Display game statistics"""
        print("\n===== GAME STATISTICS =====")
        print(f"Total Games Played: {self.stats['games_played']}")
        print(f"Player Wins: {self.stats['player_wins']}")
        print(f"AI Wins: {self.stats['ai_wins']}")
        print(f"Ties: {self.stats['ties']}")
        
        # Calculate win rates
        if self.stats['games_played'] > 0:
            player_win_rate = (self.stats['player_wins'] / self.stats['games_played']) * 100
            ai_win_rate = (self.stats['ai_wins'] / self.stats['games_played']) * 100
            tie_rate = (self.stats['ties'] / self.stats['games_played']) * 100
            
            print(f"\nPlayer Win Rate: {player_win_rate:.1f}%")
            print(f"AI Win Rate: {ai_win_rate:.1f}%")
            print(f"Tie Rate: {tie_rate:.1f}%")
        
        # Show recent games
        if self.stats['game_history']:
            print("\nRecent Games:")
            for game in self.stats['game_history'][-5:]:
                print(f"{game['date']} - {game['player1']} vs {game['player2']} - Winner: {game['winner']} - Board: {game['board_size']}")
        
        print("===========================\n")


def play(game, x_player, o_player, print_game=True, game_stats=None, game_mode=GameMode.PLAYER_VS_AI):
    """Main game loop function"""
    if print_game:
        game.print_board_nums()
        game.print_board()
    
    # Starting letter is X
    letter = 'X'
    
    # Continue playing until there are no empty squares or there's a winner
    while game.empty_squares():
        # Get the move from the appropriate player
        if letter == 'X':
            square = x_player.get_move(game)
        else:
            square = o_player.get_move(game)
        
        # Make the move
        if game.make_move(square, letter):
            if print_game:
                # Convert square to coordinate format for display
                row = square // game.board_size
                col = square % game.board_size
                coord = f"{chr(65 + col)}{row + 1}"
                
                if COLORS_AVAILABLE:
                    color = Fore.RED if letter == 'X' else Fore.BLUE
                    move_msg = f"{color}{letter}{Style.RESET_ALL} moves to {coord} (position {square})"
                else:
                    move_msg = f"{letter} moves to {coord} (position {square})"
                
                print(move_msg)
                game.print_board()
            
            # Check for a winner
            if game.current_winner:
                if print_game:
                    winner_name = x_player.name if letter == 'X' else o_player.name
                    if COLORS_AVAILABLE:
                        color = Fore.RED if letter == 'X' else Fore.BLUE
                        print(f"{color}{winner_name} ({letter}) wins!{Style.RESET_ALL}")
                    else:
                        print(f"{winner_name} ({letter}) wins!")
                
                # Update player stats
                x_player.update_stats(game.current_winner)
                o_player.update_stats(game.current_winner)
                
                # Update game stats if available
                if game_stats:
                    game_stats.update_stats(game.current_winner, x_player, o_player, game.board_size, game_mode.value)
                
                return letter
            
            # Switch players
            letter = 'O' if letter == 'X' else 'X'
    
    # If we get here, it's a tie
    if print_game:
        print("It's a tie!")
        
        # Play tie sound if available
        if SOUND_AVAILABLE and TIE_SOUND:
            TIE_SOUND.play()
    
    # Update player stats
    x_player.update_stats(None)
    o_player.update_stats(None)
    
    # Update game stats if available
    if game_stats:
        game_stats.update_stats(None, x_player, o_player, game.board_size, game_mode.value)
    
    return None


def tournament_mode(players, rounds=3, board_size=BoardSize.SMALL, win_length=3):
    """Run a tournament between multiple players"""
    print("\n===== TOURNAMENT MODE =====")
    print(f"Players: {', '.join(p.name for p in players)}")
    print(f"Rounds: {rounds}")
    print(f"Board Size: {board_size.value}x{board_size.value}")
    print("==========================\n")
    
    # Initialize tournament stats
    tournament_stats = {player.name: {"wins": 0, "losses": 0, "ties": 0, "points": 0} for player in players}
    
    # Play matches between all pairs of players
    for i, player1 in enumerate(players):
        for j, player2 in enumerate(players):
            if i >= j:  # Skip playing against self or duplicate matches
                continue
            
            print(f"\n--- Match: {player1.name} vs {player2.name} ---")
            
            # Play multiple rounds
            for round_num in range(1, rounds + 1):
                print(f"\nRound {round_num}:")
                
                # Create a new game
                game = TicTacToe(board_size, win_length)
                
                # Alternate who goes first in each round
                if round_num % 2 == 1:
                    x_player, o_player = player1, player2
                else:
                    x_player, o_player = player2, player1
                
                # Play the game
                winner = play(game, x_player, o_player, print_game=True, game_mode=GameMode.TOURNAMENT)
                
                # Update tournament stats
                if winner is None:  # Tie
                    tournament_stats[player1.name]["ties"] += 1
                    tournament_stats[player2.name]["ties"] += 1
                    tournament_stats[player1.name]["points"] += 1
                    tournament_stats[player2.name]["points"] += 1
                elif (winner == 'X' and x_player == player1) or (winner == 'O' and o_player == player1):
                    tournament_stats[player1.name]["wins"] += 1
                    tournament_stats[player2.name]["losses"] += 1
                    tournament_stats[player1.name]["points"] += 3
                else:
                    tournament_stats[player2.name]["wins"] += 1
                    tournament_stats[player1.name]["losses"] += 1
                    tournament_stats[player2.name]["points"] += 3
    
    # Display tournament results
    print("\n===== TOURNAMENT RESULTS =====")
    # Sort players by points
    sorted_players = sorted(tournament_stats.items(), key=lambda x: x[1]["points"], reverse=True)
    
    print(f"{'Rank':<5}{'Player':<20}{'Wins':<6}{'Losses':<8}{'Ties':<6}{'Points':<8}")
    print("-" * 50)
    
    for rank, (player_name, stats) in enumerate(sorted_players, 1):
        print(f"{rank:<5}{player_name:<20}{stats['wins']:<6}{stats['losses']:<8}{stats['ties']:<6}{stats['points']:<8}")
    
    print("\nTournament Champion: " + sorted_players[0][0])
    print("==============================\n")


def create_sound_directory():
    """Create directory for sound files if it doesn't exist"""
    if not os.path.exists('sounds'):
        os.makedirs('sounds')
        print("Created 'sounds' directory. You can add sound files there for game effects.")


def main():
    """Main function to run the game"""
    # Initialize colorama if available
    if COLORS_AVAILABLE:
        init()
    
    # Create sounds directory if it doesn't exist
    create_sound_directory()
    
    # Initialize game statistics
    game_stats = GameStats()
    
    # Main game loop
    while True:
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Display welcome message
        if COLORS_AVAILABLE:
            print(f"{Fore.CYAN}{Style.BRIGHT}Welcome to Advanced Tic-Tac-Toe!{Style.RESET_ALL}")
        else:
            print("Welcome to Advanced Tic-Tac-Toe!")
        
        print("\nMAIN MENU:")
        print("1. Player vs AI")
        print("2. Player vs Player")
        print("3. AI vs AI (Demo)")
        print("4. Tournament Mode")
        print("5. View Game Statistics")
        print("6. Quit")
        
        choice = input("\nSelect an option (1-6): ")
        
        if choice == '1':
            # Player vs AI mode
            game_mode = GameMode.PLAYER_VS_AI
            
            # Get player name
            player_name = input("Enter your name (or press Enter for default): ").strip()
            player_name = player_name or "Human Player"
            
            # Select board size
            print("\nSelect board size:")
            print("1. Small (3x3)")
            print("2. Medium (5x5)")
            print("3. Large (7x7)")
            
            board_choice = input("Select board size (1-3): ")
            if board_choice == '2':
                board_size = BoardSize.MEDIUM
                win_length = 4
            elif board_choice == '3':
                board_size = BoardSize.LARGE
                win_length = 5
            else:
                board_size = BoardSize.SMALL
                win_length = 3
            
            # Select AI difficulty
            print("\nSelect AI difficulty:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            print("4. Impossible")
            
            difficulty_choice = input("Select difficulty (1-4): ")
            if difficulty_choice == '1':
                ai_difficulty = Difficulty.EASY
            elif difficulty_choice == '3':
                ai_difficulty = Difficulty.HARD
            elif difficulty_choice == '4':
                ai_difficulty = Difficulty.IMPOSSIBLE
            else:
                ai_difficulty = Difficulty.MEDIUM
            
            # Choose who goes first
            player_letter = input("\nDo you want to be X or O? (X goes first): ").upper()
            
            if player_letter == 'O':
                x_player = AIPlayer('X', ai_difficulty, f"AI (X, {ai_difficulty.value})")
                o_player = HumanPlayer('O', player_name)
            else:
                x_player = HumanPlayer('X', player_name)
                o_player = AIPlayer('O', ai_difficulty, f"AI (O, {ai_difficulty.value})")
            
            # Create a new game and start playing
            game = TicTacToe(board_size, win_length)
            play(game, x_player, o_player, print_game=True, game_stats=game_stats, game_mode=game_mode)
        
        elif choice == '2':
            # Player vs Player mode
            game_mode = GameMode.PLAYER_VS_PLAYER
            
            # Get player names
            player1_name = input("Enter Player 1 (X) name: ").strip() or "Player X"
            player2_name = input("Enter Player 2 (O) name: ").strip() or "Player O"
            
            # Select board size
            print("\nSelect board size:")
            print("1. Small (3x3)")
            print("2. Medium (5x5)")
            print("3. Large (7x7)")
            
            board_choice = input("Select board size (1-3): ")
            if board_choice == '2':
                board_size = BoardSize.MEDIUM
                win_length = 4
            elif board_choice == '3':
                board_size = BoardSize.LARGE
                win_length = 5
            else:
                board_size = BoardSize.SMALL
                win_length = 3
            
            # Create players
            x_player = HumanPlayer('X', player1_name)
            o_player = HumanPlayer('O', player2_name)
            
            # Create a new game and start playing
            game = TicTacToe(board_size, win_length)
            play(game, x_player, o_player, print_game=True, game_stats=game_stats, game_mode=game_mode)
        
        elif choice == '3':
            # AI vs AI demo mode
            game_mode = GameMode.AI_VS_AI
            
            # Select board size
            print("\nSelect board size:")
            print("1. Small (3x3)")
            print("2. Medium (5x5)")
            print("3. Large (7x7)")
            
            board_choice = input("Select board size (1-3): ")
            if board_choice == '2':
                board_size = BoardSize.MEDIUM
                win_length = 4
            elif board_choice == '3':
                board_size = BoardSize.LARGE
                win_length = 5
            else:
                board_size = BoardSize.SMALL
                win_length = 3
            
            # Select AI difficulties
            print("\nSelect AI 1 (X) difficulty:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            print("4. Impossible")
            
            ai1_choice = input("Select difficulty (1-4): ")
            if ai1_choice == '1':
                ai1_difficulty = Difficulty.EASY
            elif ai1_choice == '3':
                ai1_difficulty = Difficulty.HARD
            elif ai1_choice == '4':
                ai1_difficulty = Difficulty.IMPOSSIBLE
            else:
                ai1_difficulty = Difficulty.MEDIUM
            
            print("\nSelect AI 2 (O) difficulty:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            print("4. Impossible")
            
            ai2_choice = input("Select difficulty (1-4): ")
            if ai2_choice == '1':
                ai2_difficulty = Difficulty.EASY
            elif ai2_choice == '3':
                ai2_difficulty = Difficulty.HARD
            elif ai2_choice == '4':
                ai2_difficulty = Difficulty.IMPOSSIBLE
            else:
                ai2_difficulty = Difficulty.MEDIUM
            
            # Create AI players
            x_player = AIPlayer('X', ai1_difficulty, f"AI 1 (X, {ai1_difficulty.value})")
            o_player = AIPlayer('O', ai2_difficulty, f"AI 2 (O, {ai2_difficulty.value})")
            
            # Create a new game and start playing
            game = TicTacToe(board_size, win_length)
            play(game, x_player, o_player, print_game=True, game_stats=game_stats, game_mode=game_mode)
        
        elif choice == '4':
            # Tournament mode
            # Select board size
            print("\nSelect board size:")
            print("1. Small (3x3)")
            print("2. Medium (5x5)")
            print("3. Large (7x7)")
            
            board_choice = input("Select board size (1-3): ")
            if board_choice == '2':
                board_size = BoardSize.MEDIUM
                win_length = 4
            elif board_choice == '3':
                board_size = BoardSize.LARGE
                win_length = 5
            else:
                board_size = BoardSize.SMALL
                win_length = 3
            
            # Set up tournament players
            players = []
            
            # Add human player
            human_name = input("\nEnter your name for the tournament: ").strip() or "Human Player"
            players.append(HumanPlayer('X', human_name))  # Letter doesn't matter for tournament
            
            # Add AI players of different difficulties
            players.append(AIPlayer('O', Difficulty.EASY, "AI Easy"))
            players.append(AIPlayer('O', Difficulty.MEDIUM, "AI Medium"))
            players.append(AIPlayer('O', Difficulty.HARD, "AI Hard"))
            
            # Get number of rounds
            rounds = input("\nEnter number of rounds per match (default: 3): ")
            try:
                rounds = int(rounds)
                if rounds < 1:
                    rounds = 3
            except ValueError:
                rounds = 3
            
            # Run tournament
            tournament_mode(players, rounds, board_size, win_length)
        
        elif choice == '5':
            # View game statistics
            game_stats.display_stats()
            input("Press Enter to return to the main menu...")
        
        elif choice == '6':
            # Quit
            print("Thanks for playing!")
            break
        
        else:
            print("Invalid choice. Please try again.")
        
        # Ask if the player wants to return to the main menu
        if choice in ['1', '2', '3', '4']:
            input("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    main()