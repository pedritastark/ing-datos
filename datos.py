#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 09:32:29 2023

@author: sebastianpedraza
"""

import pandas as pd



df = pd.read_csv('baseinicial..csv')


def ct(df, args):
    primary_key = df[[x for x in args[:-1]]].drop_duplicates()
    df = primary_key.set_index(args[0])
    df.to_excel(args[-1])


ct(df, ('AREA', 'AREA NAME', 'Areas.xlsx' ))
ct(df,('Weapon Used Cd', 'Weapon Desc', 'Armas.xlsx' ))
ct(df,('LOCATION', 'Cross Street','LAT', 'LAT','Rpt Dist No', 'Ubicacion.xlsx' ))
ct(df, ('Status', 'Status Desc', 'Estado.xlsx'))
ct(df, ('Premis Cd','Premis Desc' ,'Premisa.xlsx'))
ct(df, ('Crm Cd','Crm Cd Desc','Delito.xlsx'))
