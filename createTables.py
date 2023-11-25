#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 22:15:26 2023

@author: sebastianpedraza
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 21:50:55 2023

@author: sebastianpedraza
"""

import pandas as pd

def read_csv_file(filename): 
    
    try: 
        df = pd.read_csv(f'{filename}.csv')
        return df 
    
    except FileNotFoundError: 
        
        print(f"File {filename} not found.") 
        return None


def create_dataframe(df, columns, drop_duplicates=None):
    
    try: 
        if drop_duplicates:
            return df[columns].drop_duplicates(drop_duplicates)
        else:
            return df[columns]
        
    except KeyError as e: 
        print(f"Column {e} not found in DataFrame.") 
        return None


def generate_sql_create_table(df, column_mapping, table_name, primary_keys=None, foreign_keys=None):
    sql_script = f'CREATE TABLE {table_name} (\n'
    for column in df.columns:
        if column in column_mapping:
            sql_script += f'    {column_mapping[column]},\n'
            
    if primary_keys:
        sql_script += f'    PRIMARY KEY ({", ".join(primary_keys)}),\n'
        
    if foreign_keys:
        for fk in foreign_keys:
            sql_script += f'    FOREIGN KEY ({fk[0]}) REFERENCES {fk[1]} ({fk[2]}),\n'
            
    sql_script = sql_script.rstrip(',\n') + '\n);\n'

    for _, row in df.iterrows():
        values = ', '.join(f"'{str(i)}'" for i in row.values)
        sql_script += f"INSERT INTO {table_name} VALUES ({values});\n"

    with open(f'{table_name}_create_table.txt', 'w') as f:
        f.write(sql_script)
        

def main(): 
    df = read_csv_file('baseinicial')

    casos = create_dataframe(df, ['DR_NO', 'Crm Cd', 'LOCATION', 'Weapon Used Cd', 'Part 1-2', 'Premis Cd', 'Status', 'AREA'])
    estado = create_dataframe(df, ['Status', 'Status Desc'], 'Status')
    area = create_dataframe(df, ['AREA', 'AREA NAME'], 'AREA')
    crimen = create_dataframe(df, ['Crm Cd', 'Crm Cd Desc'], 'Crm Cd')
    arma = create_dataframe(df, ['Weapon Used Cd', 'Weapon Desc'], 'Weapon Used Cd')
    premisa = create_dataframe(df, ['Premis Cd', 'Premis Desc'], 'Premis Cd')
    delito = create_dataframe(df, ['Crm Cd', 'Crm Cd Desc'], 'Crm Cd')
    delito_asociado = create_dataframe(df, ['DR_NO', 'Crm Cd 1', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4'])
    victima = create_dataframe(df, ['DR_NO', 'Vict Age', 'Vict Sex', 'Vict Descent'])
    ubicacion = create_dataframe(df, ['DR_NO','LOCATION', 'Cross Street', 'LAT', 'LON'])
    fechas = create_dataframe(df, ['DR_NO','Date Rptd', 'DATE OCC', 'TIME OCC'])
    
        
    column_mapping = {
        'DR_NO': 'codigo_caso numeric(10) PRIMARY KEY',
        'Crm Cd': 'codigo_crimen numeric(10)',
        'Date Rprtd': 'fecha_reporte DATE',
        'DATE OCC': 'fecha_ocurrencia DATE',
        'TIME OCC': 'hora_ocurrencia TIME',
        'AREA': 'codigo_area numeric(10)',
        'AREA NAME': 'nombre_area character varying(50)',
        'Rpt Dist No': 'numero_distrito_reporte numeric(10)',
        'Part 1-2': 'codigo_delito char(10)',
        'Crm Cd': 'codigo_crimen numeric(10)',
        'Crm Cd Desc': 'descripcion_crimen character varying(100)',
        'Vict Age': 'edad_victima numeric(3)',
        'Vict Sex': 'genero_victima char(1)',
        'Vict Descent': 'ascendencia_victima character varying(255)',
        'Premis Cd': 'codigo_premisa numeric(10)',
        'Premis Desc': 'descripcion_premisa character varying(255)',
        'Weapon Used Cd': 'codigo_arma numeric(10)',
        'Weapon Desc': 'descripcion_arma character varying(255)',
        'Status': 'estado character(2)',
        'LOCATION': 'direccion character varying(255)',
        'Cross Street': 'calle character varying(255)',
        'LAT': 'latitud numeric(10, 8)',
        'LON': 'longitud numeric(11, 8)'
    }
    
    
    generate_sql_create_table(casos, column_mapping, 'Casos', ['codigo_caso'])
    generate_sql_create_table(estado, column_mapping, 'Estado', ['estado'])
    generate_sql_create_table(area, column_mapping, 'Area', ['codigo_area'])
    generate_sql_create_table(crimen, column_mapping, 'Crimen', ['codigo_crimen'])
    generate_sql_create_table(arma, column_mapping, 'Arma', ['codigo_arma '])
    generate_sql_create_table(premisa, column_mapping, 'Arma', ['codigo_premisa'])
    generate_sql_create_table(delito, column_mapping, 'Delito', ['codigo_crimen'])
    
    
    generate_sql_create_table(delito_asociado, column_mapping, 'Delitos Asociados', None, [['codigo_caso', 'Casos', 'codigo_caso']])
    generate_sql_create_table(victima, column_mapping, 'Victima', None, [['codigo_caso', 'Casos', 'codigo_caso']])    
    generate_sql_create_table(ubicacion, column_mapping, 'Ubicacion', None, [['codigo_caso', 'Casos', 'codigo_caso']])
    generate_sql_create_table(fechas, column_mapping, 'Fechas', None, [['codigo_caso', 'Casos', 'codigo_caso']])


    df = df[['DR_NO','Crm Cd 1', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4']]
    
    new_rows = []
    
    for index, row in df.iterrows():
        for col in ['Crm Cd 1', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4']:
            if not pd.isnull(row[col]):
                new_rows.append({'DR_NO': row['DR_NO'], 'Crm Cd': row[col]})
    
    new_df = pd.DataFrame(new_rows)
    sql_script = "CREATE TABLE Delitos_Asociados (\n    codigo_caso numeric(10),\n    crimen_asociado numeric(10),\n    FOREIGN KEY (codigo_caso) REFERENCES Casos(codigo_caso)\n);\n\n"
    
    for index, row in new_df.iterrows():
        sql_script += f"INSERT INTO Delitos_Asociados VALUES ('{row['DR_NO']}', '{row['Crm Cd']}');\n"
    
    with open('delitos_asociados_create_table.txt', 'w') as file:
        file.write(sql_script)


if __name__ == '__main__':
    main()
    
    
    
    
    