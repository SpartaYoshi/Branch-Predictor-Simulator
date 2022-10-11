'''
************************************************
** SIMULADOR BÁSICO DE UN PREDICTOR DE SALTOS **
************************************************
Hecho por Asier Septién.
'''

import sys, os

def cl(c):
	if not os.name == 'posix': 
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
		print(f'{cl("bold green")}Uso: {cl("bold")}{sys.argv[0]} <fichero_saltos> <bits_BHT> <bits_BHR> [-v|o]')
		print(cl("")) # Resetear código ANSI de terminal
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

	# Abrir archivo
	try:
		with open(sys.argv[1], "r") as fs:
			
			try:
				bits_BHT = int(sys.argv[2])
				bits_BHR = int(sys.argv[3])

				if bits_BHT <= 0 or bits_BHR < 0:
					raise ValueError()
					
			except ValueError:
				print(f'{cl("bold red")}Error: {cl("")}Los valores de bits parametrados no son válidos.')
				exit(os.EX_USAGE) if os.name == 'posix' else exit(1)
			
			# Inicialización de variables
			pred = None
			aciertos = 0
			estado_actual = list([0] * (2 ** bits_BHR))  ## estado_actual = 0 (sin BHR)
			bht_index = 0
			bhr = list([0] * bits_BHR)
			estado_max = (2 ** bits_BHT) - 1
			umbral = (2 ** bits_BHT) / 2

			# Leer archivo
			seq_saltos = fs.read().split(' ')

			# Eliminar elementos vacíos residuales de haber leído (si existen) para conversión correcta a int
			if ('') in seq_saltos:
				seq_saltos.remove('')
			seq_saltos = [ int(s) for s in seq_saltos ]

			# Procesar
			for salto in seq_saltos:
				# Actualizar historial de registro (si hay BHR)
				if(bhr):
					bhr.pop(0) # Shiftear a la izquierda y meter salto nuevo
					bhr.append(salto)
					# Concatenar el historial en un string binario, y pasar a int para determinar estado a comprobar en la tabla
					bht_index = int(''.join([str(s) for s in bhr]), base=2)

				# Realizar predicción
				if estado_actual[bht_index] < umbral:
					pred = 0
				else:
					pred = 1
				
				# Comparar si predicción es correcta
				if pred is salto:
					aciertos += 1

				# Printear si verbose
				if op_verbose: 
					iter += 1
					print(f'{cl("bold blue")}Iteración: {cl("")}{iter}', end="")
					if bits_BHR > 0: print(f'{cl("bold blue")}, Registro: {cl("")}{"".join([str(s) for s in bhr])}', end="")
					print(f'{cl("bold blue")}, Estado: {cl("")}{estado_actual[bht_index]}', end="")
					print(f'{cl("bold blue")}, Predicción: {cl("")}{pred}' + \
						  f'{cl("bold blue")}, Salto: {cl("")}{salto}', end="")
					if pred is salto: print(f'{cl("bold green")}    Acierto')
					else: print(f'{cl("bold red")}    Fallo')

				# Cambiar de estado en BHT
				if not salto and estado_actual[bht_index] > 0:
					estado_actual[bht_index] -= 1
				elif salto and estado_actual[bht_index] < estado_max:
					estado_actual[bht_index] += 1
				


				if op_write: 
					output += f'{pred} '

			# Calcular tasa de aciertos
			tasa = 0.0
			if len(seq_saltos):
				tasa = aciertos / len(seq_saltos)
			print(f'{cl("bold cyan")}Aciertos: {cl("bold")}{aciertos} de {len(seq_saltos)}' + \
				  f'{cl("bold cyan")}, Precisión: {cl("bold")}{tasa:.2%}')

			# Generar fichero de predicciones
			if op_write:
				try:
					fpname = input(f"{cl('bold yellow')}Introduce nombre de fichero a generar: {cl('')}")
					with open(fpname, 'wb') as fp:
						output += '\n'
						fp.write(output.encode())
						print(f'Fichero {cl("bold")}{fpname} {cl("")}generado.')
				except:
					print(f'{cl("bold red")}Error: {cl("")}No se puede generar el fichero de predicciones.')

			print(cl("")) # Resetear código ANSI de terminal
			exit(0)

	except FileNotFoundError:
		print(f'{cl("bold red")}Error: {cl("")}El fichero "{sys.argv[1]}" no existe.')
		exit(os.EX_OSFILE) if os.name == 'posix' else exit(2)
	
	except ValueError:
		print(f'{cl("bold red")}Error: {cl("")}El fichero "{sys.argv[1]}" contiene datos inválidos. No se puede simular.')
		exit(os.EX_DATAERR) if os.name == 'posix' else exit(3)

	except PermissionError:
		print(f'{cl("bold red")}Error: {cl("")}El fichero "{sys.argv[1]}" no tiene permisos de lectura.')
		exit(os.EX_NOPERM) if os.name == 'posix' else exit(4)

	except MemoryError or OverflowError:
		print(f'{cl("bold red")}Error: {cl("")}El tamaño parametrado del registro BHR es demasiado grande para la simulación.')
		exit(os.EX_DATAERR) if os.name == 'posix' else exit(5)

if __name__ == '__main__':
	main()
	