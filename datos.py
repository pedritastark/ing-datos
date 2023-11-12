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
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(tabla))
            self.cursor.execute(query)
            data = self.cursor.fetchall()

            # Crear una tabla bonita
            table = PrettyTable()
            table.field_names = [desc[0] for desc in self.cursor.description]
            table.add_rows(data)

            # Imprimir la tabla
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
        'dbname': 'nombre de la base',
        'user': 'usuario',
        'password': 'contraseña',
        'host': 'host',
        'port': 'puerto',
    }

    tablas = ['Caso', 'Estado', 'Area', 'Crimen', 'Arma', 'Premisa', 'Ubicacion', 'Delito', 'Delito_asociado', 'Victima']

    try:
        # Crear una instancia de la clase BaseDeDatos
        base_datos = BaseDeDatos(db_params)

        # Conectar a la base de datos
        base_datos.conectar()

        # Consultar y mostrar datos de cada tabla
        for tabla in tablas:
            base_datos.ejecutar_consulta(tabla)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Cerrar la conexión de manera segura
        base_datos.cerrar_conexion() if 'base_datos' in locals() else None
