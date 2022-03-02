import pandas as pd
import numpy as np
import pickle
import re
import _ModifyResult_
import sys
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go

tmppath = 'D:\\uno\\unoDB\\'
tmppath2 = 'D:\\uno\\unoDB\\ResultDB\\'
tmppath3 = 'D:\\uno\\unoDB\\FinalDB\\'

listTestItem = ['FT', 'ST', 'FS']
listTireSpec = ['TireInfor', 'CMP', 'CCS', 'BT1', 'BT2', 'JLC', 'BF', 'PCI', 'ETC', 'SPECALL']

DB_FT = pickle.load(open(tmppath3 + 'DBF_FT' + '.pkl', 'rb'))
DB_FS = pickle.load(open(tmppath3 + 'DBF_FS' + '.pkl', 'rb'))
DB_ST = pickle.load(open(tmppath3 + 'DBF_ST' + '.pkl', 'rb'))

# 각 시험데이터 DB를 하나의 DB로
a = DB_FT.DB
b = DB_ST.DB
c = DB_FS.DB
commonColumns = a.columns[0:38]
d = pd.merge(a, b, on = list(commonColumns), how =  'outer')
e = pd.merge(d, c, on = list(commonColumns), how =  'outer')

print(e.head)