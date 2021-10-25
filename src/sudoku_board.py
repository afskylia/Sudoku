import csv
from copy import deepcopy
import json
from enum import Enum
from random import randint, shuffle
import pandas as pd
import numpy as np


class Difficulty(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4


class SudokuBoard:
    def __init__(self, grid=None, original=None, difficulty=Difficulty.INTERMEDIATE):
        self.difficulty = difficulty

        if grid is None:
            grid = np.zeros((9, 9))
            self.generate_solution(grid)
            self.grid = grid
            self.original = deepcopy(self.grid)
            self.remove_numbers_from_grid()
        else:
            self.grid = np.array(grid)
            self.original = np.array(original)

    def generate_solution(self, grid):
        number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for i in range(0, 81):
            row = i//9
            col = i % 9

            # Find next empty cell
            if grid[row][col] == 0:
                shuffle(number_list)
                for n in number_list:
                    if self.valid_location(row, col, n, grid):
                        grid[row][col] = n
                        if not self.find_empty_square(grid):
                            return True
                        if self.generate_solution(grid):
                            return True
                break

        grid[row][col] = 0
        return False

    def solve_puzzle(self, grid):
        grid = self.grid if grid is None else grid

        for i in range(0, 81):
            row = i//9
            col = i % 9

            # Find next empty cell
            if grid[row][col] == 0:
                for n in range(1, 10):
                    if self.valid_location(row, col, n, grid):
                        grid[row][col] = n
                        if not self.find_empty_square(grid):
                            self.counter += 1
                            return True
                        if self.solve_puzzle(grid):
                            return True
                break

        grid[row][col] = 0
        return False

    def remove_numbers_from_grid(self):
        min_count = 0

        if self.difficulty == Difficulty.BEGINNER:
            min_count = 65
        elif self.difficulty == Difficulty.INTERMEDIATE:
            min_count = 49
        elif self.difficulty == Difficulty.ADVANCED:
            min_count = 33
        elif self.difficulty == Difficulty.EXPERT:
            min_count = 20

        min_count += randint(0, 10)

        non_empty_squares = self.get_non_empty_squares(self.grid)
        count = len(non_empty_squares)
        rounds = 3

        while rounds > 0 and count >= min_count:
            row, col = non_empty_squares.pop()
            count -= 1
            removed_square = self.grid[row][col]
            self.grid[row][col] = 0
            grid_copy = deepcopy(self.grid)
            self.counter = 0
            self.solve_puzzle(grid_copy)

            if self.counter != 1:
                self.grid[row][col] = removed_square
                count += 1
                rounds -= 1

    def valid_location(self, row, col, n, grid=None):
        grid = self.grid if grid is None else grid

        if self.count_num_row(row, n, grid) > 0:
            return False
        elif self.count_num_col(col, n, grid) > 0:
            return False
        elif self.count_num_square(row//3, col//3, n, grid) > 0:
            return False
        return True

    def get_non_empty_squares(self, grid=None):
        grid = self.grid if grid is None else grid
        non_empty_squares = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] != 0:
                    non_empty_squares.append((i, j))
        shuffle(non_empty_squares)
        return non_empty_squares

    def find_empty_square(self, grid=None):
        grid = self.grid if grid is None else grid

        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return

    def is_solved(self):
        comparison = self.grid == self.original
        return comparison.all()

    def validate(self, grid=None):
        grid = self.grid if grid is None else grid

        # Check rows and columns
        for i in range(9):
            for n in range(1, 10):
                if self.count_num_row(i, n, grid) != 1:
                    print("Row {}, n={}".format(i, n))
                    return False
                if self.count_num_col(i, n, grid) != 1:
                    print("Column {}, n={}".format(i, n))
                    return False

        # Check squares
        for x in range(3):
            for y in range(3):
                for n in range(1, 10):
                    if self.count_num_square(x, y, n, grid) != 1:
                        print("Square ({},{}), n={}".format(x, y, n))
                        return False

        # Sudoku is valid
        return True

    def update(self, x, y, n):
        self.grid[x][y] = n

    def remove(self, x, y):
        self.grid[x][y] = 0

    def count_num_row(self, row, n, grid=None):
        grid = self.grid if grid is None else grid
        return (self.get_row(row, grid) == n).sum()

    def count_num_col(self, col, n, grid=None):
        grid = self.grid if grid is None else grid
        return (self.get_column(col, grid) == n).sum()

    def count_num_square(self, row, col, n, grid=None):
        grid = self.grid if grid is None else grid
        return (self.get_square(row, col, grid) == n).sum()

    def get_row(self, x, grid=None):
        grid = self.grid if grid is None else grid
        return grid[x, :]

    def get_column(self, y, grid=None):
        grid = self.grid if grid is None else grid
        return grid[:, y]

    def get_square(self, x, y, grid=None):
        grid = self.grid if grid is None else grid
        return grid[x*3:x*3+3, y*3:y*3+3].flatten()

    def __getitem__(self, item):
        return self.grid[item]

    def __str__(self):
        grid_str = np.empty((9, 9), dtype=str)
        for i in range(9):
            for j in range(9):
                val = self.grid[i][j]
                val_str = "."
                if val != 0:
                    val_str = str(val)
                grid_str[i][j] = val_str

        return '\n'.join(['  '.join([str(cell) for cell in row]) for row in grid_str])


def generate_boards_json(num=1, difficulty=Difficulty.INTERMEDIATE):
    boards = []
    for _ in range(num):
        board = SudokuBoard(grid=None, difficulty=difficulty)
        print(board)
        grid_json = json.dumps(board.grid.tolist())
        original_json = json.dumps(board.original.tolist())
        # json_string = '{"grid":"' + grid_json + '","original":"' + original_json + '"}'
        obj = {"grid": grid_json, "original": original_json}
        boards.append(obj)

    filename = "grids/{}.json".format(difficulty.name)
    with open(filename) as json_file:
        data = json.load(json_file)
        temp = data['boards']
        for board in boards:
            temp.append(board)

    with open(filename, 'w') as file:
        json.dump(data, file)


def load_board_json(difficulty=Difficulty.INTERMEDIATE):
    filename = "grids/{}.json".format(difficulty.name)
    with open(filename) as json_file:
        data = json.load(json_file)
        i = randint(0, len(data['boards'])-1)
        board_json = data['boards'][i]
        grid = json.loads(board_json['grid'])
        original = json.loads(board_json['grid'])
        return grid, original
