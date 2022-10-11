/***********************************************
** SIMULADOR BÁSICO DE UN PREDICTOR DE SALTOS **
************************************************
Hecho por Asier Septién.
*/

#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>

extern int errno;

int main (int argc, char *argv[]){

	if (argc != 4) {
		printf("Uso: predict-sim <input_saltos> <bits_BHT> <bits_BHR>\n");
		exit(EINVAL);
	}

	// Abrir archivo
	FILE *fs = fopen(argv[1], "r");
	if (fs == NULL){
		printf("Error: El fichero no existe.\n");
		exit(errno);
	}

	int bits_BHT = atoi(argv[2]);
	int bits_BHR = atoi(argv[3]);

	if (bits_BHT <= 0 || bits_BHR < 0) {
		printf("Error: Los valores de bits parametrados no son válidos.\n");
		exit(EINVAL);
	}

	int salto, pred;
	int aciertos = 0, num_saltos = 0;
	int estado_actual = 0;
	int estado_max = pow(2, bits_BHT) - 1;
	int umbral = pow(2, bits_BHT) / 2;

	while(fscanf(fs, "%d", &salto) != EOF) {
		// Llevar cuenta de total de saltos
		num_saltos++;
		
		// Realizar predicción (sin BHR)
		if (estado_actual < umbral)
			pred = 0;
		else
			pred = 1;
		

		// Comparar si predicción es correcta
		if (salto == pred)
			aciertos++;

		// Cambiar de estado en BHT
		if (!salto && estado_actual > 0){
			estado_actual--;
		}
		else if (salto && estado_actual < estado_max){
			estado_actual++;
		}
				
	}

	float tasa = 0.0;
	if (num_saltos != 0)
		tasa = (float) aciertos / num_saltos;
	printf("Aciertos: %d, tasa: %.2f\n", aciertos, tasa);


	exit(0);
}