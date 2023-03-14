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
🚀 Quick start TRANSFORMACIONES
</h1>
Para este MVP no necesitas perfección, ¡necesitas rapidez! ⏩ Vas a hacer estas, y solo estas, transformaciones a los datos:
<br></br>

Antes de iniciar con las transformaciones, es importante aclarar que leimos los Datasets e implementamos un dataframe por medio de la libreria pandas.
<b>Nota:</b> puede ver todo el procedimiento en el archivo Transformaciones.ipynb adjunto en este repositorio

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
