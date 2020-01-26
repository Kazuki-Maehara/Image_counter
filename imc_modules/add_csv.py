#! /usr/bin/env python3
# coding = utf-8

import pandas as pd
from datetime import datetime

def add_csv(csv_dir, count):

    file_name = csv_dir + datetime.now().strftime('%Y%m%d') + '.csv'

    df = pd.DataFrame([], columns=['Time', 'No.'])

    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        print('File is not found, creat new file : ' + file_name)
        df.to_csv(file_name)
    else:
        print('File is opend : ' + file_name)

    c_time =  datetime.now().strftime('%X')

    df_temp = pd.DataFrame([[c_time, count]])

    df_temp.to_csv(file_name, index_label='index', encoding='utf-8', mode='a', header=False)

if __name__ == '__main__':
    add_csv()

