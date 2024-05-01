class Board:
    def __init__(self, board):
        self.board = board  # Initialize the Sudoku board

    def __str__(self):
        # Strings for drawing the Sudoku board
        upper_lines = f'\n╔═══{"╤═══"*2}{"╦═══"}{"╤═══"*2}{"╦═══"}{"╤═══"*2}╗\n'
        middle_lines = f'╟───{"┼───"*2}{"╫───"}{"┼───"*2}{"╫───"}{"┼───"*2}╢\n'
        lower_lines = f'╚═══{"╧═══"*2}{"╩═══"}{"╧═══"*2}{"╩═══"}{"╧═══"*2}╝\n'
        board_string = upper_lines

        # Iterate through each row and column of the board to construct the string representation
        for index, line in enumerate(self.board):
            row_list = []
            # Divide each row into 3 parts (sub-squares)
            for square_no, part in enumerate([line[:3], line[3:6], line[6:]], start=1):
                row_square = '|'.join(str(item) for item in part)  # Join the sub-square elements with '|'
                row_list.extend(row_square)
                if square_no != 3:
                    row_list.append('║')  # Add vertical separators between sub-squares

            row = f'║ {" ".join(row_list)} ║\n'  # Join the sub-squares of a row with ' ' and add horizontal separators
            row_empty = row.replace('0', ' ')  # Replace '0' with ' ' to represent empty cells
            board_string += row_empty

            # Add appropriate horizontal separators after each row
            if index < 8:
                if index % 3 == 2:
                    board_string += f'╠═══{"╪═══"*2}{"╬═══"}{"╪═══"*2}{"╬═══"}{"╪═══"*2}╣\n'
                else:
                    board_string += middle_lines
            else:
                board_string += lower_lines  # Add the lower border for the board

        return board_string

    def find_empty_cell(self):
        # Find the first empty cell in the board
        for row, contents in enumerate(self.board):
            try:
                col = contents.index(0)
                return row, col  # Return the row and column indices of the empty cell
            except ValueError:
                pass
        return None  # Return None if no empty cell is found

    def valid_in_row(self, row, num):
        # Check if 'num' is valid in the given row
        return num not in self.board[row]  # Return True if 'num' is not present in the row

    def valid_in_col(self, col, num):
        # Check if 'num' is valid in the given column
        return all(
            self.board[row][col] != num
            for row in range(9)
        )  # Return True if 'num' is not present in the column

    def valid_in_square(self, row, col, num):
        # Check if 'num' is valid in the 3x3 square containing the cell at (row, col)
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
        for row_no in range(row_start, row_start + 3):
            for col_no in range(col_start, col_start + 3):
                if self.board[row_no][col_no] == num:
                    return False  # Return False if 'num' is already present in the square
        return True  # Return True if 'num' is not present in the square

    def is_valid(self, empty, num):
        # Check if placing 'num' in the empty cell at 'empty' is valid
        row, col = empty
        valid_in_row = self.valid_in_row(row, num)
        valid_in_col = self.valid_in_col(col, num)
        valid_in_square = self.valid_in_square(row, col, num)
        return all([valid_in_row, valid_in_col, valid_in_square])  # Return True if 'num' is valid in all aspects

    def solver(self):
        # Recursive function to solve the Sudoku puzzle
        if (next_empty := self.find_empty_cell()) is None:
            return True  # Return True if there are no empty cells (base case)
        else:
            for guess in range(1, 10):
                if self.is_valid(next_empty, guess):
                    row, col = next_empty
                    self.board[row][col] = guess  # Place the valid guess in the empty cell
                    if self.solver():  # Recur to solve the remaining puzzle
                        return True  # Return True if the puzzle is solved
                    self.board[row][col] = 0  # Backtrack if the current guess doesn't lead to a solution

        return False  # Return False if no valid guess leads to a solution


def solve_sudoku(board):
    # Function to solve the Sudoku puzzle
    gameboard = Board(board)  # Create a Board object with the given puzzle
    print(f'\nPuzzle to solve:\n{gameboard}')  # Print the initial state of the puzzle
    if gameboard.solver():  # Attempt to solve the puzzle
        print('\nSolved puzzle:')
        print(gameboard)  # Print the solved puzzle
    else:
        print('\nThe provided puzzle is unsolvable.')  # Print a message if the puzzle is unsolvable
    return gameboard


# Example Sudoku puzzle
puzzle = [
  [0, 0, 2, 0, 0, 8, 0, 0, 0],
  [0, 0, 0, 0, 0, 3, 7, 6, 2],
  [4, 3, 0, 0, 0, 0, 8, 0, 0],
  [0, 5, 0, 0, 3, 0, 0, 9, 0],
  [0, 4, 0, 0, 0, 0, 0, 2, 6],
  [0, 0, 0, 4, 6, 7, 0, 0, 0],
  [0, 8, 6, 7, 0, 4, 0, 0, 0],
  [0, 0, 0, 5, 1, 9, 0, 0, 8],
  [1, 7, 0, 0, 0, 6, 0, 0, 5]
]

solve_sudoku(puzzle)  # Solve the example Sudoku puzzle
