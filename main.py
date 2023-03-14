from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import pandas as pd

#Se importa la base de datos que se usará
score_df = pd.read_csv("Merge.csv")
movie_df = pd.read_csv("ConsolidadoGeneral.csv")

app = FastAPI(title='Consultas Plataformas de Streaming',
            description='Start-up que provee servicios de agregación de plataformas de streaming.',
            version='1.0.0')

##Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN.
@app.get("/get_max_duration/")
async def get_max_duration(year: int = None, platform: str = None, duration_type: str = None):
    # Filtra por los parametros entregados 'year', 'platform', 'duration_type'
    filtered_df = movie_df
    if year:
        filtered_df = filtered_df[filtered_df['release_year'] == year]
    if platform:
        filtered_df = filtered_df[filtered_df['platform'] == platform]
    if duration_type:
        filtered_df = filtered_df[filtered_df['duration_type'] == duration_type]

    # Ordena los valores de manera descendente
    sorted_df = filtered_df.sort_values(by='duration_int', ascending=False)
    # Se obtiene el titulo de la plícula y la duración máxima
    max_duration_movie = sorted_df.iloc[0]['title']
    max_duration_movie1 = sorted_df.iloc[0]['duration_int']
    return {"mensaje": f"Titulo: {max_duration_movie} Tipo: {duration_type} Duración Total: {max_duration_movie1}"}

##Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año (la función debe llamarse get_score_count(platform, score, year))
@app.get("/get_score_count/")
def get_score_count(platform: str, score: Optional[int], year: int):
    # Hace el filtro de acuerdo con los valores seleccionados
    filtered_movies = score_df[(score_df["platform"] == platform) & (score_df["score"] > score) & (score_df["release_year"] == year)]
    # Hace el conteo total
    count = len(filtered_movies)
    return {"count": count}

##Cantidad de películas por plataforma con filtro de PLATAFORMA. (La función debe llamarse get_count_platform(platform))
@app.get("/get_count_platform/")
def get_count_platform(platform):
    # Filtra las peliculas dependiendo de la plataforma seleccionada 'platform'
    filtered_movies = movie_df[(movie_df["platform"] == platform)]
    # Hace el conteo total por la plataforma seleccionada
    count = len(filtered_movies)
    return count

##Actor que más se repite según plataforma y año. (La función debe llamarse get_actor(platform, year))
@app.get("/get_actor/")
def get_actor(platform: str, year: int):
    # Filtrar el DataFrame para seleccionar solo las filas que corresponden a la plataforma y el año especificados
    filtered_df = movie_df[(movie_df['platform'] == platform) & (movie_df['release_year'] == year)]
    
    # Eliminar las filas que contienen valores nulos en la columna 'actor'
    filtered_df = filtered_df.dropna(subset=['cast'])
    
    # Contar cuántas veces aparece cada actor en la columna 'actor'
    actor_counts = filtered_df['cast'].value_counts()
    
    # Verificar si la serie actor_counts está vacía
    if actor_counts.empty:
        return {"mensaje": f"No se encontraron actores para la plataforma {platform} en el año {year}"}
    
    # Obtener el índice del valor máximo en la serie actor_counts
    max_actor = actor_counts.idxmax()
    return {"Actor/s": max_actor}