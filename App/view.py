"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

doc_conections='connections.csv'
doc_paises='countries.csv'
doc_lp='landing_points.csv'


def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Encontrar cantidad de clústeres y si 2 landing points están en el mismo clúster")
    print("3- Encontrar ruta mínima en distancia entre dos países")
    print("4- Encontrar red de expansión mínima en distancia")
    print("5- Gráficas")

analizer = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        analizer=controller.new_analizer()
        controller.load(analizer,doc_conections,doc_paises,doc_lp)
        paises=analizer["paises"]
        print("numero de paises: "+str(mp.size(paises)))
        print("numero de conexiones: "+str(gr.numEdges(analizer["conexiones"])))
        print("numero de landing points: "+str(mp.size(analizer["LP"])))
        
    elif int(inputs[0]) == 2:
        pass

    else:
        sys.exit(0)
sys.exit(0)
