"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from hashlib import new
import config as cf
import random
from DISClib.ADT import graph as gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from math import radians, cos, sin, asin, sqrt
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc as s
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import prim
from DISClib.Utils import error as error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def new_analyer():
    try:
        analyzer = {
                    'LP': None,#Landing points
                    'LP_id':None,#<id,nombre>
                    'conexiones': None,
                    'paises': None
                    }

        analyzer['paises'] = mp.newMap(numelements=500,
                                     maptype='PROBING'
                                     )

        analyzer['LP'] = mp.newMap(numelements=2600,
                                     maptype='PROBING'
                                     )

        analyzer['LP_id'] = mp.newMap(numelements=2600,
                                     maptype='PROBING'
                                     )

        analyzer['conexiones'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=4000
                                              )
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')
# Funciones para agregar informacion al catalogo

def new_LP(analyzer,lp):
    key_lp=lp['name'].split(",")
    key_lp=key_lp[0]+","+key_lp[-1]
    mp.put(analyzer['LP'],key_lp,lp)#Hay puntos con el mismo nombre inicial, así que se pone el nombre de la ciudad y del pais.
    mp.put(analyzer['LP_id'],lp['landing_point_id'],key_lp)#Se inserta la entra en un mapa id-nombre. Esto se hace para facilitar el req 2

def new_country(analyzer,count,valid_id):
    country_name=count['CountryName']
    mp.put(analyzer['paises'],country_name,count)#Inserta el pais en el mapa.

    name_capital=count['CapitalName']+", "+country_name
    if not(mp.contains(analyzer['LP'],name_capital)):#Si la capital de este pais no tiene un LP
        id_new=None
        run=True
        while run:#esto es para poner una id a las capitales
            r=random.randint(19251,20251)#19250 es la id más grande de todas las que estan en el csv.
            if not(lt.isPresent(valid_id,str(r))):
                id_new=str(r)
                lt.addLast(valid_id,id_new)
                run=False
        gr.insertVertex(analyzer['conexiones'],id_new)#Añade el vertice al grafo. El vertice tendra la id de la ciudad añadida.
        new_lp={
            "landing_point_id":id_new,
            "id":count['CapitalName']+", "+count['CountryName'],
            'name':count['CapitalName']+", "+count['CountryName'],
            'latitude':count['CapitalLatitude'],
            'longitude':count['CapitalLongitude']
            }#Se configuran los datos del nuevo punto de enlace
        for i in lt.iterator(mp.valueSet(analyzer['LP'])):#Se recorren todos los puntos de enlace existentes, si son del mismo pais, se conectan a la capital.
            pais_i=i['name'].split(',')#Divide el nombre del LP en una lista separada por comas, el ultimo elemento es el nombre del pais
            pais_i=pais_i[-1]#Toma el nombre del pais
            pais_i=pais_i[1:]#Quita el espacio que va a tener al inicio
            if pais_i==country_name:
                #print(country_name, i['name'])
                lat1=float(i['latitude'])
                long1=float(i['longitude'])
                lat2=float(new_lp['latitude'])
                long2=float(new_lp['longitude'])
                wd=haversine(long1, lat1, long2, lat2)#calculo del peso del camino
                gr.addEdge(graph=analyzer['conexiones'], vertexa=i['landing_point_id'], vertexb=new_lp['landing_point_id'], weight=wd)
                gr.addEdge(graph=analyzer['conexiones'], vertexa=new_lp['landing_point_id'], vertexb=i['landing_point_id'], weight=wd)
        new_LP(analyzer,new_lp)#Se añade el nuevo punto de enlace despues de recorrer los existentes para evitar el error en el que se enlaza a si mismo.

def set_new_conection(analyzer,new_conection):
    origin=new_conection['origin']
    destination=new_conection['destination']
    if not(gr.containsVertex(analyzer['conexiones'],origin)):
        gr.insertVertex(analyzer['conexiones'],origin)
    if not(gr.containsVertex(analyzer['conexiones'],destination)):
        gr.insertVertex(analyzer['conexiones'],destination)
    wg=None
    if new_conection['cable_length']!='n.a.':
        wg=new_conection['cable_length']
        wg=wg.replace(' km','')
        wg=float(wg.replace(",",''))
    else: #Si la distancia no viene en la tabla entonces hay que calcularla.
        name_1=me.getValue(mp.get(analyzer['LP_id'],origin))
        name_2=me.getValue(mp.get(analyzer['LP_id'],destination))

        long1=float(me.getValue(mp.get(analyzer['LP'],name_1))['longitude'])
        long2=float(me.getValue(mp.get(analyzer['LP'],name_2))['longitude'])
        lat1=float(me.getValue(mp.get(analyzer['LP'],name_1))['latitude'])
        lat2=float(me.getValue(mp.get(analyzer['LP'],name_2))['latitude'])
        wg=haversine(long1, lat1, long2, lat2)
    gr.addEdge(graph=analyzer['conexiones'], vertexa=origin, vertexb=destination, weight=wg)


# Funciones para creacion de datos

# Funciones de consulta
def connected_components(graph,lp1,lp2):
    scc=s.KosarajuSCC(graph)
    n=s.connectedComponents(scc)
    lps_sc=s.stronglyConnected(scc,lp1,lp2)
    return n,lps_sc

def ruta_minima(graph,vert_origen):
    return djk.Dijkstra(graph,vert_origen)

def red_expansion_minima(graph):
    return prim.PrimMST(graph)

def rama_mas_larga(graph):
    red=red_expansion_minima(graph['conexiones'])
    vertices_A=lt.newList('ARRAY_LIST')
    vertices_B=lt.newList('ARRAY_LIST')
    for arco in lt.iterator(red['edgeTo']['table']):
        if arco['key']!=None:
            lt.addLast(vertices_A, arco['value']['vertexA'])
            lt.addLast(vertices_B, arco['value']['vertexB'])

    mayor_rama=0
    rama_def=None
    i=1
    while i<=lt.size(red['edgeTo']['table']):
        arco=lt.getElement(red['edgeTo']['table'], i)
        rama=[]
        long=0
        if arco['key']!=None:
            vertice_a=arco['value']['vertexA']
            vertice_b=arco['value']['vertexB']

            while lt.isPresent(vertices_A, vertice_b)!=0:
                long+=1
                vertice_a=vertice_b
                vertice_b=lt.getElement(vertices_B, lt.isPresent(vertices_A, vertice_b))
                LP_a=me.getValue(mp.get(graph['LP_id'], vertice_a))
                LP_b=me.getValue(mp.get(graph['LP_id'], vertice_b))
                rama.append((LP_a, LP_b))
                            
        if long>mayor_rama:
            mayor_rama=long
            rama_def=rama
        i+=1
    return rama_def

# Funciones utilizadas para comparar elementos dentro de una lista
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
# Funciones de ordenamiento
