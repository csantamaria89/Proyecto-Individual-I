from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import pandas as pd

tags_metadata = [
    {
        "name": "Material fílmico de máxima duración"
    },
    {
        "name": "Cantidad de material fílmico por plataforma de acuerdo a su score",
    },
    {
        "name": "Cantidad total de material fílmico por plataforma",
    },
    {
        "name": "Actor con más participación por plataforma",  
    },
]

#Se importa la base de datos que se usará
score_df = pd.read_csv("Merge.csv")
movie_df = pd.read_csv("ConsolidadoGeneral.csv")

app = FastAPI(title='Consultas Plataformas de Streaming',
            description='Start-up que provee servicios de agregación de plataformas de streaming. By Camilo Santamaría',
            version='1.0.0', openapi_tags=tags_metadata)

##Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN.
@app.get("/get_max_duration/",  tags=["Material fílmico de máxima duración"])
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
@app.get("/get_score_count/", tags=["Cantidad de material fílmico por plataforma de acuerdo a su score"])
def get_score_count(platform: str, score: Optional[int], year: int):
    # Hace el filtro de acuerdo con los valores seleccionados
    filtered_movies = score_df[(score_df["platform"] == platform) & (score_df["score"] > score) & (score_df["release_year"] == year)]
    # Hace el conteo total
    count = len(filtered_movies)
    return {"count": count}

##Cantidad de películas por plataforma con filtro de PLATAFORMA. (La función debe llamarse get_count_platform(platform))
@app.get("/get_count_platform/", tags=["Cantidad total de material fílmico por plataforma"])
def get_count_platform(platform):
    # Filtra las peliculas dependiendo de la plataforma seleccionada 'platform'
    filtered_movies = movie_df[(movie_df["platform"] == platform)]
    # Hace el conteo total por la plataforma seleccionada
    count = len(filtered_movies)
    return count

##Actor que más se repite según plataforma y año. (La función debe llamarse get_actor(platform, year))
@app.get("/get_actor/", tags=["Actor con más participación por plataforma"])
async def count_actors(platform: str, year: int):
    # Filtrar el DataFrame por plataforma y año
    df_filtered = movie_df.loc[(movie_df['platform'] == platform) & (movie_df['release_year'] == year)]

    # Dividir la columna de actores en filas
    df_actors = df_filtered['cast'].str.split(',', expand=True).stack().reset_index(level=0).rename(columns={0:'cast'})

    # Contar la frecuencia de cada actor
    actor_counts = df_actors['cast'].value_counts().reset_index(name='count').rename(columns={'index':'cast'})

    # Encontrar el actor más común
    actor_max_count = actor_counts.iloc[0]['cast']

    return {'platform': platform, 'year': year, 'actor': actor_max_count}