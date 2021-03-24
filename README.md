# Crossword Designer

This designer uses the Forward Checking, Least Constrained Value, and Degree Heuristics to provide solutions for a given crossword board.

[Python 3](https://www.python.org/downloads/) along with the [csv](https://docs.python.org/3/library/csv.html), [operator](https://docs.python.org/3/library/operator.html) and [copy](https://docs.python.org/3/library/copy.html) packages are required to run this program.

## Running the solver:
The solver requires exactly 3 arguments;

- `puzzleLayoutFile`: csv file that contains crossword puzzle layout. Samples provided ([task1Puzzle.csv](./task1Puzzle.csv), [task2Puzzle.csv](./task2Puzzle.csv), [task2Puzzle2.csv](./task2Puzzle2.csv)).
	- `#`: represents a block (black square) in the board
	- `-`: represents a blank cell in the board
	- `num`: a number that represents the starting points for words
- `wordList`: text file with a list of words to be used in the puzzle (one word per line). Samples provided ([task1Words.txt](./task1Words.txt), [words.txt](./words.txt))
- `heuristic`: heuristic algorithm(s) to use. Heuristic options include:
	- `fc`: Forward Checking
	- `lcv`: Least Constraining Value
	- `dh`: Degree Heuristic
	- `fc,lcv` or `lcv,fc`: Forward Checking with Least Constraining Value
	- `fc,dh` or `dh,fc`: Forward Checking with Degree Heuristic

### Usage

```shell
$ python3 designCrossword.py puzzleLayoutFile wordList hueristic
```
### Example:
```shell
$ python3 designCrossword.py puzzle.csv words.txt fc
```