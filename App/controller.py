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
 """

import config as cf
import model
import csv
import model as m

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

# Funciones para la carga de datos
def new_analizer():
    return m.new_analyer()

def load(analizer,doc_conections,doc_paises,doc_lp):
    
    doc_paises = cf.data_dir + doc_paises
    input_file_paises = csv.DictReader(open(doc_paises, encoding="utf-8"),
                                delimiter=",")
    doc_conections = cf.data_dir + doc_conections
    input_file_conections = csv.DictReader(open(doc_conections, encoding="utf-8-sig"),
                                delimiter=",")
    doc_lp = cf.data_dir + doc_lp
    input_file_lp = csv.DictReader(open(doc_lp, encoding="utf-8"),
                                delimiter=",")

    for pais in input_file_paises:
        m.new_country(analizer,pais)
    for lp in input_file_lp:
        m.new_LP(analizer,lp)
    for con in input_file_conections:
        m.set_new_conection(analizer,con)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
