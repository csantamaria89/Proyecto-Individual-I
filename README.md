<h1 align="center">
Proyecto Individual N°1
</h1>

El objetivo de este proyecto de **`Data Scientist`** es analizar y utilizar datos relevantes para proporcionar información valiosa que permita la toma de decisiones fundamentadas en diferentes áreas de interés, utilizando herramientas y técnicas de análisis y visualización de datos, modelado estadístico y aprendizaje automático, con el fin de mejorar la eficiencia, la productividad y la rentabilidad en este caso para una organización ficticia.

<h1 align="center">
Rol a desarrollar 👨‍💻
</h1>

Empezaste a trabajar como **`Data Scientist`** en una start-up que provee servicios de agregación de plataformas de streaming. El mundo es bello y vas a crear tu primer modelo de ML (Machine Learning) que soluciona un problema de negocio: un sistema de recomendación que aún no ha sido puesto en marcha!

<p align="center">
<img src="https://github.com/csantamaria89/Proyecto-Individual-I/blob/main/assets/streaming.jpg"  height=300>
</p>

<h1 align="center">
<br>🚀 Quick start MVP Ingeniería de datos</br>
 <br>TRANSFORMACIONES</br>
</h1>
Para este MVP no necesitas perfección, ¡necesitas rapidez! ⏩ Vas a hacer estas, y solo estas, transformaciones a los datos:
<br></br>

Antes de iniciar con las transformaciones, es importante aclarar que leimos los Datasets e implementamos un dataframe por medio de la libreria pandas.
[Nota] puede ver todo el procedimiento en el archivo Transformaciones.ipynb adjunto en este repositorio

+ Generar campo id: Cada id se compondrá de la primera letra del nombre de la plataforma, seguido del show_id ya presente en los datasets (ejemplo para títulos de Amazon = as123)

```shell
# Función lambda para agregar un caracter al inicio de cada valor en la columna 'show_id'
add_char = lambda x: 'a' + x
# Aplicamos la función a la columna 'show_id' usando el método apply()
df_amazon['show_id'] = df_amazon['show_id'].apply(add_char)
```
Se realizarón las agregaciones de acuerdo con la siguiente nomenclatura:

<table>
<tr>
  <td><strong>Caracter</strong></td>
  <td><strong>Plataforma</strong></td>
</tr>

<tr>
  <td>a</td>
  <td>Amazon</td>
</tr>

<tr>
  <td>n</td>
  <td>Netflix</td>
</tr>
<tr>
  <td>d</td>
  <td>Disney+</td>
</tr>
<tr>
  <td>h</td>
  <td>Hulu</td>
</tr>
</table>

+ Los valores nulos del campo rating deberán reemplazarse por el string “**`G`**” (corresponde al maturity rating: “general for all audiences”)
```shell
df_amazon['rating'] = df_amazon['rating'].fillna("G")
#Utilizamos la función Fillna para que en todos aquellos valores nulos se reeplazara por el caracter en especifico. 
#En este caso "G" en la columna 'rating'
```

+ De haber fechas, deberán tener el formato **`AAAA-mm-dd`**
```shell
df_amazon['date_added'] = pd.to_datetime(df_amazon['date_added'])
df_amazon['date_added'] = df_amazon['date_added'].dt.strftime('%Y-%m-%d')
```
Estas dos líneas de código convierten la columna 'date_added' de un dataframe llamado 'df_amazon' a un formato de fecha y luego lo convierten en una cadena de texto con el formato solicitado 'YYYY-MM-DD'.

+ Los campos de texto deberán estar en **minúsculas**, sin excepciones
```shell
# Aplicamos la función str.lower() a todos los valores del DataFrame utilizando el método applymap()
df_amazon = df_amazon.applymap(lambda x: x.lower() if type(x) == str else x)
df_amazon.head()
```

+ El campo ***duration*** debe convertirse en dos campos: **`duration_int`** y **`duration_type`**. El primero será un integer y el segundo un string indicando la unidad de medición de duración: min (minutos) o season (temporadas)

```shell
# Utilizamos str.extract() para separar la cantidad de tiempo y la unidad de tiempo en dos columnas diferentes
df_amazon[['duration_int', 'duration_type']] = df_amazon['duration'].str.extract('(\d+) (\w+)')
df_amazon['duration_int'] = pd.to_numeric(df_amazon['duration_int'])
df_amazon.head()
```

El siguiente procedimiento se aplico a cada una de las plataformas de Streaming. En la siguiente sentencia se puede evidenciar el código resumido para esta caso la plataforma de DisneyPlus:
```shell
add_char = lambda x: 'd' + x

df_disney['show_id'] = df_disney['show_id'].apply(add_char)


df_disney['rating'] = df_disney['rating'].fillna("G")

df_disney['date_added'] = pd.to_datetime(df_disney['date_added'])
df_disney['date_added'] = df_disney['date_added'].dt.strftime('%Y-%m-%d')


df_disney = df_disney.applymap(lambda x: x.lower() if type(x) == str else x)

df_disney[['duration_int', 'duration_type']] = df_disney['duration'].str.extract('(\d+) (\w+)')
df_disney['duration_int'] = pd.to_numeric(df_disney['duration_int'])
```

Al final se evidenció que cada Dataset contenía las mismas variables por lo que se procedió a integrar todas las plataformas en un solo **`df`** y se creo una nueva columna denominada "plataforma" para indicar de acuerdo con la inicial del Id, a que plataforma correspondía:
```shell
# Unir los dos DataFrames
df_general = pd.concat([df_amazon, df_hulu, df_disney, df_netflix])

#Generar nueva columna que me in dica la plataforma

def set_platform(row):
    if row.startswith("a"):
        return "amazon"
    elif row.startswith("n"):
        return "netflix"
    elif row.startswith("h"):
        return "hulu"
    elif row.startswith("d"):
        return "disney"
    else:
        return "Otro"

# Crear una nueva columna "platform" basada en la columna "Id"
df_general["platform"] = df_general["show_id"].apply(set_platform)
df_general = df_general.rename(columns={"show_id": "movieId"}
```

<h1 align="center">
<br>📲DESARROLLO API</br>
</h1>
Se propone disponibilizar los datos de le empresa usando el framework <b>FastAPI</b>. Las consultas propuestas son las siguientes: 
<br></br>
Antes de resolver cada consulta, importamos las librerias a utilizar y llamamos los **`df`** respectivos para su correspondiente uso

```shell
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import pandas as pd

#Se importa la base de datos que se usará
score_df = pd.read_csv("Merge.csv")
movie_df = pd.read_csv("ConsolidadoGeneral.csv")
```

+ Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN. (la función debe llamarse get_max_duration(year, platform, duration_type))
```shell
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
```

+ Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año (la función debe llamarse get_score_count(platform, scored, year))

```shell
@app.get("/get_score_count/")
def get_score_count(platform: str, score: Optional[int], year: int):
    # Hace el filtro de acuerdo con los valores seleccionados
    filtered_movies = score_df[(score_df["platform"] == platform) & (score_df["score"] > score) & (score_df["release_year"] == year)]
    # Hace el conteo total
    count = len(filtered_movies)
    return {"count": count}
```

+ Cantidad de películas por plataforma con filtro de PLATAFORMA. (La función debe llamarse get_count_platform(platform))

```shell
@app.get("/get_count_platform/")
def get_count_platform(platform):
    # Filtra las peliculas dependiendo de la plataforma seleccionada 'platform'
    filtered_movies = movie_df[(movie_df["platform"] == platform)]
    # Hace el conteo total por la plataforma seleccionada
    count = len(filtered_movies)
    return count
```

+ Actor que más se repite según plataforma y año. (La función debe llamarse get_actor(platform, year))

```shell
@app.get("/get_actor/")
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
```
🚨Puedes visualizar la API desarrollada con el siguiente enlace:

+ [Deployment FastAPI](https://proyecto-deploy.onrender.com/docs#/) 👈

<br>🚨Para ver el paso a paso de la implementación, entrenamiento y testeo del modelo de **MachinLearning** ver el archivo:  [ModeloML](https://github.com/csantamaria89/Proyecto-Individual-I/blob/main/ModeloML.ipynb)

Puedes visualizar la API desarrollada con el siguiente enlace:

+ [ModeloML](https://huggingface.co/spaces/csanta89/ProyectoHenry) 👈

🚨Video explicativo:

+ [YouTube](https://www.youtube.com/watch?v=ao57TtVFkgI) 👈

