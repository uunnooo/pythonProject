import pandas as pd
import numpy as np
import pickle
import _DropDupliCol_
import os


# temporary folder to avoid secure permission
# tmppath = 'D:\\workroom\\p_workroom\\_DATA_Traing\\'
# 'D:\\workroom\\p_workroom\\_DATA_Traing\\'

tmppath = 'D:\\uno\\unoDB\\'

# Import Oracle DB Package
import cx_Oracle
# Credentials
import _AuthConfig as auth

# def fnCompareColumns(df1, df2, df3):
#     TmpIndex1 = []
#     TmpIndex2 = []
#     TmpIndex3 = []
#     for i in range(0, len(df1.columns)) :
#         for j in range(0, len(df2.columns)) :
#             for k in range(0, len(df3.columns)):
#                 if df1.columns[i] == df2.columns[j] == df3.columns[k]:
#                     TmpIndex1.append(i)
#                     TmpIndex2.append(j)
#                     TmpIndex3.append(k)
#
#     return TmpIndex1, TmpIndex2, TmpIndex3

pdFS = pd.DataFrame()  # Foot shape 정보 프레임
pdST = pd.DataFrame()  # Static 정보 프레임
pdFT = pd.DataFrame()  # Flattrac shape 정보 프레임


pdFS = pickle.load(open(tmppath+'pdST.pkl', 'rb'))
pdST = pickle.load(open(tmppath+'pdST.pkl', 'rb'))
pdFT = pickle.load(open(tmppath+'pdST.pkl', 'rb'))

'''
pdST.head(100).to_csv(tmppath+'RAWFS.csv')
pdST.head(100).to_csv(tmppath+'RAWFT.csv')
pdST.head(100).to_csv(tmppath+'RAWST.csv')
'''
'''
# 비교 해서 check는 해보지만 너무 오래 걸림
# DB 테이블의 결과값들에 대한 부분외에는 다 동일하다고 보고 진행함함
result1, result2, result3 = fnCompareColumns(pdST, pdST, pdST)

result = list(set(result1) | set(result2) | set(result3))
result.sort()
colIndexFS = list(range(0 , len(pdST.columns)))
colIndexST = list(range(0 , len(pdST.columns)))
colIndexFT = list(range(0 , len(pdST.columns)))
resultFS = list(set(colIndexFS) - set(result))
resultST = list(set(colIndexST) - set(result))
resultFT = list(set(colIndexFT) - set(result))
print("result " , result)
'''
# Spec No에 대한 정보 합치기
tmpFS1 = _DropDupliCol_.fnEmptyRowReplace(pdFS, 0, 'SPEC_NO')
tmpFT1 = _DropDupliCol_.fnEmptyRowReplace(pdFT, 0, 'SPEC_NO')
tmpST1 = _DropDupliCol_.fnEmptyRowReplace(pdST, 0, 'SPEC_NO')

'''
tmpFS1.head(100).to_csv(tmppath+'DBFS1.csv')
tmpFS1.head(100).to_csv(tmppath+'DBFT1.csv')
tmpST1.head(100).to_csv(tmppath+'DBST1.csv')
'''
# 중복되는 Column 제거
tmpFS2 = _DropDupliCol_.fnDuplicatedInColumns(tmpFS1, 'first')
tmpFT2 = _DropDupliCol_.fnDuplicatedInColumns(tmpFT1, 'first')
tmpST2 = _DropDupliCol_.fnDuplicatedInColumns(tmpST1, 'first')

# print(pdST.columns[687:706])
# 용량이 문제인지 파일이 제대로 만들어지지 않는다
# tmpST.to_excel('D:\\workroom\\p_workroom\\_DATA_Traing\\DBST.xlsx',
#                sheet_name = 'Sheet1', na_rep = 'NaN',
#                header = True,
#                #columns = ["group", "value_1", "value_2"], # if header is False
#                index = True, index_label = "No", startrow = 1, startcol = 1,
#                #engine = 'xlsxwriter',
#                freeze_panes = (2, 0))
'''
tmpFS2.head(100).to_csv(tmppath+'DBFS2.csv')
# tmpFS2.head(100).to_csv(tmppath+'DBFT2.csv')
# tmpFS2.to_csv(tmppath+'DBFT2.csv')
tmpST2.head(100).to_csv(tmppath+'DBST2.csv')
'''

df = tmpFT2.copy()
# CA의 값이 없는 행 삭제
rCADF = df.dropna(subset=['CA']) # CA가 없는 모든값 제거, CA가 없는 DB는 필요가 없다.
tmprSPDF = rCADF.drop_duplicates('SPEC_NO').copy() # 셀을 합치기 위해 스펙넘버가 중보되는 모든 값을 제가. SPEN_NO에 대한 유일 데이터 프레임


## 같은 스펙번호를 가지는 행들 구분하기

# listduSN = rCADF.loc[rCADF['SPEC_NO'].duplicated(),'SPEC_NO'] # 중복 SPEC NO 뽑아 내기 여기에 여러개의 중복 값들은 가지는 SPEC NO중복 만큼 들어가 있게됨
listduSN = rCADF.loc[rCADF['SPEC_NO'].duplicated(), 'SPEC_NO'].drop_duplicates()
# for문을 만들어서 같은 스펙으로 묶여 있는 데이터 리스트들을 처리해 준다.

# 변경된 값을 저장할 DataFrame 생성
newtmpDF = pd.DataFrame()

# Spec넘버를 기준으로 같은 Spec을 갖고 있는 행들을 찾고 각각의 행들의 조건을 이용하요
#중복된 값들을 처리

for specNo in listduSN :
    tmpDF = rCADF.loc[rCADF['SPEC_NO'] == specNo].copy()
    flagCase = 0
    if len(tmpDF['REQ_NO'].drop_duplicates()) > 1 : flagCase += 1
    if len(tmpDF['TIRE_NO'].drop_duplicates()) > 1 : flagCase += 2
    if len(tmpDF['AIR'].drop_duplicates()) > 1 : flagCase = 4
    if len(tmpDF['LOAD_100'].drop_duplicates()) > 1 : flagCase = 8

 # 조건에 판별이 너무 복잡해 마스크 이용 코딩
    if flagCase & 0b0001 :
        print('REQ_NO 다른 케이스')
        # 위에서 REQ_NO가 다른 모든 케이스
        tmpCA = tmpDF['CA'].astype('float').mean()
        tmpDF.drop_duplicates(['SPEC_NO'], inplace=True) # SPEC_NO으로 수정 원래 REQ_NO
        tmpDF['CA'] = format(tmpCA, '.2f')
        tmpDF['CA'].astype('object')

    elif flagCase & 0b0010 :
        # print('TIRE_NO 다른 케이스')
        # 위에서 REQ_NO가 다른 경우는 없어지고 REQ_NO는 같고 TIRE_NO가 다른 모든 케이스. 여기에는 TIRE_NO가 다르고 조건이 다른 경우도 포함
        # 여기에는 TIRE_NO만 다른 케이스와 조건이 다른 케이스에 대한 if필요
        if flagCase & 0b1100 :
            print('TIRE NO 다르고 공기압 혹은 하중조건이 다른 케이스')
            # TIRE_NO가 다르고 공기압 or 하중조건이 다른 케이스
            # pd.concat([tmpDF[i - 1:i], tmpDF.loc[tmpDF.index[i], ['AIR', 'LOAD_100', 'CA']]], axis=1) 수정중
            b = tmpDF.loc[[tmpDF.index[1]], ['AIR', 'LOAD_100', 'CA']]

        else :
            print('TIRE NO 만 다른 케이스')
            # 공기압 and 하중조건이 같고 TIRE_NO만 다른 케이스
            tmpCA = tmpDF['CA'].astype('float').mean()
            tmpDF.drop_duplicates(['AIR', 'LOAD_100'], inplace = True)
            tmpDF['CA'] = format(tmpCA, '.2f')
            tmpDF['CA'].astype('object')

    elif flagCase | 0b1100 :
        # 위에서 REQ_NO가 다르고, TIRE_NO가 다른 케이스는 없어지고, REQ_NO, TIRE_NO같고 공기압 or 하중 정보가 다른 케이스
        # SPEC_NO, REQ_NO 같고 조건이 다른 케이스, 조건을 다르게 해서 시험한 경우 조건과 결과값을 추가
        print('조건이 다른 케이스')

        for i in range(len(tmpDF.drop_duplicates(['AIR', 'LOAD_100']))) :

            if i > 0 : # 첫번째 데이터 프레임을 기준으로 횡연결
                tmpAddDF = tmpDF.loc[[tmpDF.index[i]],['AIR','LOAD_100','CA']]

                for ind in range(len(tmpAddDF.columns)) :
                    tmpAddDF.rename(columns = {tmpAddDF.columns[ind]: tmpAddDF.columns[ind] + '_' + str(i)},
                                    inplace = True)

                # tmpDF.drop(tmpDF.index[i], inplace = True) # 하나의 행으로 합치기 위해 칼럼으로 만든 열 삭제
                tmpAddDF.rename(index={tmpAddDF.index[0]: tmpDF.index[0]}, inplace = True)  # 기존 DF와 합치기 위해 index 값을 합쳐질 열번호로 변경
                tmpDF = pd.concat([tmpDF, tmpAddDF], axis=1)  # 새로운 값이 들어 있는 데이터 프레임,
                # 계속적으로 첫행에 붙인다. 첫행을 제외한 나머지 데이터들은 건들이지 않는다. 조건이 3개 이상 있는 경우를 위해

        tmpDF.drop(tmpDF.index[1:], inplace = True) # 하나의 행으로 합치기 위해 첫행을 제외한 모든 임시 데이터 프레임 삭제

    else :
        print('무슨 조건인지 모르는 케이스')

    print(specNo)
    print('--' * 10)

    newtmpDF = pd.concat([newtmpDF, tmpDF], axis=0) # 새로운 값이 들어 있는 데이터 프레임

    ## 이전 데이터 프레임에 새로운 데이터 프레임 업데이트(for문 돌때마다)
    # tmprSPDF[tmpDF.index[0]:tmpDF.index[0] + 1] = tmpDF

## 이전 데이터 프레임에 새로운 데이터 프레임 업데이트
tmprSPDF.update(newtmpDF) # 기존 데이터 프레임과 같은 값을 평균값으로 바꿈(있는 값만 최신값으로 바꿈)
                          # Merge 할때 다른 값들이 있으면 추가 행이 생기면서 합쳐짐. 추가행 방지를 위해 같은 Spec에 대한 값들을
                          #업데이트 하고 Merge 진행 필요
newDF = pd.merge(tmprSPDF,newtmpDF, how='outer') # 추가 조건에 대한 값들을 열로 합침
# 값을 비교 해보기 위한 DataFrame 생성
#r = pd.merge(rCAdf[['SPEC_NO','CA']],newDF[['SPEC_NO','CA']], on = 'SPEC_NO')
print('end')



