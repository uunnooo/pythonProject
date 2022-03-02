import pandas as pd
import pickle
import _Preprocessing_
import _ModifyResult_

pd.set_option('mode.chained_assignment',  None)

tmppath = 'D:\\uno\\unoDB\\'
tmppath2 = 'D:\\uno\\unoDB\\ResultDB\\'

tYear = 2017 # +1 year 부터 DB 불러옴
itemName = 'FT'

rawDBTotal = pd.DataFrame()
DBTotal = pd.DataFrame()
globals()[f'DB_{itemName}'] = pd.DataFrame()

tmp = _ModifyResult_.unoDB(pd.DataFrame(),'None')
## 연도별 데이터 처리
for i in range(0,4) :
    dateYear = tYear + i
    ## 연도별 DB 불러오기
#     globals()[f'DB_{dateYear+1}'] = \
#         pickle.load(open(tmppath2 + str(dateYear + 1) + '_ResultDB_' + itemName + '.pkl', 'rb'))
#     DBTotal = pd.concat([DBTotal, globals()[f'DB_{dateYear + 1}']])
# pickle.dump(DBTotal, open(tmppath2 + 'ResultDBTotal_'+itemName+'.pkl', 'wb'))
    ## 연도별 데이터를 하나의 DB로 만들어서 한번에 처리(연도별로 하면 중복되는 데이터가 존재한다)
    rawDB = pickle.load(open(tmppath + str(dateYear + 1) + '_pd' + itemName + '.pkl', 'rb'))
    print('Loading Complete')
    rRawDB = rawDB[tmp.PreInfor + tmp.SPECALL + tmp.RawResultFT]
    rawDBTotal = pd.concat([rawDBTotal, rRawDB])
pickle.dump(rawDBTotal, open(tmppath2 + 'RawDBTotal_' + itemName + '.pkl', 'wb'))
ResultDB = _Preprocessing_.fnMakeFlattracDB(rawDBTotal)
print('Analysis Complete')
pickle.dump(ResultDB, open(tmppath2 + 'ResultDBFull_' + itemName + '.pkl', 'wb'))

## 각 시험데이터 DB를 하나의 DB로
# a = DB_FT.DB
# b = DB_ST.DB
# c = DB_FS.DB
# commonColumns = a.columns[0:38]
# d = pd.merge(a, b, on = list(commonColumns), how =  'outer')
# e = pd.merge(d, c, on = list(commonColumns), how =  'outer')