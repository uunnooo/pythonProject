import pandas as pd
import numpy as np
import pickle
import _DropDupliCol_
import MakeConditionDB

# pickle.dump(pdST, open(tmppath+'pdST.pkl', 'wb'))
# set a path for files saving data
tmppath = 'D:\\uno\\unoDB\\'
tmppath2 = 'D:\\uno\\unoDB\\FS\\'
pdFS = pd.DataFrame()  # Flattrac shape 정보 프레임

# 저장된 정보를 이용해서 프리 프로세싱 시작
pdFS = pickle.load(open(tmppath + 'pdST.pkl', 'rb'))
# Load Rate Per에 대한 결과값들을 모두 처리(한개의 Foot shape 결과에는 항상 다중 하중 조건에 대한 결과들이 존재)
# newtmpDF = MakeConditionDB.fnAddLoadRatePerConditionFSDB(pdST, tmppath2)
newtmpDF = pickle.load(open(tmppath2+'pdFSUno.pkl', 'rb'))
print(newtmpDF)



valList = ['SPEC_NO', 'REQ_NO', 'TIRE_NO', 'TEST_COND_NO', 'AIR', 'TEST_LOAD', 'LOAD_RATE_PER']

