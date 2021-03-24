#!/usr/bin/python3
import sys
import csv
import copy
from operator import itemgetter
import time


BLOCK = '#'
BLANK = '-'

class cell():
	def __init__(self, val=BLANK):
		self.val = val
		self.across = -1
		self.down = -1
		self.letter = ''

class puzzle():
	def __init__(self, crossword=[], wordDict={}, fc=False):
		if len(crossword) > 0:
			self.crossword = crossword
			self.cells = []
			self.rows = len(crossword)
			self.columns = len(crossword[0])
			self.wordDict = wordDict
			self.moves = []
			self.fc = fc


	def printPuzzle(self):
		print('******************************************')
		for i in range(self.rows):
			for j in range(self.columns):
				if(self.cells[i][j].val == BLOCK):
					print(BLOCK, end='\t')
				elif(self.cells[i][j].letter == '' and self.cells[i][j].val == BLANK):
					print(BLANK, end='\t')
				elif(self.cells[i][j].letter == '' and self.cells[i][j].val.isdigit()):
					print(self.cells[i][j].val, end='\t')
				else:
					print(self.cells[i][j].letter, end='\t')
			print('\n')
		print('\n')


	def generateTableMap(self):
		self.cells = []
		constraintAcross = []
		constraintDown = []
		for r in range(self.rows):
			row = []
			for c in range(self.columns):
				curCell = cell(self.crossword[r][c])
				if(curCell.val.isdigit()):
					across, constA = self.getAcross(r, c)
					constraintAcross = constraintAcross + constA
					if across in self.wordDict and curCell.val not in constraintAcross:
						curCell.across = across
						constraints = self.getIntersectionsForAcross(r, c)
						self.moves.append((curCell, across, 'A', constraints))

					down, constD = self.getDown(r, c)
					constraintDown = constraintDown + constD
					if down in self.wordDict and curCell.val not in constraintDown:
						curCell.down = down
						constraints = self.getIntersectionsForDown(r, c)
						self.moves.append((curCell, down, 'D', constraints))
				elif curCell.val.isalpha():
					curCell.letter = curCell.val.upper()

				row.append(curCell)
			self.cells.append(row)


	def getAcross(self, r, c):
		count = 0
		constraint = []
		for i in range(c, self.columns):
			cell = self.crossword[r][i]
			if cell == BLANK or cell.isdigit():
				count += 1
				if cell.isdigit() and i != c:
					constraint.append(cell)
			else:
				break
		return count, constraint

	def getIntersectionsForAcross(self, r, c):
		intersectionCounter = 0
		for i in range(c, self.columns):
			for row in range(r, -1, -1):
				if self.crossword[row][i] == BLOCK:
					break
				elif self.crossword[row][i].isdigit():
					intersectionCounter += 1
					break
		return intersectionCounter


	def getDown(self, r, c):
		count = 0
		constraint = []
		for i in range(r, self.rows):
			cell = self.crossword[i][c]
			if cell == BLANK or cell.isdigit():
				count += 1
				if cell.isdigit() and i != r:
					constraint.append(cell)
			else:
				break
		return count, constraint

	def getIntersectionsForDown(self, r, c):
		intersectionCounter = 0
		for i in range(r, self.rows):
			for col in range(c, -1, -1):
				if self.crossword[i][col] == BLOCK:
					break
				elif self.crossword[i][col].isdigit():
					intersectionCounter += 1
					break
		return intersectionCounter


	def solve(self, words, moves):
		if self.checkGoal():
			return True

		for move in moves:
			for word in words[move[1]]:
				temp = copy.deepcopy(self)
				if self.addWord(move, word, words):
					self.printPuzzle()
					
					updatedWords = copy.deepcopy(words)
					updatedWords[move[1]].remove(word)

					updatedMoves = copy.deepcopy(moves[1:])
					
					if self.solve(updatedWords, updatedMoves):
						return True
					self.cells = copy.deepcopy(temp.cells)
			if self.fc:
				return False
		return False


	def checkGoal(self):
		for i in range(self.rows):
			for j in range(self.columns):
				if self.cells[i][j].val != BLOCK and self.cells[i][j].letter == '':
					return False
		return True


	def addWord(self, move, word, wordDict):
		for i in range(self.rows):
			for j in range(self.columns):
				if self.cells[i][j].val == move[0].val:
					temp = copy.deepcopy(self.cells)
					if move[2] == 'A':
						wInd = 0
						for z in range(j, j+len(word)):
							cell = temp[i][z]
							if cell.letter != '' and cell.letter != word[wInd]:
								return False
							elif cell.letter == '':
								if self.fc and cell.val != move[0].val and cell.val.isdigit():
									if not self.forwardCheck(word, wInd, wordDict, cell):
										return False
								cell.letter = word[wInd]
							wInd += 1

					elif move[2] == 'D':
						wInd = 0
						for z in range(i, i+len(word)):
							cell = temp[z][j]
							if cell.letter != '' and cell.letter != word[wInd]:
								return False
							elif cell.letter == '':
								if self.fc and cell.val != move[0].val and cell.val.isdigit():
									if not self.forwardCheck(word, wInd, wordDict, cell):
										return False
								cell.letter = word[wInd]
							wInd += 1
					self.cells = temp
					break
		return True

	def forwardCheck(self, word, wInd, wordDict, cell):
		if cell.across > 0:
			i = 0
			iteratedThrough = len(wordDict[cell.across])
			while i < len(wordDict[cell.across]):
				curWord = wordDict[cell.across][i]
				if curWord[0] == word[wInd] and curWord != word:
					return True
				elif curWord[0] != word[wInd] and curWord != word:
					wordDict[cell.across].append(wordDict[cell.across].pop(wordDict[cell.across].index(curWord)))
					i = i - 1
				i = i + 1
				iteratedThrough = iteratedThrough - 1
				if iteratedThrough == 0:
					return False

		if cell.down > 0:
			i = 0
			iteratedThrough = len(wordDict[cell.down])
			while i < len(wordDict[cell.down]):
				curWord = wordDict[cell.down][i]
				if curWord[0] == word[wInd] and curWord != word:
					return True
				elif curWord[0] != word[wInd] and curWord != word:
					wordDict[cell.down].append(wordDict[cell.down].pop(wordDict[cell.down].index(curWord)))
					i = i - 1
				i = i + 1
				iteratedThrough = iteratedThrough - 1
				if iteratedThrough == 0:
					return False
		return False


def fileToCrossword(filePath):
	with open(filePath) as file:
		csv_reader = csv.reader(file)
		crossword = list(csv_reader)
		return crossword


def readWordFile(filePath):
	wordDict = {}
	with open(filePath) as file:
		for word in file:
			word = word.replace("\n", "")
			wordLength = len(word)
			if wordLength in wordDict:
				wordDict[wordLength].append(word)
			else:
				wordDict[wordLength] = [word]
	return wordDict


def main():
	if len(sys.argv) != 3 and len(sys.argv) != 4:
		print('Usage: '+sys.argv[0]+' puzzleLayoutFile wordList hueristic')
		print('E.g:   '+sys.argv[0]+' puzzle.csv words.txt fc')
		print('hueristic parameter options:')
		print('\t- fc: Forward Checking')
		print('\t- lcv: Least Constraining Value')
		print('\t- dh: Degree Heuristic')
		print('\t- fc,lcv or lcv,fc: Forward Checking with Least Constraining Value')
		print('\t- fc,dh or dh,fc: Forward Checking with Degree Heuristic')
		print('\t- enter only 3 args for no hueristics')
		sys.exit()

	puzzleLayoutPath = sys.argv[1]
	wordListPath = sys.argv[2]
	fcArg = False
	if len(sys.argv) == 4:
		if 'fc' in sys.argv[3]:
			fcArg = True
	
	p = puzzle(fileToCrossword(puzzleLayoutPath), readWordFile(wordListPath), fc=fcArg)
	p.generateTableMap()

	lcvArg = False
	dhArg = False
	if len(sys.argv) == 4:
		if 'lcv' in sys.argv[3]:
			p.moves = sorted(p.moves, key=itemgetter(3), reverse=True)
		elif 'dh' in sys.argv[3]:
			p.moves = sorted(p.moves, key=itemgetter(3))
	
	start = time.time()
	p.solve(p.wordDict, p.moves)
	stop = time.time()
	print('Execution Time: '+str((stop-start)/60)+' minutes')
	p.printPuzzle()

if __name__ == "__main__":
	main()