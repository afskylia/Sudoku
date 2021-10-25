from SudokuBoard import *


def main():
    #sudoku = SudokuBoard(difficulty=Difficulty.ADVANCED)
    # generate_boards_json(num=1,difficulty=Difficulty.BEGINNER)
    grid, original = load_board_json(Difficulty.ADVANCED)
    sudoku = SudokuBoard(grid, original, Difficulty.ADVANCED)
    print(sudoku)


if __name__ == "__main__":
    main()
