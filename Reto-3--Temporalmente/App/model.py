"""
 * Copyright 2020, Departamento de sistemas y Computación
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------
def newAnalyzer():

    analyzer = {'accidents': None,
                'dateIndex': None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
    return analyzer

# Funciones para agregar informacion al catalogo
def addAccident(analyzer, accident):
    """
    """
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['dateIndex'], accident)
    return analyzer

def addDateIndex(datentry, accident):
    lst = datentry['lstaccidents']
    lt.addLast(lst, accident)
    accidentIndex = datentry['accidentIndex']
    offentry = m.get(accidentIndex, accident['Start_Time'])
    if (offentry is None):
        entry = newaccidentEntry(accident['Start_Time'], accident)
        lt.addLast(entry['lstaccidents'], accident)
        m.put(accidentIndex, accident['Start_Time'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstaccidents'], accident)
    return datentry

def updateDateIndex(map, accident):
    occurreddate = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdate.date())
    if entry is None:
        datentry = newDataEntry(accident)
        om.put(map, accidentdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accident)
    return map

def newDataEntry(accident):
    entry = {'accidentIndex': None, 'lstaccidents': None}
    entry['accidentIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareaccidents)
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newaccidentEntry(accidentgrp, accident):
    ofentry = {'accident': None, 'lstaccidents': None}
    ofentry['accident'] = accidentgrp
    ofentry['lstaccidents'] = lt.newList('SINGLELINKED', compareaccidents)
    return ofentry
# ==============================
# Funciones de consulta
# ==============================
def accidentsSize(analyzer):
    return lt.size(analyzer['accidents'])


def indexHeight(analyzer):
   
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):

    return om.maxKey(analyzer['dateIndex'])

def getAccidents(analyzer, initialDate):
    lst = om.values(analyzer['dateIndex'], initialDate, initialDate)
    return lst
# ==============================
# Funciones de Comparacion
# ==============================
def compareIds(id1, id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareDates(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
def compareaccidents(accident1, accident2):
    accident = me.getKey(accident2)
    if (accident1 == accident):
        return 0
    elif (accident1 > accident):
        return 1
    else:
        return -1
