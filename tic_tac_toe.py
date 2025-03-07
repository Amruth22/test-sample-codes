#!/usr/bin/env python3

import random
import time
import os

class TicTacToe:
    def __init__(self):
        # Initialize the board as a 3x3 grid with empty spaces
        self.board = [' ' for _ in range(9)]
        self.current_winner = None  # Keep track of winner

    def print_board(self):
        """Print the game board in a nice format"""
        # Clear the screen for better visualization
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print('TIC-TAC-TOE')
        print('------------')
        
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
        
        print('------------')

    def print_board_nums(self):
        """Print the board with position numbers for reference"""
        # Board with numbers 0-8 to show players which number corresponds to which position
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        
        print('Position reference:')
        print('------------')
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')
        print('------------')

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
            
            # Check if this move results in a win
            if self.winner(square, letter):
                self.current_winner = letter
            
            return True
        return False

    def winner(self, square, letter):
        """Check if the last move resulted in a win"""
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        
        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        
        # Check diagonals
        # Only need to check if the move is on a diagonal
        if square % 2 == 0:
            # Check main diagonal (top-left to bottom-right)
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            
            # Check other diagonal (top-right to bottom-left)
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        
        # If all checks fail, no winner yet
        return False


class Player:
    def __init__(self, letter):
        # letter is X or O
        self.letter = letter

    def get_move(self, game):
        """Get the player's move"""
        pass


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        """Get a valid move from the human player"""
        valid_square = False
        val = None
        
        while not valid_square:
            square = input(f"{self.letter}'s turn. Input move (0-8): ")
            
            # Check if the input is valid
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print("Invalid square. Try again.")
        
        return val


class AIPlayer(Player):
    def __init__(self, letter, difficulty='medium'):
        super().__init__(letter)
        self.difficulty = difficulty
        # Set the opponent's letter
        self.opponent_letter = 'O' if letter == 'X' else 'X'

    def get_move(self, game):
        """Get the AI's move based on difficulty level"""
        if self.difficulty == 'easy':
            # Easy AI just makes random moves
            return self.random_move(game)
        
        elif self.difficulty == 'medium':
            # Medium AI checks for winning moves and blocks opponent's winning moves
            # Otherwise makes a random move
            
            # First check if AI can win in the next move
            for move in game.available_moves():
                # Try the move
                game.board[move] = self.letter
                if game.winner(move, self.letter):
                    game.board[move] = ' '  # Undo the move
                    return move
                game.board[move] = ' '  # Undo the move
            
            # Check if opponent can win in their next move and block them
            for move in game.available_moves():
                game.board[move] = self.opponent_letter
                if game.winner(move, self.opponent_letter):
                    game.board[move] = ' '  # Undo the move
                    return move
                game.board[move] = ' '  # Undo the move
            
            # If no winning moves, make a random move
            return self.random_move(game)
        
        elif self.difficulty == 'hard':
            # Hard AI uses minimax algorithm for optimal play
            return self.minimax(game, True)['position']
        
        else:
            # Default to random move if difficulty is not recognized
            return self.random_move(game)

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
            if state.winner(possible_move, player_letter):
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


def play(game, x_player, o_player, print_game=True):
    """Main game loop function"""
    if print_game:
        game.print_board_nums()
    
    # Starting letter is X
    letter = 'X'
    
    # Continue playing until there are no empty squares or there's a winner
    while game.empty_squares():
        # Get the move from the appropriate player
        if letter == 'X':
            square = x_player.get_move(game)
        else:
            square = o_player.get_move(game)
            # Add a small delay for AI moves to make the game more readable
            time.sleep(0.8)
        
        # Make the move
        if game.make_move(square, letter):
            if print_game:
                print(f"{letter} makes a move to square {square}")
                game.print_board()
                print('')
            
            # Check for a winner
            if game.current_winner:
                if print_game:
                    print(f"{letter} wins!")
                return letter
            
            # Switch players
            letter = 'O' if letter == 'X' else 'X'
    
    # If we get here, it's a tie
    if print_game:
        print("It's a tie!")
    return None


def main():
    """Main function to run the game"""
    print("Welcome to Tic-Tac-Toe!")
    
    while True:
        # Game setup
        game_mode = input("Select game mode:\n1. Player vs AI\n2. Player vs Player\n> ")
        
        if game_mode == '1':
            # Player vs AI mode
            difficulty = input("Select AI difficulty:\n1. Easy\n2. Medium\n3. Hard\n> ")
            
            if difficulty == '1':
                ai_difficulty = 'easy'
            elif difficulty == '3':
                ai_difficulty = 'hard'
            else:
                ai_difficulty = 'medium'
            
            player_letter = input("Do you want to be X or O? (X goes first): ").upper()
            
            if player_letter == 'X':
                x_player = HumanPlayer('X')
                o_player = AIPlayer('O', ai_difficulty)
            else:
                x_player = AIPlayer('X', ai_difficulty)
                o_player = HumanPlayer('O')
        
        elif game_mode == '2':
            # Player vs Player mode
            x_player = HumanPlayer('X')
            o_player = HumanPlayer('O')
        
        else:
            print("Invalid choice. Please try again.")
            continue
        
        # Create a new game and start playing
        game = TicTacToe()
        play(game, x_player, o_player, print_game=True)
        
        # Ask if the player wants to play again
        play_again = input("Play again? (y/n): ").lower()
        if play_again != 'y':
            break
    
    print("Thanks for playing!")


if __name__ == "__main__":
    main()