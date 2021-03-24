#!/usr/bin/python3
import subprocess
import time

wordFiles = ['task1Words.txt', 'words.txt']
puzzleFiles = ['task1Puzzle.csv', 'task2Puzzle.csv', 'task2Puzzle2.csv']
heuristics =['', 'fc', 'dh', 'lcv', 'fc,dh', 'fc,lcv']
CUTOFF_TIME = 5400 #90 mins

with open('results.txt', 'a') as file:
	for puzzleFile in puzzleFiles:
		for h in heuristics:
			if h == 'fc':
				heuristic = 'Forward Checking'
			elif h == 'dh':
				heuristic = 'Degree Heuristic'
			elif h == 'lcv':
				heuristic = 'Lowest Constraint Value'
			elif h == 'fc,dh':
				heuristic = 'Degree Heuristic with Forward Checking'
			elif h == 'fc,lcv':
				heuristic = 'Lowest Constraint Value with Forward Checking'
			else:
				heuristic = 'No heuristics used'

			if puzzleFile == puzzleFiles[0]:
				wordFile = wordFiles[0]
			else:
				wordFile = wordFiles[1]

			print("--------------------------------------")
			print("Puzzle: "+puzzleFile)
			print("Heuristic: "+heuristic)

			file.write("--------------------------------------\n")
			file.write("Puzzle: "+puzzleFile+"\n")
			file.write("Heuristic: "+heuristic+"\n")

			try:
				start = time.time()
				output = subprocess.check_output(['python3', 
								'designCrossword.py', 
								puzzleFile,
								wordFile,
								h], timeout=CUTOFF_TIME)
				stop = time.time()
				output = output.decode('utf-8')

				print(output)
				print("--------------------------------------")

				file.write("Time: "+str((stop-start)/60)+" min\n")
				file.write("--------------------------------------\n")
				file.write(output)
				file.write("\n\n")
			except:
				stop = time.time()
				print("Execution ended due to cutoff time")
				print("--------------------------------------")

				file.write("Time: "+str((stop-start)/60)+" min\n")
				file.write("Execution ended after " + str(CUTOFF_TIME/60) + " minutes\n")
				file.write("--------------------------------------\n")
				file.write("\n\n")

