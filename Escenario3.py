#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 09:14:56 2023

@author: sebastianpedraza
"""

import psycopg2
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

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

# Crear la consulta SQL
sql = "SELECT * FROM victima;"

# Ejecutar la consulta y convertir los resultados en un DataFrame
df_victima = pd.read_sql_query(sql, conn)


# Cerrar la conexión
conn.close()

# Crear aplicación Dash
app = dash.Dash(__name__)

# Definir el diseño del tablero
app.layout = html.Div(children=[
    html.H1(children='Análisis de Víctimas'),

    # Gráfico de barras para la distribución de edades de las víctimas
    dcc.Graph(
        id='grafico-edades',
        figure=px.histogram(df_victima, x='edad_victima', nbins=20, title='Distribución de Edades de las Víctimas')
    ),

    # Gráfico de pastel para la distribución de género de las víctimas
    dcc.Graph(
        id='grafico-genero',
        figure=px.pie(df_victima, names='genero_victima', title='Distribución de Género de las Víctimas')
    )

])

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
