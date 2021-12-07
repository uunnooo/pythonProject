import pandas as pd
import numpy as np
import pickle
import re
import _DropDupliCol_
import MakeConditionDB

# pickle.dump(pdST, open(tmppath+'pdST.pkl', 'wb'))
# set a path for files saving data
tmppathTEST = 'D:\\uno\\unoDB\\Test\\'
tmppath = 'D:\\uno\\unoDB\\'
tmppath2 = 'D:\\uno\\unoDB\\FS\\'
tmppath3 = 'D:\\uno\\unoDB\\FS\\TC1\\'
tmppath4 = 'D:\\uno\\unoDB\\FS\\TC2\\'
tmppath5 = 'D:\\uno\\unoDB\\FS\\TC3\\'

pdFS = pd.DataFrame()  # Flattrac shape 정보 프레임
# 저장된 정보를 이용해서 프리 프로세싱 시작
pdFS = pickle.load(open(tmppath + 'pdST.pkl', 'rb'))

'''
Load Rate per에 의해 분할되어 있는 결과값들을 하나의 행으로 합쳐서 DB 생성
Load Rate Per에 대한 결과값들을 모두 처리(한개의 Foot shape 결과에는 항상 다중 하중 조건에 대한 결과들이 존재)
그외에 누락된 데이터 및 여러가지 기본 처리들은 사전에 처리
'''
# newtmpDF = MakeConditionDB.fnAddLoadRatePerConditionFSDB(pdFS, tmppath2)
rDF = pickle.load(open(tmppath2+'pdFSUno.pkl', 'rb')) # 저장되어 있는 데이터 사용

valList = ['REQ_NO', 'TIRE_NO', 'TEST_COND_NO', 'TEST_LOAD', 'LOAD_RATE_PER']

# 중복되어지는 Spec_NO list 생성
listduSN = rDF.loc[rDF['SPEC_NO'].duplicated(), 'SPEC_NO'].drop_duplicates()
# SPEC_NO가 중복되지 않은 DB 생성
newtmprDF = rDF.drop_duplicates('SPEC_NO').copy()
newtmprDF2 = newtmprDF[newtmprDF['SPEC_NO'].isin\
    (pd.Series(list(set(rDF['SPEC_NO']) - set(listduSN))))].copy()

# 중복된 DB를 처리 후 저장할 DataFrame 생성
newtmpDF = pd.DataFrame()



# 조건에 따라 결과들을 횡으로 연결, 연결된 결과 범위 설정
indStartResult = np.where(rDF.columns == 'AIR')[0][0]
indEndResult = len(rDF.columns)
rangeResult = range(indStartResult,indEndResult)
p = re.compile('^FILE|HINT') # 정규 표현식 사용(결과값이 있는 범위를 찾기 위해

# 중복 리스트를 이용해서 중복시의 조건들을 구분
for specNo in listduSN :
    tmpDF = rDF.loc[rDF['SPEC_NO'] == specNo].copy()
    flagCase = 0
    if len(tmpDF['REQ_NO'].drop_duplicates()) > 1 : flagCase += 1
    if len(tmpDF['TIRE_NO'].drop_duplicates()) > 1 : flagCase += 2
    if len(tmpDF['TEST_COND_NO'].drop_duplicates()) > 1: flagCase += 4
    if len(tmpDF['AIR'].drop_duplicates()) > 1 : flagCase += 8
    if len(tmpDF['TEST_LOAD'].drop_duplicates()) > 1 : flagCase += 16

    if not(flagCase & 0b11000) :
    # if flagCase == 0b00001 or flagCase == 0b00010 or flagCase == 0b00100 :
        # 시험 조건이 같은 경우는 최신값을 사용, 평균값을 사용하기에도 애매한 부분 있음
        # 동일 시점에 의뢰되어 같은 스펙의 여러개의 타이어를 이용해서 시험한 경우는 평균값 사용
        '''
        print('시험조건은 같고 REQ_NO, TIRE_NO, TEST_COND_NO 만 다른경우' + specNo)
        tmpDF.to_csv(tmppath3 + '_' + specNo + '.csv')
        
        if len(tmpDF.drop_duplicates('CONFIRM_DATE')) > 1 :
            # 평가한 시점이 다르다면 최신 데이터를 사용
            tmpDF1 = tmpDF.iloc[[tmpDF['CONFIRM_DATE'].argmax()],:].copy()
        else :
            # 평가한 시점이 같다면 평균값을 사용
        '''
    # 평가한 시점이 다르다면 최신 데이터만을 사용
        if len(tmpDF.drop_duplicates('CONFIRM_DATE')) > 1:
            # 최신 날짜에 해당하는 시험들만 DB로 생성(과거 데이터들까지 평균이 되는것을 방지 하기 위해)
            maxDate = tmpDF.iloc[[tmpDF['CONFIRM_DATE'].argmax()], np.where(tmpDF.columns == 'CONFIRM_DATE')[0][0]]
            tmpDF = tmpDF[tmpDF['CONFIRM_DATE'] == maxDate.iloc[0]].copy()
            # tmpResultVal = pd.DataFrame([p.findall(str) for str in tmpDF.columns[666:]]).isnull()
            # indResultVal = np.where(tmpResultVal)[0] + 666

        ## 모든 데이터는 평균값 사용(시점이 같다면 평균값을 사용)
        tmpResultVal = pd.DataFrame([p.findall(str) for str in tmpDF.columns[666:]]).isnull()
        indResultVal = np.where(tmpResultVal)[0] + 666
        tmpDF1 = tmpDF.drop_duplicates('SPEC_NO').copy()
        for colNum in indResultVal :
            tmpDF1[tmpDF.columns[colNum]] =\
                format(tmpDF[tmpDF.columns[colNum]].astype('float').mean(), '.2f')
            tmpDF1[tmpDF.columns[colNum]].astype('object')
    elif flagCase & 0b11000 :
        '''
        print('시험조건이 다른경우' + specNo)        
        tmpDF.to_csv(tmppath4 + '_' + specNo + '.csv')
        '''
        # 시험 조건이 다른 경우는 조건에 대해서
        tmpDF1 = tmpDF[0:1].copy()
        for i in range(len(tmpDF.drop_duplicates(['AIR', 'TEST_LOAD']))) :
            if i > 0 : # 첫번째 데이터 프레임을 기준으로 횡연결
                tmpAddDF = tmpDF.iloc[[i],indStartResult:]
                for ind in range(len(tmpAddDF.columns)) :
                    tmpAddDF.rename(columns = {tmpAddDF.columns[ind]: tmpAddDF.columns[ind] + '_' + str(i)},
                                    inplace = True)
                # index값 변경(추가된 열을 기존 DataFrame과 합치기 위해 Index 통일, concat는 index기준 추가)
                tmpAddDF.rename(index={tmpAddDF.index[0]: tmpDF.index[0]}, inplace = True)
                # 첫행기준으로 열 추가. 첫행 이외의 열은 수정 금지(조건이 3개 이상 있는 경우대비)
                tmpDF1 = pd.concat([tmpDF1, tmpAddDF], axis=1)
    else :
        print('어떤 경우 인거지?' + specNo)
        tmpDF.to_csv(tmppath5 + '_' + specNo + '.csv')

    newtmpDF = newtmpDF.append(tmpDF1)

newDF = pd.merge(newtmprDF2,newtmpDF, how='outer')
pickle.dump(newDF, open(tmppath + 'FSDB_F.pkl', 'wb'))

print('Done')





