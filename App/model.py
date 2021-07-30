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


import config as cf
from DISClib.ADT import graph as gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
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
                    'conexiones': None,
                    'paises': None
                    }

        analyzer['paises'] = mp.newMap(numelements=500,
                                     maptype='PROBING'
                                     )

        analyzer['LP'] = mp.newMap(numelements=2600,
                                     maptype='PROBING'
                                     )

        analyzer['conexiones'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=4000
                                              )
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')
# Funciones para agregar informacion al catalogo

def new_LP(analyzer,lp):
    key_lp=lp['landing_point_id']
    mp.put(analyzer['LP'],key_lp,lp)

def new_country(analyzer,count):
    country_name=count['CountryName']
    mp.put(analyzer['paises'],country_name,count)

def set_new_conection(analyzer,new_conection):
    origin=new_conection['origin']
    destination=new_conection['destination']
    if not(gr.containsVertex(analyzer['conexiones'],origin)):
        gr.insertVertex(analyzer['conexiones'],origin)
    if not(gr.containsVertex(analyzer['conexiones'],destination)):
        gr.insertVertex(analyzer['conexiones'],destination)
    gr.addEdge(graph=analyzer['conexiones'], vertexa=origin, vertexb=destination, weight=0)


# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
