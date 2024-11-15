import requests
import numpy as np
import pandas as pd
import urllib
import os
# import sqlalchemy
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
from urllib import parse
import pymysql

# user = 'team4'
# password = 'Encore_team4@'
# host='192.168.0.95'
# port = 3306
# database = 'team4'
# password = parse.quote_plus(password)

def insert_repair_shop():
    con = pymysql.connect(host='192.168.0.95', user='team4', passwd='', port=3306, database='team4')
    cursor = con.cursor()
    sql = "insert into car_repair_shop (brand, region, high_voltage) values (%s, %s, %s)"
    for x in os.listdir('./data'):
        if x.endswith(".csv"):        
            print(x)
            df = pd.read_csv(f'./data/{x}')
            print(df.head())
            
            for idx, row in df.iterrows():
                print(row['LIST_ENTRPS'], row['LIST_REGION'], row['high_voltage'])
                cursor.execute(sql, [row['LIST_ENTRPS'], row['LIST_REGION'] , row['high_voltage']])        

    con.commit()

def insert_elec_car():
    con = pymysql.connect(host='192.168.0.95', user='team4', passwd='Encore_team4@', port=3306, database='team4')
    cursor = con.cursor()
    sql = "insert into nation_elec_car (region, reg_cnt) values (%s, %s)"
    for x in os.listdir('./data'):
        if x.endswith("electric_car.csv"):        
            print(x)
            df = pd.read_csv(f'./data/{x}')
            # print(df.head())
            for col in df.columns:
                print(col, df[col].values[0])
                cursor.execute(sql, [col, df[col].values[0]]) 

    con.commit()

# insert_elec_car()

def insert_charger_car():
    con = pymysql.connect(host='192.168.0.95', user='team4', passwd='Encore_team4@', port=3306, database='team4')
    cursor = con.cursor()
    sql = "insert into nation_elec_car_charger (region, cnt) values (%s, %s)"
    for x in os.listdir('./data'):
        if x.endswith("charge_car.csv"):        
            print(x)
            df = pd.read_csv(f'./data/{x}')
            print(df.head())
            for col in df.columns:
                print(col, df[col].values[0])
                cursor.execute(sql, [col, df[col].values[0]]) 

    con.commit()

# insert_charger_car()
