def fnMakeFootshapeDB(raw_df) :
    
    import pandas as pd
    import numpy as np
    import re
    import x_MakeConditionDB

    r = re.compile('CONTACT|SQUARE|ROUNDNESS')  # 정규 표현식 사용(결과값이 있는 범위를 찾기 위해

    ## Load rate per 조건에 대한 값들 처리(같은 시험에 해당하는 Load rate per를 하나의 행으로)
    rDF = x_MakeConditionDB.fnAddLoadRatePerConditionFSDB(raw_df)
    listduSN = rDF.loc[rDF['SPEC_NO'].duplicated(), 'SPEC_NO'].drop_duplicates() # 중복 Spec_NO list 생성
    # listduSN = 'CPKT1029296X00001'

    newtmprDF = rDF.drop_duplicates('SPEC_NO').copy()
    ## SPEC_NO가 중복되지 않은 DB 생성
    newtmprDF2 = newtmprDF[newtmprDF['SPEC_NO'].isin \
        (pd.Series(list(set(rDF['SPEC_NO']) - set(listduSN))))].copy()
    newtmpDF = pd.DataFrame() # 중복된 DB를 처리 후 저장할 DataFrame 생성
    indStartResult = np.where(rDF.columns == 'AIR')[0][0] # 조건에 따라 결과들을 횡으로 연결, 연결된 결과 범위 설정

    ## 중복 리스트를 이용해서 중복시의 조건들을 구분
    totalCount = len(listduSN)
    count = 0
    for specNo in listduSN:
        count += 1
        tmpDF = rDF.loc[rDF['SPEC_NO'] == specNo].copy()
        # 하나의 스펙번호를 기준으로 시험 컨디션 조건(공기압, 시험기준 하중)에 대해서 데이터 처리
        tmprCondDF = x_MakeConditionDB.fnMakeTestConditionDB(tmpDF, r, indStartResult)
        newtmpDF = newtmpDF.append(tmprCondDF)
        print(str(count) + ' of ' + str(totalCount))
    ResultDF = pd.concat([newtmprDF2,newtmpDF])
    # print('Done')
    return ResultDF


def fnMakeStaticDB(raw_df):
    import pandas as pd
    import numpy as np
    import re
    import x_MakeConditionDB

    r = re.compile('^RESULT(?!_DATE)')  # 정규 표현식 사용(결과값이 있는 범위를 찾기 위해

    ## Load rate per 조건에 대한 값들 처리(같은 시험에 해당하는 Load rate per를 하나의 행으로)
    rDF = x_MakeConditionDB.fnAddMeasureFlagConditionSTDB(raw_df)
    listduSN = rDF.loc[rDF['SPEC_NO'].duplicated(), 'SPEC_NO'].drop_duplicates()  # 중복 Spec_NO list 생성
    # listduSN = 'CPKT1029296X00001'

    newtmprDF = rDF.drop_duplicates('SPEC_NO').copy()
    ## SPEC_NO가 중복되지 않은 DB 생성
    newtmprDF2 = newtmprDF[newtmprDF['SPEC_NO'].isin \
        (pd.Series(list(set(rDF['SPEC_NO']) - set(listduSN))))].copy()
    newtmpDF = pd.DataFrame()  # 중복된 DB를 처리 후 저장할 DataFrame 생성
    indStartResult = np.where(rDF.columns == 'AIR')[0][0]  # 조건에 따라 결과들을 횡으로 연결, 연결된 결과 범위 설정

    ## 중복 리스트를 이용해서 중복시의 조건들을 구분
    totalCount = len(listduSN)
    count = 0
    for specNo in listduSN:
        count += 1
        tmpDF = rDF.loc[rDF['SPEC_NO'] == specNo].copy()
        # 하나의 스펙번호를 기준으로 시험 컨디션 조건(공기압, 시험기준 하중)에 대해서 데이터 처리
        # print(specNo) #디버깅용
        tmprCondDF = x_MakeConditionDB.fnMakeTestConditionDB(tmpDF, r, indStartResult)
        newtmpDF = newtmpDF.append(tmprCondDF)
        print(str(count) + ' of ' + str(totalCount))
    ResultDF = pd.concat([newtmprDF2, newtmpDF])
    # print('Done')
    return ResultDF

def fnMakeFlattracDB(raw_df):
    import pandas as pd
    import numpy as np
    import re
    import x_MakeConditionDB

    r = re.compile('^CA(?![^a-z])')  # 정규 표현식 사용(결과값이 있는 범위를 찾기 위해

    ## Load rate per 조건에 대한 값들 처리(같은 시험에 해당하는 Load rate per를 하나의 행으로)
    rDF = x_MakeConditionDB.fnPreprocessingFTDB(raw_df)
    listduSN = rDF.loc[rDF['SPEC_NO'].duplicated(), 'SPEC_NO'].drop_duplicates()  # 중복 Spec_NO list 생성
    # listduSN = 'CPKT1029296X00001'

    newtmprDF = rDF.drop_duplicates('SPEC_NO').copy()
    ## SPEC_NO가 중복되지 않은 DB 생성
    newtmprDF2 = newtmprDF[newtmprDF['SPEC_NO'].isin \
        (pd.Series(list(set(rDF['SPEC_NO']) - set(listduSN))))].copy()
    newtmpDF = pd.DataFrame()  # 중복된 DB를 처리 후 저장할 DataFrame 생성
    indStartResult = np.where(rDF.columns == 'AIR')[0][0]  # 조건에 따라 결과들을 횡으로 연결, 연결된 결과 범위 설정

    ## 중복 리스트를 이용해서 중복시의 조건들을 구분
    totalCount = len(listduSN)
    count = 0
    for specNo in listduSN:
        count += 1
        tmpDF = rDF.loc[rDF['SPEC_NO'] == specNo].copy()
        # 하나의 스펙번호를 기준으로 시험 컨디션 조건(공기압, 시험기준 하중)에 대해서 데이터 처리
        # print(specNo) #디버깅용
        tmprCondDF = x_MakeConditionDB.fnMakeTestConditionDB(tmpDF, r, indStartResult)
        newtmpDF = newtmpDF.append(tmprCondDF)
        print(str(count) + ' of ' + str(totalCount))
    ResultDF = pd.concat([newtmprDF2, newtmpDF])
    # print('Done')
    return ResultDF





