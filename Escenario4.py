#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 04:58:44 2023

@author: sebastianpedraza
"""

import psycopg2
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
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
sql = """
SELECT t.codigo_crimen, c.descripcion_crimen, COUNT(*) AS frecuencia,
       RANK() OVER (ORDER BY COUNT(*) DESC) as rank,
       (COUNT(*) * 100.0 / total.total_crimenes) as porcentaje
FROM casos AS t
JOIN crimen AS c ON t.codigo_crimen = c.codigo_crimen
CROSS JOIN (SELECT COUNT(*) as total_crimenes FROM casos) as total
GROUP BY t.codigo_crimen, c.descripcion_crimen, total.total_crimenes
ORDER BY frecuencia DESC;
"""

# Ejecutar la consulta y convertir los resultados en un DataFrame
df = pd.read_sql_query(sql, conn)

# Cerrar la conexión
conn.close()

# Crear una nueva columna 'descripcion_crimen_agrupada' que agrupa todos los crímenes que no están en los primeros 5 en 'Otros'
df['descripcion_crimen_agrupada'] = df['descripcion_crimen'].where(df['rank'] <= 5, 'Otros')

# Sumar las frecuencias de los crímenes agrupados
df_agrupado = df.groupby('descripcion_crimen_agrupada').frecuencia.sum().reset_index()

# Crear el gráfico de torta
fig = px.pie(df_agrupado, values='frecuencia', names='descripcion_crimen_agrupada', title='Top Crímenes')

# Crear la aplicación Dash
# Crear la aplicación Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)