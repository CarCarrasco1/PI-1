from fastapi import FastAPI, Request, Form
import pandas as pd
import numpy as np
from flask import Flask, request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from typing import Optional

app = FastAPI()

df_api= pd.read_csv(r'base_api.csv', sep= ',')



# Cargo la informacion para la API
@app.get('/about')
async def about():
    return 'API created with FastAPI and Uvicorn'

@app.get("/get_max_duration")
def get_max_duration(year: Optional[int] = None, platform: Optional[str] = None, duration_type: Optional[str] = None):

    # Copiar el DataFrame original
    filtered_df = df_api.copy()

    # Aplicar los filtros, si se especificaron
    if duration_type is not None:
        filtered_df = filtered_df[filtered_df['duration_type'] == duration_type]
    if year is not None:
        filtered_df = filtered_df[filtered_df['year'] == year]
    if platform is not None:
        filtered_df = filtered_df[filtered_df['platform'] == platform]

    # Obtener la fila con la duración máxima
    sorted_df = filtered_df.sort_values(by='duration_int', ascending=False)
    max_duration = sorted_df.iloc[0][['title']]

    return max_duration
"""
Esta función devuelve el título de la película o serie con la duración más larga que cumpla con ciertas condiciones.

Tiene tres argumentos opcionales: year, platform y duration_type. Estos son los filtros que se aplican para restringir 
la búsqueda de la película o serie con la duración máxima.
Si no se especifica ningún filtro, entonces se considera el DataFrame original.

Comienza por hacer una copia del DataFrame original (df_api). Luego, aplica los filtros según los argumentos pasados. 
Después, ordena el DataFrame resultante en orden descendente según la columna 'duration_int', que es la duración de la película 
o serie convertida a minutos (el DataFrame original contiene la duración en formato de tiempo).

Finalmente, devuelve el título de la película o serie con la duración máxima. Este título se obtiene tomando la primera 
fila del DataFrame ordenado y extrayendo el valor de la columna 'title'.

Es importante mencionar que si no hay películas o series que cumplan con las condiciones de los filtros, la función devolverá 
un valor nulo (None).

"""  

@app.get("/get_score_count/")
def get_score_count(platform: str, scored: int, year:int):

    # Filtrar los datos segun las condiciones
    df_filtered = df_api[(df_api["platform"] == platform) & (df_api["scored"] >= scored) & (df_api["year"] == year)]

    # Contar el numero de filas que cumplen las condiciones
    cantidad = len(df_filtered)

    # Devolver la cantidad de veces que se cumple la condicion
    return cantidad

"""
Esta función recibe tres parámetros obligatorios (platform, scored y year) que son utilizados para 
filtrar el DataFrame que contiene información sobre películas. 

'platform', 'scored' y 'year' son parámetros de la función que corresponden a la plataforma de la película, la puntuación 
mínima que debe tener y el año en que se lanzó, respectivamente.

Primero, se filtran los datos de df_api según estas condiciones. Para hacer esto, se utiliza la sintaxis de 
indexación booleana de pandas, que filtra las filas de df_api que cumplen las condiciones.

Luego se cuentan las filas resultantes utilizando la función len() y se almacena en la variable cantidad.

Finalmente, se devuelve cantidad como la cantidad de veces que se cumplieron las condiciones en el DataFrame df_api.

"""  


@app.get('/get_count_platform')
def get_count_platform(platform=None):
    
    if platform:
        df_filtered = df_api[df_api['platform'] == platform]
    else:
        df_filtered = df_api
    
    # contar la cantidad de peliculas por plataforma
    count_by_platform = df_filtered['platform'].value_counts()
    
    # si la plataforma existe en el dataframe, devolver la cantidad como un entero
    if platform in count_by_platform.index:
        return int(count_by_platform[platform])
    
    # si no se proporciono una plataforma, devolver la suma de todas las peliculas en el dataframe
    elif platform is None:
        return int(count_by_platform.sum())
    
    # si la plataforma no existe en el dataframe, devolver 0
    else:
        return 0
"""
Esta cuenta la cantidad de películas que hay en el dataframe agrupadas por plataforma y luego devuelve la cantidad total 
de películas en una plataforma determinada o en todo eldataframe, según se especifique o no un nombre de plataforma.

En detalle, si se especifica una plataforma, la función filtra el dataframe por esa plataforma. Luego, cuenta la cantidad 
de películas por plataforma y la devuelve como un entero si se encuentra en el dataframe o devuelve 0 si la plataforma
no se encuentra en el dataframe.

Por otro lado, si no se especifica una plataforma, devuelve la cantidad total de películas en el dataframe como un entero.

""" 

@app.get('/get_actor')
def get_actor(platform:str, year:int):
    
    global df_api

    # Filtrar por anio y plataforma
    filtered_df = df_api[(df_api['platform'] == platform) & (df_api['year'] == year)]

    # Contar la cantidad de veces que aparece cada actor en la columna 'cast'
    actor_count = filtered_df['cast'].str.split(',').explode().str.strip().value_counts()

    if actor_count.empty:
        return None
    else:
        return actor_count.index[0]
"""
Esta función se encarga de encontrar el actor que más aparece en películas de una plataforma y año específicos.

Primero, se filtra el dataframe df_api según la plataforma y año especificados en los parámetros. Luego, se cuenta 
la cantidad de veces que aparece cada actor en la columna 'cast' del dataframe resultante. Para hacer esto, 
se divide la cadena de texto en la columna 'cast' en una lista de actores usando la función split(','), 
se convierte esta lista en una serie usando la función explode(), se elimina cualquier espacio en blanco alrededor
de los nombres de los actores usando la función str.strip(), y se cuenta la cantidad de veces que aparece cada actor 
en la serie resultante usando la función value_counts().

Finalmente, el actor que más se repite se determina verificando la serie de conteo de actores. Si la serie está vacía,
es decir, no hay actores en la lista de reparto, entonces el resultado es None.
En caso contrario, se devuelve el nombre del actor que aparece en la primera posición de la serie, 
que es el que más se repite.

"""
