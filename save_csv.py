import pandas as pd 
import csv
import os


def save(imagePath, co_ordinate, reset=True):
    if ('points.csv' not in os.listdir(os.getcwd())) or reset:
        empty = pd.DataFrame(columns=['ImagePath'])
        empty.to_csv('points.csv', index=False)
    df = pd.read_csv('points.csv')
    d ={}
    for count, i in enumerate(co_ordinate):
        d['ImagePath'] = imagePath
        d[f'x{count}'] = i[0]
        d[f'y{count}'] = i[1]
    df = df.append(d, ignore_index=True)
    df.to_csv('points.csv', index=False)

    print('Points Uploaded!')