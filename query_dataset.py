import pyodbc 
import json
from typing import List
import sql_utils
import numpy as np
import matplotlib.pyplot as plt



def column_to_array(column:List):
    arr = []
    for row in column:
        arr.append(row[0])
    return arr

print('Connecting to server...')
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=6S3S0J3;'
                      'DATABASE=rightmove;'
                      'Trusted_Connection=yes;')
print('Creating cursor...')
cursor = conn.cursor()

table_name  = 'properties'
column_name = 'price'
result: List = sql_utils.query_table(cursor, 'test', 'select_column', table_name, column_name)
bins = np.linspace(int(100000), int(2000000), 100000)
array = column_to_array(result)
hist, bin_edges = np.histogram(array, bins=bins)
