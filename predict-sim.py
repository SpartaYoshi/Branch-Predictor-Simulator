#!/usr/bin/python3 

'''
**************************************
** BASIC BRANCH PREDICTOR SIMULATOR **
**************************************
Made by Asier Septién.
'''

import sys, os

def cl(c):
	if os.name == 'nt': 
		return ''

	c = str(c)
	code = '\x1b['
	if 'bold' in c: code += '1;'
	else: 			code += '0;'

	if 'red' in c:      code += '31;'
	elif 'green' in c:  code += '32;'
	elif 'cyan' in c:   code += '36;'
	elif 'blue' in c:   code += '34;'
	elif 'yellow' in c: code += '33;'
	else:			    code += '37;'
	
	code += '40m'
	return code


def main():
	if len(sys.argv) < 4 or len(sys.argv) > 5:
		print(f'{cl("bold green")}Use: {cl("bold")}{sys.argv[0]} <branch_file> <bits_BHT> <bits_BHR> [-v|o]')
		print(cl("")) # Reset ANSI code in terminal
		exit(os.EX_USAGE) if os.name == 'posix' else exit(1)

	op_verbose = False
	op_write = False
	for op in sys.argv[4:]:
		if not '-' in op: break
		if 'v' in op:	  
			iter = 0
			op_verbose = True
		if 'o' in op:
			output = ''	  
			op_write = True

	# Open file
	try:
		with open(sys.argv[1], "r") as fs:
			
			try:
				bits_BHT = int(sys.argv[2])
				bits_BHR = int(sys.argv[3])

				if bits_BHT <= 0 or bits_BHR < 0:
					raise ValueError()
					
			except ValueError:
				print(f'{cl("bold red")}Error: {cl("")}Bit parameter values are invalid.')
				exit(os.EX_USAGE) if os.name == 'posix' else exit(1)
			
			# Variable init
			pred = None
			hits = 0
			current_state = list([0] * (2 ** bits_BHR))  ## current_state = 0 (no BHR)
			bht_index = 0
			bhr = list([0] * bits_BHR)
			max_state = (2 ** bits_BHT) - 1
			threshold = (2 ** bits_BHT) / 2

			# Leer archivo
			branch_seq = fs.read().split(' ')

			# Remove residual empty elements from reading file (if they exist) for correct conversion to int
			if ('') in branch_seq:
				branch_seq.remove('')
			branch_seq = [ int(s) for s in branch_seq ]

			# Process branch sequence
			for branch in branch_seq:
				if(bhr):
					# Concatenate BHR register history onto binary string, convert to int to determine current state in BHT table
					bht_index = int(''.join([str(s) for s in bhr]), base=2)

				# Make prediction
				if current_state[bht_index] < threshold:
					pred = 0
				else:
					pred = 1
				
				# Compare if prediction is correct
				if pred is branch:
					hits += 1
				
				# Update register history (if BHR)
				if(bhr):
					bhr.pop(0) # Shift to left and insert recent branch
					bhr.append(branch)

				# Print if verbose
				if op_verbose: 
					iter += 1
					print(f'{cl("bold blue")}Iteration: {cl("")}{iter}', end="")
					if bits_BHR > 0: print(f'{cl("bold blue")}, Register: {cl("")}{"".join([str(s) for s in bhr])}', end="")
					print(f'{cl("bold blue")}, State: {cl("")}{current_state[bht_index]}', end="")
					print(f'{cl("bold blue")}, Prediction: {cl("")}{pred}' + \
						  f'{cl("bold blue")}, Branch: {cl("")}{branch}', end="")
					if pred is branch: print(f'{cl("bold green")}    Hit')
					else: print(f'{cl("bold red")}    Miss')

				# Switch state in BHT
				if not branch and current_state[bht_index] > 0:
					current_state[bht_index] -= 1
				elif branch and current_state[bht_index] < max_state:
					current_state[bht_index] += 1
				
				# Write to file if output is enabled
				if op_write: 
					output += f'{pred} '

			# Calculate accuracy rate
			rate = 0.0
			if len(branch_seq):
				rate = hits / len(branch_seq)
			print(f'{cl("bold cyan")}Hits: {cl("bold")}{hits} of {len(branch_seq)}' + \
				  f'{cl("bold cyan")}, Accuracy rate: {cl("bold")}{rate:.2%}')

			# Generate prediction file
			if op_write:
				try:
					fpname = input(f"{cl('bold yellow')}Enter file name to generate: {cl('')}")
					with open(fpname, 'wb') as fp:
						output += '\n'
						fp.write(output.encode())
						print(f'File {cl("bold")}{fpname} {cl("")}generated.')
				except:
					print(f'{cl("bold red")}Error: {cl("")}Can\'t create prediction file.')

			print(cl("")) # Reset ANSI code in terminal
			exit(0)

	except FileNotFoundError:
		print(f'{cl("bold red")}Error: {cl("")}File "{sys.argv[1]}" does not exist.')
		exit(os.EX_OSFILE) if os.name == 'posix' else exit(2)
	
	except ValueError:
		print(f'{cl("bold red")}Error: {cl("")}File "{sys.argv[1]}" contains invalid data. Aborting simulation.')
		exit(os.EX_DATAERR) if os.name == 'posix' else exit(3)

	except PermissionError:
		print(f'{cl("bold red")}Error: {cl("")}File "{sys.argv[1]}" does not have read permissions.')
		exit(os.EX_NOPERM) if os.name == 'posix' else exit(4)

	except MemoryError or OverflowError:
		print(f'{cl("bold red")}Error: {cl("")}Size parameter for BHR register is too big for simulation.')
		exit(os.EX_DATAERR) if os.name == 'posix' else exit(5)

if __name__ == '__main__':
	main()
	