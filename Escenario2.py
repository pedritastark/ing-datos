#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 22:19:54 2023

@author: sebastianpedraza
"""

from dash import Dash, dcc, html
import folium
from folium.plugins import HeatMap
import pandas as pd
import psycopg2

# Parámetros de conexión
db_params = {
    'dbname': 'ProyectoDatos',
    'user': 'postgres',
    'password': 'J19f15G11a08',
    'host': 'localhost',
    'port': '5433',
}

# Crear la cadena de conexión
connection_string = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"

# Crear la conexión
conn = psycopg2.connect(connection_string)

# Crear la consulta SQL para obtener los datos de ubicación y frecuencia
sql = """
SELECT latitud, longitud, COUNT(codigo_caso) AS freq
FROM ubicacion
GROUP BY latitud, longitud;
"""

# Ejecutar la consulta y convertir los resultados en un DataFrame
df = pd.read_sql_query(sql, conn)

# Cerrar la conexión
conn.close()

# Crear un mapa de Folium
m = folium.Map([df['latitud'].mean(), df['longitud'].mean()], zoom_start=10)

# Agregar el mapa de calor al mapa
HeatMap(data=df[['latitud', 'longitud', 'freq']].dropna().values.tolist()).add_to(m)

# Convertir el mapa a HTML
html_string = m._repr_html_()

# Crear la aplicación Dash
app = Dash(__name__)

app.layout = html.Div([
    html.Iframe(id='map', srcDoc=html_string, width='100%', height='600')
])

if __name__ == '__main__':
    app.run_server(debug=True)