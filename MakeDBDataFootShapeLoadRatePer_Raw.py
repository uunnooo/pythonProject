import pandas as pd
import numpy as np
import pickle
import DuplicatedInColumns
import MakeConditionDB


# pickle.dump(pdFS, open(tmppath+'pdFS.pkl', 'wb'))
# set a path for files saving data
tmppath = 'D:\\uno\\unoDB\\'
tmppath2 = 'D:\\uno\\unoDB\\FS\\'
pdFS = pd.DataFrame()  # Flattrac shape 정보 프레임

# 저장된 정보를 이용해서 프리 프로세싱 시작
pdFS = pickle.load(open(tmppath + 'pdFS.pkl', 'rb'))


valList = ['SPEC_NO', 'REQ_NO', 'TIRE_NO', 'TEST_COND_NO', 'AIR', 'TEST_LOAD', 'LOAD_RATE_PER']

## 중복되는 칼럼을 합치기
# 칼럼을 합치기 전에 합치게 될 기준열을 정하고 기준열에 없는 정보들은 다른열에 있는 값으로 채움
tmpFS1 = DuplicatedInColumns.fnEmptyRowReplace(pdFS, 0, 'SPEC_NO')
# 중복되는 칼럼들 제거(제거시 각 테이블별 없는 정보들이있어서 주의 필요)
tmpFS2 = DuplicatedInColumns.fnDuplicatedInColumns(tmpFS1, 'first')

# CA가 없는 모든값 제거, CA가 없는 DB는 필요가 없다.
rCADF = tmpFS2.dropna(subset=['TOTAL_CONTACT_AREA']).copy()
# CA가 0인값 제거, 결과가 없는것으로 판단
rCADF = rCADF.drop(rCADF[tmpFS2['TOTAL_CONTACT_AREA'] == 0].index).copy()
# CA가 0인값 제거, 결과가 없는것으로 판단
rCADF = rCADF.drop(rCADF[rCADF['LOAD_KG'].isna() | rCADF['AIR'].isna()].index).copy()



## SPEC_NO에 대해서 유일한 데이터 프레임 생성(DB를 이용시 기준은 SPEC_NO가 된다)
# SPEN_NO기존 중복 행 삭제(중복으로 인해 누락되는 데이터들은 아래에서 처리)
#기준이 LOAD_RATE_PER 100을 기준 데이터로 사용
tmpFS3 = rCADF[rCADF['LOAD_RATE_PER'] == 100].copy()
tmprSPDF = tmpFS3.drop_duplicates('SPEC_NO').copy()

### SPEC_NO에 대해 중복되어 누락되어 지는 데이터들 처리
## 같은 스펙번호를 가지는 행들 구분하기
# 중복 SPEC NO 뽑아 리스트로 만들기
listduSN = rCADF.loc[rCADF['SPEC_NO'].duplicated(), 'SPEC_NO'].drop_duplicates()

# 변경되어져야할 값을 저장할 DataFrame 생성
newtmpDF = pd.DataFrame()

# 조건에 따라 결과들을 횡으로 연결, 연결될 결과 범위 설정
indStartResult = np.where(tmprSPDF.columns == 'LOAD_KG')[0][0]
indEndResult = len(tmprSPDF.columns)
rangeResult = range(indStartResult,indEndResult)


# 중복 리스트를 이용해서 중복시의 조건들을 구분
for specNo in listduSN :
    flagCase = 0
    tmpDF = rCADF.loc[rCADF['SPEC_NO'] == specNo].copy()
    listduRN = tmpDF.loc[tmpDF['REQ_NO'].duplicated(), 'REQ_NO'].drop_duplicates()
    for reqNo in listduRN :
        tmpDFReq = tmpDF[tmpDF['REQ_NO'] == reqNo].copy()
        listduTN = tmpDFReq.loc[tmpDFReq['TIRE_NO'].duplicated(), 'TIRE_NO']\
            .drop_duplicates().sort_values()
        for tireNo in listduTN :
            tmpDFTire = tmpDFReq[tmpDFReq['TIRE_NO'] == tireNo].copy()
            listduCN = tmpDFTire.loc[tmpDFTire['TEST_COND_NO'].duplicated(), 'TEST_COND_NO']\
                .drop_duplicates().sort_values()
            tmpDF2 = pd.DataFrame()
            for condNo in listduCN :
                tmpDFCond1 = tmpDFTire[tmpDFTire['TEST_COND_NO'] == condNo].copy()
                # 무슨 오류인지 모르는데 같은 데이터가 중복으로 들어간 경우가 있다. 완전 중북된 데이터는 날려버리자
                tmpDFCond2 = tmpDFCond1.drop_duplicates('LOAD_RATE_PER').copy()
                tmpDF1 = MakeConditionDB.fnAddConditionTestDB(tmpDFCond2, 'LOAD_RATE_PER', rangeResult, 100)
                # if tmpDF1.index == 6384 :
                #     print('check')
                newtmpDF = newtmpDF.append(tmpDF1)
                print(tmpDF1[valList])
# print(newtmpDF[valList])

pickle.dump(newtmpDF, open(tmppath2+'pdFSUno.pkl', 'wb'))
print('Complete')




