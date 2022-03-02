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
# tmp1 = tmp.PreInfor + tmp.SPECALL + ['PATTERN']
tmp1 = tmp.PreInfor + tmp.SPECALL
## Static result columns
# tmp2 = ['REQ_NO', 'REQ_REVISION', 'TEST_NO', 'TIRE_NO', 'TEST_COND_NO', 'TEST_ITEM', 'STEP_RATE', 'MESR_FLAG',
#         'DISPLACE', 'LOAD', 'RESULT', 'GLOBAL_RESULT', 'GLOBAL_CONVERSION']

## Footshape result columns
# tmp2 = ['REQ_NO', 'REQ_REVISION', 'TEST_NO', 'TIRE_NO', 'TEST_COND_NO', 'TEST_COND_CODE', 'SPEC_SEQ', 'ITEM_SEQ',
#         'LOAD_KG', 'LOAD_RATE_PER', 'CONTACT_LENGTH_MM_MAX', 'CONTACT_LENGTH_MM_CENTER', 'CONTACT_LENGTH_MM_25',
#         'CONTACT_LENGTH_MM_75', 'CONTACT_WIDTH_MM_MAX', 'CONTACT_WIDTH_MM_CENTER', 'CONTACT_WIDTH_MM_25',
#         'CONTACT_WIDTH_MM_75', 'SQUARE_RATIO', 'CONTACT_RATIO', 'ROUNDNESS', 'ACTUAL_CONTACT_AREA',
#         'TOTAL_CONTACT_AREA', 'FILEPATH', 'FILENAME', 'HINT_DETAIL_OBJ_ID']

## Flattrac result columns
tmp2 = ['REQ_NO', 'REQ_REVISION', 'TEST_NO', 'TIRE_NO', 'TEST_COND_NO', 'TEST_COND_CODE', 'CA', 'CAT', 'PRAT',
        'LOAD_N', 'REF_INFLATION', 'CA_COEF_A', 'CA_COEF_B', 'CA_COEF_C', 'LM_COEF_A', 'LM_COEF_B', 'LM_COEF_C',
        'LOCAL_PRAT', 'GLOBAL_PRAT']

tmp3 = tmp1 + tmp2

## 연도별 데이터 처리
for i in range(0,4) :
    dateYear = tYear + i
    QueryStartdate = f"{dateYear}-12-31"
    QueryEnddate = f"{dateYear+2}-1-1"
    ##연도별 RawDB 저장
    # DF = Query.fnQuery(QueryStartdate,QueryEnddate,itemName)
    # DF.to_csv(tmppath + str(dateYear+1) + '_' + itemName + '.csv')
    # print(i, dateYear+1)
    # pickle.dump(DF, open(tmppath + str(dateYear+1) + '_pd' + itemName + '.pkl', 'wb'))
    '''
    ## Foot shape 연도별 저장된 데이터 불러와서 데이터 처리
    rawDBFS = pickle.load(open(tmppath + str(dateYear+1) + '_pd' + itemName + '.pkl', 'rb'))
    print('Loading Complete')
    ResultDB = _Preprocessing_.fnMakeFlattracDB(rawDBFS)
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
    ## 연도별 데이터를 하나의 DB로 만들어서 한번에 처리(연도별로 하면 중복되는 데이터가 존재한다)
    rawDB = pickle.load(open(tmppath + str(dateYear + 1) + '_pd' + itemName + '.pkl', 'rb'))
    # rawDB = pickle.load(open(tmppath2 + 'rRawDBTotal_ST.pkl', 'rb'))
    print('Loading Complete')
    rRawDB = rawDB[tmp3]
    rawDBTotal = pd.concat([rawDBTotal, rRawDB])
pickle.dump(rawDBTotal, open(tmppath2 + 'RawDBTotal_' + itemName + '.pkl', 'wb'))
ResultDB = _Preprocessing_.fnMakeFlattracDB(rawDBTotal)
print('Analysis Complete')
pickle.dump(ResultDB, open(tmppath2 + 'ResultDBFull_' + itemName + '.pkl', 'wb'))


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

