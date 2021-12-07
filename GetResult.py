import pandas as pd
import numpy as np
import pickle
import re
import _DropDupliCol_
import MakeConditionDB
import _MakeQuery_ as Query
import datetime

tmppath = 'D:\\uno\\unoDB\\'
tYear = 2017
itemName = 'FS'


for i in range(0,4) :
    dateYear = tYear + i
    QueryStartdate = f"{dateYear}-12-31"
    QueryEnddate = f"{dateYear+2}-1-1"
    DF = Query.fnQuery(QueryStartdate,QueryEnddate,itemName)

    DF.to_csv(tmppath + str(dateYear+1) + '_' + itemName + '.csv')
    print(i, dateYear+1)
    pickle.dump(DF, open(tmppath + str(dateYear+1) + '_pd' + itemName + '.pkl', 'wb'))




# f = open(tmppath+'pdFS.pkl', 'wb')
# DBFS = pickle.load(open(tmppath + 'pdFS.pkl', 'rb'))

# DBFS = pickle.load(open(tmppath + 'FSDB_F.pkl', 'rb'))
# DBFT = pickle.load(open(tmppath + 'FTDB_F.pkl', 'rb'))
# DBST = pickle.load(open(tmppath + 'STDB_F.pkl', 'rb'))
#
#
# re1 = re.compile('RESULT') # 정규 표현식 사용(결과값이 있는 범위를 찾기 위해
# re2 = re.compile('HINT') # 정규 표현식 사용(결과값이 있는 범위를 찾기 위해
# re3 = re.compile('DATE') # 정규 표현식 사용(결과값이 있는 범위를 찾기 위해
#
# ind1 = ~pd.DataFrame([re1.findall(str) for str in tmpDF.columns]).isnull()