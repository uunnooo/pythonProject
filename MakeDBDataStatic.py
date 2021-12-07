import pandas as pd
import numpy as np
import pickle
import re
import _DropDupliCol_
import MakeConditionDB

# pickle.dump(pdST, open(tmppath+'pdST.pkl', 'wb'))
# set a path for files saving data
tmppath = 'D:\\uno\\unoDB\\'
tmppath2 = 'D:\\uno\\unoDB\\ST\\'
tmppath3 = 'D:\\uno\\unoDB\\ST\\TC1\\'
tmppath4 = 'D:\\uno\\unoDB\\ST\\TC2\\'
tmppath5 = 'D:\\uno\\unoDB\\ST\\TC3\\'

pdST = pd.DataFrame()  # Flattrac shape 정보 프레임
# 저장된 정보를 이용해서 프리 프로세싱 시작
pdST = pickle.load(open(tmppath + 'pdST.pkl', 'rb'))
pdST.to_csv(tmppath2+'pdST.csv')

## 중복되는 칼럼을 합치기
# 칼럼을 합치기 전에 합치게 될 기준열을 정하고 기준열에 없는 정보들은 다른열에 있는 값으로 채움
# tmpST1 = DuplicatedInColumns.fnEmptyRowReplace(pdST, 0, 'SPEC_NO')
# # 중복되는 칼럼들 제거(제거시 각 테이블별 없는 정보들이있어서 주의 필요)
# tmpST2 = DuplicatedInColumns.fnDuplicatedInColumns(tmpST1,'first')
# tmpST2.to_csv(tmppath2+'tmpST2.csv')

'''
Load Rate per에 의해 분할되어 있는 결과값들을 하나의 행으로 합쳐서 DB 생성
Load Rate Per에 대한 결과값들을 모두 처리(한개의 Foot shape x결과에는 항상 다중 하중 조건에 대한 결과들이 존재)
그외에 누락된 데이터 및 여러가지 기본 처리들은 사전에 처리
'''
# rDF = MakeConditionDB.fnAddMesrFlagConditionSTDB(pdST, tmppath2)
rDF = pickle.load(open(tmppath2+'pdSTUno.pkl', 'rb')) # 저장되어 있는 데이터 사용

'''
## 전처리
# 칼럼을 합치기 전에 합치게 될 기준열을 정하고 기준열에 없는 정보들은 다른열에 있는 값으로 채움
DF1 = DuplicatedInColumns.fnEmptyRowReplace(pdST, 0, 'SPEC_NO')
# 중복되는 칼럼들 제거(제거시 각 테이블별 없는 정보들이있어서 주의 필요)
DF2 = DuplicatedInColumns.fnDuplicatedInColumns(DF1, 'first')
# Static의 결과가 없는 모든값 제거, 결과가 없는 시험 데이터 제거
rDF1 = DF2.dropna(subset=['RESULT']).copy()
# Static의 결과가 0인값 제거, 결과가 없는것으로 판단
rDF2 = rDF1.drop(rDF1[rDF1['RESULT'] == 0].index).copy()
# Kv만 여러 하중조건으로 결과 측정, MESR_FLAG가 없는 값은 KV가 아님
rDF3 = rDF2.dropna(subset=['MESR_FLAG']).copy()
# MESR_FLAG가 0인값 제거, KV가 아니라고 판단
rDF4 = rDF3.drop(rDF3[rDF3['MESR_FLAG'] == 0].index).copy()
# AIR가 없거나 Load가 없는 데이터 제거, 시험조건이 없는 경우의 데이터는 사용 불가
rDF5 = rDF4.drop(rDF4[rDF4['TEST_LOAD'].isna() | rDF4['AIR'].isna()].index).copy()
'''

valList = ['REQ_NO', 'TIRE_NO', 'TEST_ITEM', 'TEST_LOAD', 'LOAD_RATE_PER']

# 중복되어지는 Spec_NO list 생성
listduSN = rDF.loc[rDF['SPEC_NO'].duplicated(), 'SPEC_NO'].drop_duplicates()
# SPEC_NO가 중복되지 않은 DB 생성
newtmprDF = rDF.drop_duplicates('SPEC_NO').copy()
newtmprDF2 = newtmprDF[newtmprDF['SPEC_NO'].isin\
    (pd.Series(list(set(rDF['SPEC_NO']) - set(listduSN))))].copy()

# 중복된 DB를 처리 후 저장할 DataFrame 생성
newtmpDF = pd.DataFrame()


# 조건에 따라 결과들을 횡으로 연결, 연결된 결과 범위 설정
indStartResult = np.where(rDF.columns == 'TEST_ITEM')[0][0]
indEndResult = len(rDF.columns)
rangeResult = range(indStartResult,indEndResult)

re1 = re.compile('RESULT') # 정규 표현식 사용(결과값이 있는 범위를 찾기 위해
re2 = re.compile('HINT') # 정규 표현식 사용(결과값이 있는 범위를 찾기 위해
re3 = re.compile('DATE') # 정규 표현식 사용(결과값이 있는 범위를 찾기 위해



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
        '''
        # 평가한 시점이 다르다면 최신 데이터만을 사용
        if len(tmpDF.drop_duplicates('CONFIRM_DATE')) > 1 :
            # 최신 날짜에 해당하는 시험들만 DB로 생성(과거 데이터들까지 평균이 되는것을 방지 하기 위해)
            maxDate = tmpDF.iloc[[tmpDF['CONFIRM_DATE'].argmax()], np.where(tmpDF.columns == 'CONFIRM_DATE')[0][0]]
            tmpDF = tmpDF[tmpDF['CONFIRM_DATE'] == maxDate.iloc[0]].copy()
        # tmpResultVal = pd.DataFrame([p.findall(str) for str in tmpDF.columns[666:]]).isnull()
        # indResultVal = np.where(tmpResultVal)[0] + 666

        ## 모든 데이터는 평균값 사용(시점이 같다면 평균값을 사용)
        ind1 = ~pd.DataFrame([re1.findall(str) for str in tmpDF.columns]).isnull()
        ind2 = ~pd.DataFrame([re2.findall(str) for str in tmpDF.columns]).isnull()
        ind3 = ~pd.DataFrame([re3.findall(str) for str in tmpDF.columns]).isnull()

        # 결과값들이 있는 열을 찾음(비교식)
        tmpResultVal = ind1 & ~(ind2 | ind3)
        indResultVal = np.where(tmpResultVal)[0]
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
pickle.dump(newDF, open(tmppath + 'STDB_F.pkl', 'wb'))

print('Done')





