import pandas as pd
import numpy as np
import pickle
import re
import _DropDupliCol_
import MakeConditionDB
import _MakeQuery_ as Query
import datetime
import MakeDB

pd.set_option('mode.chained_assignment',  None)

tmppath = 'D:\\uno\\unoDB\\'
tmppath2 = 'D:\\uno\\unoDB\\ResultDB\\'


tYear = 2017 # +1 year 부터 DB 불러옴
itemName = 'FT'

rawDBTotal = pd.DataFrame()
DBTotal = pd.DataFrame()
globals()[f'DB_{itemName}'] = pd.DataFrame()


## 연도별 데이터 처리
for i in range(0,4) :
    dateYear = tYear + i
    QueryStartdate = f"{dateYear}-12-31"
    QueryEnddate = f"{dateYear+2}-1-1"
    '''
    ##연도별 RawDB 저장
    DF = Query.fnQuery(QueryStartdate,QueryEnddate,itemName)
    DF.to_csv(tmppath + str(dateYear+1) + '_' + itemName + '.csv')
    print(i, dateYear+1)
    pickle.dump(DF, open(tmppath + str(dateYear+1) + '_pd' + itemName + '.pkl', 'wb'))
    '''

    '''
    ## Foot shape 연도별 저장된 데이터 불러와서 데이터 처리
    rawDBFS = pickle.load(open(tmppath + str(dateYear+1) + '_pd' + itemName + '.pkl', 'rb'))
    print('Loading Complete')
    ResultDB = MakeDB.fnMakeFootshapeDB(rawDBFS)
    print('Analysis Complete')
    pickle.dump(ResultDB, open(tmppath2 + str(dateYear+1) + '_ResultDB_' + itemName + '.pkl', 'wb'))
    '''

    '''
    ## Static 연도별 저장된 데이터 불러와서 데이터 처리
    rawDBST = pickle.load(open(tmppath + str(dateYear + 1) + '_pd' + itemName + '.pkl', 'rb'))
    print('Loading Complete')
    ResultDB = MakeDB.fnMakeStaticDB(rawDBST)
    print('Analysis Complete')
    pickle.dump(ResultDB, open(tmppath2 + str(dateYear + 1) + '_ResultDB_' + itemName + '.pkl', 'wb'))
    '''

    '''
    ## Flatrac 연도별 저장된 데이터 불러와서 데이터 처리
    rawDBFT = pickle.load(open(tmppath + str(dateYear + 1) + '_pd' + itemName + '.pkl', 'rb'))
    print('Loading Complete')
    ResultDB = MakeDB.fnMakeFlattracDB(rawDBFT)
    print('Analysis Complete')
    pickle.dump(ResultDB, open(tmppath2 + str(dateYear + 1) + '_ResultDB_' + itemName + '.pkl', 'wb'))
    '''

    ## Flatrac 연도별 저장된 데이터 불러와서 한번에 데이터 처리(연도별로 하면 중복되는 데이터가 존재한다)

    rawDB = pickle.load(open(tmppath + str(dateYear + 1) + '_pd' + itemName + '.pkl', 'rb'))
    print('Loading Complete')
    rawDBTotal = pd.concat([rawDBTotal, rawDB])

ResultDB = MakeDB.fnMakeFlattracDB(rawDBTotal)
print('Analysis Complete')
pickle.dump(ResultDB, open(tmppath2 + 'ResultDBTotal_' + itemName + '.pkl', 'wb'))

'''
    ## 연도별 DB 불러오기
    globals()[f'DB_{dateYear+1}'] = \
        pickle.load(open(tmppath2 + str(dateYear + 1) + '_ResultDB_' + itemName + '.pkl', 'rb'))
    DBTotal = pd.concat([DBTotal, globals()[f'DB_{dateYear + 1}']])
pickle.dump(DBTotal, open(tmppath2 + 'ResultDBTotal_'+itemName+'.pkl', 'wb'))
'''

# listduSN = globals()[f'DB_{itemName}'].loc[globals()[f'DB_{itemName}']['SPEC_NO'].duplicated(), 'SPEC_NO'].drop_duplicates()

    

## Footshape 시험 테스트
# rawDBFS = pickle.load(open(tmppath + '2021_pdFS.pkl', 'rb'))
# rawDBFS = pickle.load(open(tmppath + 'TestDBFS2.pkl', 'rb'))
# # rawDBFS = rawDBFS[rawDBFS.iloc[:,1] == 'KPKT1018918S00005'].copy()
# # rawDBFS.to_csv('D:\\uno\\unoDB\\Test\\raw_KPKT1018918S00005.csv')
#
# ResultDBFS = MakeDB.fnMakeFootshapeDB(rawDBFS)

## Static 시험 테스트
# rawDBST = pickle.load(open(tmppath + '2018_pdST.pkl', 'rb'))
# rawDBST = rawDBST[rawDBST.iloc[:,1] == 'KPKT1016073V00000'].copy()
# DSKT1024183S00003
# rawDBFS = pickle.load(open(tmppath + 'TestDBFS2.pkl', 'rb'))
# rawDBFS = rawDBFS[rawDBFS.iloc[:,1] == 'KPKT1018918S00005'].copy()
# rawDBFS.to_csv('D:\\uno\\unoDB\\Test\\raw_KPKT1018918S00005.csv')

# ResultDBST = MakeDB.fnMakeStaticDB(rawDBST)


print('Done')

