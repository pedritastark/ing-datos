#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 19:16:07 2023

@author: sebastianpedraza
"""

import psycopg2
from psycopg2 import sql
from prettytable import PrettyTable

class BaseDeDatos:
    def __init__(self, db_params):
        self.db_params = db_params
        self.connection = None
        self.cursor = None

    def conectar(self):
        try:
            self.connection = psycopg2.connect(**self.db_params)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise

    def ejecutar_consulta(self, tabla):
        try:
            query = sql.SQL("SELECT * FROM {} LIMIT 5").format(sql.Identifier(tabla))            
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            
            table = PrettyTable()
            table.field_names = [desc[0] for desc in self.cursor.description]
            table.add_rows(data)

            print(f"\nDatos de la tabla {tabla}:")
            print(table)
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            raise

    def cerrar_conexion(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

if __name__ == "__main__":
    # Parámetros de conexión
    db_params = {
        'dbname': 'ProyectoDatos',
        'user': 'postgres',
        'password': 'J19f15G11a08',
        'host': 'localhost',
        'port': '5433',
    }

    tablas = ['casos', 'estado', 'area', 'crimen', 'arma', 'premisa', 'ubicacion', 'delito', 'delitos_asociados', 'victima']
    try:
        # Crear una instancia de la clase BaseDeDatos
        base_datos = BaseDeDatos(db_params)
        base_datos.conectar()

        # Consultar y mostrar datos de cada tabla
        for tabla in tablas:
            base_datos.ejecutar_consulta(tabla)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        base_datos.cerrar_conexion() if 'base_datos' in locals() else None
