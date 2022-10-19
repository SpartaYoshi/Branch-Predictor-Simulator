#!/usr/bin/python3 

'''
***********************************************
** SIMULADOR BÁSICO DE UN PREDICTOR DE SALTOS **
************************************************
Hecho por Asier Septién.
'''

import sys, os

def main():
	if len(sys.argv) != 4:
		print(f'Uso: {sys.argv[0]} <input_saltos> <bits_BHT> <bits_BHR>')
		exit(os.EX_USAGE) if os.name == 'posix' else exit(1)


	# Abrir archivo
	try:
		with open(sys.argv[1], "r") as fs:

			bits_BHT = int(sys.argv[2])
			bits_BHR = int(sys.argv[3])

			if bits_BHT <= 0 or bits_BHR < 0:
				print("Error: Los valores de bits parametrados no son válidos.")
				exit(os.EX_USAGE) if os.name == 'posix' else exit(1)
			
			# Inicialización de variables
			pred = None
			aciertos = 0
			estado_actual = 0
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
				# Realizar predicción (sin BHR)
				if estado_actual < umbral:
					pred = 0
				else:
					pred = 1
				
				# Comparar si predicción es correcta
				if pred is salto:
					aciertos += 1

				# Cambiar de estado en BHT
				if not salto and estado_actual > 0:
					estado_actual -= 1
				elif salto and estado_actual < estado_max:
					estado_actual += 1

			# Calcular tasa de aciertos
			tasa = 0.0
			if len(seq_saltos):
				tasa = aciertos / len(seq_saltos)
			print(f'Aciertos: {aciertos} de {len(seq_saltos)}, tasa: {tasa:.2%}')
			
			exit(0)

	except FileNotFoundError:
		print(f'Error: El fichero "{sys.argv[1]}" no existe.')
		exit(os.EX_OSFILE) if os.name == 'posix' else exit(2)
	
	except ValueError:
		print(f'Error: El fichero "{sys.argv[1]}" contiene datos inválidos. No se puede simular.')
		exit(os.EX_DATAERR) if os.name == 'posix' else exit(3)

	except PermissionError:
		print(f'Error: El fichero "{sys.argv[1]}" no tiene permisos de lectura.')
		exit(os.EX_NOPERM) if os.name == 'posix' else exit(4)
	

if __name__ == '__main__':
	main()