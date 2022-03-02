def fnMakePDMeanValue(reguler, raw_df) :

    return



def fnMakeFootshapeDB(raw_df) :
    
    import pandas as pd
    import numpy as np
    import re
    import x_MakeConditionDB

    p = re.compile('^FILE|HINT')  # 정규 표현식 사용(결과값이 있는 범위를 찾기 위해
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
    '''
    하나의 스펙에 대해서 컨디션 조건에 따라 분류 하고, 우선적으로 최신 날짜의 데이터를 찾아 내고, 최신 데이터를 평균하여 데이터 처리
    하나의 스펙에 한개의 컨디션이 있어도 결국 최신 데이터가 되고, 평균이 된다.
    '''
    for specNo in listduSN:
        tmprCondDF = pd.DataFrame()
        tmpDF = rDF.loc[rDF['SPEC_NO'] == specNo].copy()
        countCond = 1
        # 하나의 스펙번호를 기준으로 시험 컨디션 조건(공기압, 시험기준 하중)에 대해서 데이터 처리
        for tCond in tmpDF[['AIR', 'TEST_LOAD']].drop_duplicates().values:
            tmpDF1 = tmpDF[(tmpDF['AIR'] == tCond[0]) & (tmpDF['TEST_LOAD'] == tCond[1])].copy()
            # 같은 조건의 시험 데이터중 최신의 데이터를 사용(하나의 데이터가 있으면 결국 그 하나가 최신 데이터가 된다)
            maxDate = tmpDF1.iloc[[tmpDF1['CONFIRM_DATE'].argmax()], np.where(tmpDF1.columns == 'CONFIRM_DATE')[0][0]]
            tmpDF2 = tmpDF1[tmpDF1['CONFIRM_DATE'] == maxDate.iloc[0]].copy()
            ## 최신 데이터들에 대해서만 데이터 처리(평균값 사용)
            # 평균값을 넣을 데이터 프레임 생성(최신 시험 날짜 기준 한개의 데이터 프레임 선정)
            tmpDF3 = tmpDF2.drop_duplicates('SPEC_NO').copy()
            # 시험 결과 데이터에 대한 인덱스를 찾아 인덱스 설정
            tmpResultVal = pd.DataFrame([r.findall(str) for str in tmpDF2.columns]) # 정규표현을 이용하여 시험 결과값이 있는 칼럼 선택
            indResultVal = np.where(tmpResultVal)[0]
            indAddRange = ['SPEC_NO'] + list(tmpDF3.columns[indStartResult:].values)
            # 시험 데이터에 해당하는 칼럼에 대해서만 평균값 계산
            for colNum in indResultVal:
                tmpDF3[tmpDF3.columns[colNum]] = \
                    format(tmpDF2[tmpDF2.columns[colNum]].astype('float').mean(), '.2f')
                tmpDF3[tmpDF3.columns[colNum]].astype('object')
                # 머지를 써야 하나 concat를 써야 하나 어떻해 합쳐야 하는지
            tmpAddDF = tmpDF3.loc[:, indAddRange]
            if len(tmprCondDF) > 0 :
                tmprCondDF = pd.merge(tmprCondDF, tmpAddDF, on = 'SPEC_NO', suffixes = ("",'_'+str(countCond)))
                countCond += 1
            else : tmprCondDF = tmprCondDF.append(tmpDF3)
        newtmpDF = newtmpDF.append(tmprCondDF)
    ResultDF = pd.concat([newtmprDF2,newtmpDF])
    print('Done')
    return ResultDF






