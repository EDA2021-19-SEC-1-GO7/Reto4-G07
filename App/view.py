﻿"""
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
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.ADT import stack
from DISClib.ADT import graph as gr
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

doc_connections='connections.csv'
doc_paises='countries.csv'
doc_lp='landing_points.csv'


def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Encontrar cantidad de clústeres y si 2 landing points están en el mismo clúster")
    print("3- Encontrar ruta mínima en distancia entre dos países")
    print("4- Encontrar red de expansión mínima en distancia")

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
        carga=controller.load(analizer, doc_connections, doc_paises, doc_lp)
        paises=analizer["paises"]
        print("Numero de paises: "+str(mp.size(paises)))
        print("Numero de conexiones: "+str(gr.numEdges(analizer["conexiones"])))
        print("Numero de landing points: "+str(mp.size(analizer["LP"])))
        primer_LP=lt.firstElement(carga[1])
        ultimo_pais=lt.lastElement(carga[0])
        print('Información del primer landing point Identificador: {}, Nombre: {}, Latitud: {}, Longitud: {}'.format(primer_LP['landing_point_id'], primer_LP['name'], primer_LP['latitude'], primer_LP['longitude']) )
        print('Información del último_pais Población: {}, Número de usuarios de Internet: {}'.format(ultimo_pais['Population'], ultimo_pais['Internet users']))
        
    elif int(inputs[0]) == 2:
        nombre_1=input("Nombre del landing point 1: ")
        nombre_2=input("Nombre del landing point 2: ")
        lp1=me.getValue(mp.get(analizer['LP'],nombre_1))
        lp1=lp1["landing_point_id"]
        lp2=me.getValue(mp.get(analizer['LP'],nombre_2))
        lp2=lp2["landing_point_id"]
        res=controller.connected_components(analizer['conexiones'],lp1,lp2)
        print("hay "+str(res[0])+" componentes conectados en el grafo.")
        if res[1]:
            print("Los landing points ingresados estan en el mismo componente.")
        else:
            print("Los landing points ingresados no estan en el mismo componente.")
    elif int(inputs[0]) == 3:
        ciudad_salida=input("Capital de salida: ")#ej:Bogota, Colombia
        ciudad_entrada=input("Capital de entrada: ")
        vertice_salida=me.getValue(mp.get(analizer['LP'],ciudad_salida))['landing_point_id']
        vertice_entrada=me.getValue(mp.get(analizer['LP'],ciudad_entrada))['landing_point_id']
        min_path=controller.ruta_minima(analizer['conexiones'],vertice_salida)
        
        print('Distancia total de la ruta: '+str(round(djk.distTo(min_path,vertice_entrada),2))+' km')
        path=djk.pathTo(min_path,vertice_entrada)
        
        while not(stack.isEmpty(path)):
            segmento=stack.pop(path)
            verA=segmento["vertexA"]
            verB=segmento["vertexB"]
            wg=float(segmento["weight"])
            print(me.getValue(mp.get(analizer['LP_id'],verA))+"---"+str(round(wg,2))+" km--->"+me.getValue(mp.get(analizer['LP_id'],verB)))

    elif int(inputs[0]) == 4:
        red=controller.red_expansion_minima(analizer['conexiones'])
        rama=controller.rama_mas_larga(analizer)
        distancia=0
        costos=mp.valueSet(red['distTo'])
        for costo in lt.iterator(costos):
            if costo!=None:
                distancia+=costo
        print('Hay {} nodos conectados a las red de expansión mínima'.format(mp.size(red['marked'])))
        print('El costo de la red de expansión mínima es de {:.3f} km'.format(distancia))
        print('La rama más larga, con {} arcos es'.format(len(rama)))
        i=0
        while i<len(rama):
            print(rama[i])
            i+=1

    else:
        sys.exit(0)
sys.exit(0)
