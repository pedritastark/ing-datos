#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 05:09:50 2023

@author: sebastianpedraza
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
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

# Crear la consulta SQL
sql = "SELECT * FROM fechas;"

# Ejecutar la consulta y convertir los resultados en un DataFrame
df = pd.read_sql_query(sql, conn)
print(df)

# Cerrar la conexión
conn.close()

# Convertir la columna 'fecha_reporte' a datetime y extraer el mes
df['fecha_reporte'] = pd.to_datetime(df['fecha_reporte'])
df['mes'] = df['fecha_reporte'].dt.month

# Crear un diccionario que mapee los números de mes a los nombres de mes
meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 
         7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}

# Reemplazar los números de mes con los nombres de mes
df['mes'] = df['mes'].replace(meses)

# Agrupar por mes y contar el número de casos
df_mes = df.groupby('mes').size().reset_index(name='casos')

# Crear el gráfico de barras
fig = px.bar(df_mes, x='mes', y='casos', title='Casos registrados por mes')

# Crear la aplicación Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
