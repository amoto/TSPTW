# TSPTW

Este programa intenta encontrar una solución al problema TSPTW por medio de una estrategia de VNS con 2-opt y un preprocesamiento para reducir los arcos que se pueden utilizar del grafo.

## Ejecución

Para ejecutar el programa es necesario ejecutar el archivo python `tsptw.py`, pasandole como primer parámetro la cantidad de segundos que tiene para ejecutar, y como segundo parámetro el nombre del archivo de caso de prueba SolomonPotvinBengio a ejecutar.
```
python3 tsptw.py [timeout] [case_file]
```
Por ejemplo, para decirle al programa que ejecute el caso *rc_201.1.txt* con un tiempo límite de 2 segundos, se haría de la siguiente forma:
```
python3 tsptw.py 2 rc_201.1.txt
```