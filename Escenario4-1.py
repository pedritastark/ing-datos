#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 23:03:27 2023

@author: sebastianpedraza
"""

import psycopg2
import pandas as pd
from prettytable import PrettyTable

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
ORDER BY frecuencia DESC
LIMIT 10;
"""

# Ejecutar la consulta y convertir los resultados en un DataFrame
df = pd.read_sql_query(sql, conn)

# Cerrar la conexión
conn.close()

# Crear una tabla bonita
table = PrettyTable()

# Establecer los nombres de las columnas
table.field_names = df.columns.tolist()

# Añadir las filas
for index, row in df.iterrows():
    table.add_row(row.tolist())

# Imprimir la tabla
print(table)