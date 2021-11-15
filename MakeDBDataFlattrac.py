import pandas as pd
import pickle
import DuplicatedInColumns

# set a path for files saving data
tmppath = 'D:\\uno\\unoDB\\'
pdFT = pd.DataFrame()  # Flattrac shape 정보 프레임
# 저장된 정보를 이용해서 프리 프로세싱 시작
pdFT = pickle.load(open(tmppath+'pdFT.pkl', 'rb'))

## 중복되는 칼럼을 합치기
# 칼럼을 합치기 전에 합치게 될 기준열을 정하고 기준열에 없는 정보들은 다른열에 있는 값으로 채움
tmpFT1 = DuplicatedInColumns.fnEmptyRowReplace(pdFT, 0, 'SPEC_NO')
# 중복되는 칼럼들 제거(제거시 각 테이블별 없는 정보들이있어서 주의 필요)
tmpFT2 = DuplicatedInColumns.fnDuplicatedInColumns(tmpFT1,'first')
# CA가 없는 모든값 제거, CA가 없는 DB는 필요가 없다.
rCADF = tmpFT2.dropna(subset=['CA']).copy()

## SPEC_NO에 대해서 유일한 데이터 프레임 생성(DB를 이용시 기준은 SPEC_NO가 된다)
# SPEN_NO기존 중복 행 삭제(중복으로 인해 누락되는 데이터들은 아래에서 처리)
tmprSPDF = rCADF.drop_duplicates('SPEC_NO').copy()

### SPEC_NO에 대해 중복되어 누락되어 지는 데이터들 처리
## 같은 스펙번호를 가지는 행들 구분하기
# 중복 SPEC NO 뽑아 리스트로 만들기
listduSN = rCADF.loc[rCADF['SPEC_NO'].duplicated(), 'SPEC_NO'].drop_duplicates()

newtmprDF = rCADF.drop_duplicates('SPEC_NO').copy()
newtmprDF2 = newtmprDF[newtmprDF['SPEC_NO'].isin\
    (pd.Series(list(set(rCADF['SPEC_NO']) - set(listduSN))))].copy()

# 변경되어져야할 값을 저장할 DataFrame 생성
newtmpDF = pd.DataFrame()


# 중복 리스트를 이용해서 중복시의 조건들을 구분
for specNo in listduSN :
    tmpDF = rCADF.loc[rCADF['SPEC_NO'] == specNo].copy()
    flagCase = 0
    if len(tmpDF['REQ_NO'].drop_duplicates()) > 1 : flagCase += 1
    if len(tmpDF['TIRE_NO'].drop_duplicates()) > 1 : flagCase += 2
    if len(tmpDF['TEST_COND_NO'].drop_duplicates()) > 1: flagCase += 4
    if len(tmpDF['AIR'].drop_duplicates()) > 1 : flagCase = 8
    if len(tmpDF['LOAD_100'].drop_duplicates()) > 1 : flagCase = 16
 # 마스크 이용 조건 판별 후 각각의 조건에 맞는 데이터 처리(조건 판별 간결성)
    if not(flagCase & 0b11000) :
        if len(tmpDF.drop_duplicates('CONFIRM_DATE')) > 1 :
            # 평가한 시점이 다르다면 최신 데이터를 사용
            tmpDF = tmpDF.iloc[[tmpDF['CONFIRM_DATE'].argmax()],:].copy()
        else :
            #print('REQ_NO 다른 케이스')
            # REQ_NO가 다른 모든 케이스는 평균값 사용
            tmpCA = tmpDF['CA'].astype('float').mean() # 평균값 계산
            tmpDF.drop_duplicates(['SPEC_NO'], inplace=True) # 중복행 제거
            tmpDF['CA'] = format(tmpCA, '.2f') # 데이터 타입 Float으로 변경
            tmpDF['CA'].astype('object') # 기존 DataFrame 타입 유지

    elif flagCase & 0b11000:
        ## 위에서 REQ_NO가 다르고, TIRE_NO가 다른 케이스는 없어지고
        # REQ_NO, TIRE_NO 같고 공기압 or 하중 조건이 다른 케이스
        # 조건별로 행을 추가 하여 DataFrame 생성
        for i in range(len(tmpDF.drop_duplicates(['AIR', 'LOAD_100']))) :

            if i > 0 : # 첫번째 데이터 프레임을 기준으로 횡연결
                tmpAddDF = tmpDF.loc[[tmpDF.index[i]],['AIR','LOAD_100','CA']]

                for ind in range(len(tmpAddDF.columns)) :
                    tmpAddDF.rename(columns = {tmpAddDF.columns[ind]: tmpAddDF.columns[ind] + '_' + str(i)},
                                    inplace = True)

                # index값 변경(추가된 열을 기존 DataFrame과 합치기 위해 Index 통일, concat는 index기준 추가)
                tmpAddDF.rename(index={tmpAddDF.index[0]: tmpDF.index[0]}, inplace = True)
                # 첫행기준으로 열 추가. 첫행 이외의 열은 수정 금지(조건이 3개 이상 있는 경우대비)
                tmpDF = pd.concat([tmpDF, tmpAddDF], axis=1)

        # 하나의 행으로 합치기 위해 첫행 제외, 모든 행 삭제. 추후 Merge를 위해
        tmpDF.drop(tmpDF.index[1:], inplace = True)

    else :
        print('SPEC_NO 중복 분류 불가')
        break
    # 새로운 값들을 순차적으로 데이터 프레임으로 구성
    newtmpDF = newtmpDF.append(tmpDF)

## 이전 데이터 프레임에 새로운 데이터 프레임 업데이트
'''
 기존 데이터 프레임과 중복되는 값들을 새로운값들로 변경
Merge시 교집합 부분에 값들이 같지 않을시 추가 행 생성 후 결합. 추가행 생성 방지를 위해 같은
Spec에 대한 값들 통일 후 Merge 진행 필요
'''
# tmprSPDF에 있는 tmprSPDF와 newtmpDF의 교집합 값들을 newtmpDF의 값으로 변경
# tmprSPDF.update(newtmpDF)
# 추가 조건에 대한 값들을 열로 합침
newDF = pd.merge(newtmprDF2,newtmpDF, how='outer')
pickle.dump(newDF, open(tmppath + 'FTDB_F.pkl', 'wb'))
# 새로 생성된 값들을 비교 해보기 위한 DataFrame 생성 방법
#r = pd.merge(rCAdf[['SPEC_NO','CA']],newDF[['SPEC_NO','CA']], on = 'SPEC_NO')




