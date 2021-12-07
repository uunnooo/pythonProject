def fnAddConditionTestDB(df, condition, addrange, refval) :
    '''
    한번의 시험에 여러가지 조건에 의해 결과값이 여러개인 경우, 한개의 Spec당 여러개의 결과값이 존재.
    각 조건의 시험들을 하나의 행으로 만들어서 한개의 Spec당 한개의 DB로 만듬
    df = DataFrame
    condition = 데이터가 추가되는 조건
    addrannge = 추가되는 조건에 따라오는 결과값들(범위지정)
    refval = 행을 이어붙일때 기준이 되는 행(여러가지 조건들 중 기준 조건뒤에 데이터들 연결)
    '''
    import pandas as pd
    import numpy as np

    tmpAddDF2 = df[df[condition] == refval].copy()
    df.sort_values([condition], inplace=True)
    for i in range(len(df.drop_duplicates([condition]))):
        if df.loc[df.index[i], condition] != refval:  # 하중 refval을 기준으로 데이터 결합
            indColumnLRP = np.where(df.columns == condition)[0][0]
            tmpDF1 = df.iloc[[i], addrange]
            for ind in range(len(tmpDF1.columns)):
                tmpDF1.rename(columns={tmpDF1.columns[ind]: tmpDF1.columns[ind]
                                                            + '_' + str(df.iloc[i, indColumnLRP])}, inplace=True)
            tmpDF1.rename(index={tmpDF1.index[0]: tmpAddDF2.index[0]}, inplace=True)
            tmpAddDF2 = pd.concat([tmpAddDF2, tmpDF1], axis=1)


    return tmpAddDF2.copy()

def fnAddLoadRatePerConditionFSDB(df, dirpath) :
    '''
    :param df: Pandas Data Frame of Footshape DB include condition of Load rate per
    :return: Pandas Data Frame of Footshpate DB rearrange conition of Load rate per
    ex) df + result1_load rate per1 result2_load rate per2 ... resultn_load rate pern
        n : number of Load rate per condition
    '''
    import pandas as pd
    import numpy as np
    import _DropDupliCol_

    ## 전처리
    # 칼럼을 합치기 전에 합치게 될 기준열을 정하고 기준열에 없는 정보들은 다른열에 있는 값으로 채움
    DF1 = _DropDupliCol_.fnEmptyRowReplace(df, 0, 'SPEC_NO')
    # 중복되는 칼럼들 제거(제거시 각 테이블별 없는 정보들이있어서 주의 필요)
    DF2 = _DropDupliCol_.fnDuplicatedInColumns(DF1, 'first')
    # CA가 없는 모든값 제거, CA가 없으면 Result가 없다. 결과가 없는 시험 데이터 제거
    rDF1 = DF2.dropna(subset=['TOTAL_CONTACT_AREA']).copy()
    # CA가 0인값 제거, 결과가 없는것으로 판단
    rDF1 = rDF1.drop(rDF1[DF2['TOTAL_CONTACT_AREA'] == 0].index).copy()
    # AIR가 없거나 Load가 없는 데이터 제거, 시험조건이 없는 경우의 데이터는 사용 불가
    rDF1 = rDF1.drop(rDF1[rDF1['LOAD_KG'].isna() | rDF1['AIR'].isna()].index).copy()

    ## SPEC_NO에 대해서 유일한 데이터 프레임 생성(DB를 이용시 기준은 SPEC_NO가 된다)
    # LOAD_RATE_PER 100을 기준 데이터로 사용
    DF3 = rDF1[rDF1['LOAD_RATE_PER'] == 100].copy()
    rDF2 = DF3.drop_duplicates('SPEC_NO').copy()

    ## SPEC_NO에 대해 중복되어 누락되어 지는 데이터를 기준으로 Load Rate Per에 해당하는 결과 데이터들을 결합
    # 중복 SPEC NO 뽑아 리스트로 만들기
    listduSN = rDF1.loc[rDF1['SPEC_NO'].duplicated(), 'SPEC_NO'].drop_duplicates()
    # 변경되어져야할 값을 저장할 DataFrame 생성
    newtmpDF = pd.DataFrame()
    # 조건에 따라 결과들을 횡으로 연결, 연결될 결과 범위 설정
    indStartResult = np.where(rDF2.columns == 'LOAD_KG')[0][0]
    indEndResult = len(rDF2.columns)
    rangeResult = range(indStartResult, indEndResult)

    ## 결과 처리
    # 각 조건들에 대해서 Load rate per에 대한 값들을 열에 추가
    # 각 조건들은 행으로 추가
    for specNo in listduSN:
        tmpDF = rDF1.loc[rDF1['SPEC_NO'] == specNo].copy()
        listduRN = tmpDF.loc[tmpDF['REQ_NO'].duplicated(), 'REQ_NO'].drop_duplicates()
        for reqNo in listduRN:
            tmpDFReq = tmpDF[tmpDF['REQ_NO'] == reqNo].copy()
            listduTN = tmpDFReq.loc[tmpDFReq['TIRE_NO'].duplicated(), 'TIRE_NO'] \
                .drop_duplicates().sort_values()
            for tireNo in listduTN:
                tmpDFTire = tmpDFReq[tmpDFReq['TIRE_NO'] == tireNo].copy()
                listduCN = tmpDFTire.loc[tmpDFTire['TEST_COND_NO'].duplicated(), 'TEST_COND_NO'] \
                    .drop_duplicates().sort_values()
                for condNo in listduCN:
                    tmpDFCond1 = tmpDFTire[tmpDFTire['TEST_COND_NO'] == condNo].copy()
                    # 무슨 오류인지 모르는데 같은 데이터가 중복으로 들어간 경우가 있다. 중북된 데이터 제거
                    # 어떤 값을 기준으로 사용해야 할지 모르는 경우와 같은 데이터가 중복으로 들어가 있는 모든 경우 제거
                    tmpDFCond2 = tmpDFCond1.drop_duplicates('LOAD_RATE_PER').copy()
                    tmpDF1 = fnAddConditionTestDB(tmpDFCond2, 'LOAD_RATE_PER', rangeResult, 100)
                    newtmpDF = newtmpDF.append(tmpDF1)

    # pickle.dump(newtmpDF, open(dirpath + 'pdFSUno.pkl', 'wb'))
    return newtmpDF.copy()

def fnAddMesrFlagConditionSTDB(df, dirpath) :
    '''
    :param df: Pandas Data Frame of Static DB include condition of Load rate per
    :return: Pandas Data Frame of Static DB rearrange condition of Load rate per
    ex) df + result1_measureflag1 result2_measureflag2 ... resultn_measureflagn
     n : number of Load rate per condition
    '''
    import pandas as pd
    import numpy as np
    import _DropDupliCol_

    ## 전처리
    # 칼럼을 합치기 전에 합치게 될 기준열을 정하고 기준열에 없는 정보들은 다른열에 있는 값으로 채움
    DF1 = _DropDupliCol_.fnEmptyRowReplace(df, 0, 'SPEC_NO')
    # 중복되는 칼럼들 제거(제거시 각 테이블별 없는 정보들이있어서 주의 필요)
    DF2 = _DropDupliCol_.fnDuplicatedInColumns(DF1, 'first')
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

    ## SPEC_NO에 대해 중복되어 누락되어 지는 데이터를 기준 MESR_FLAG에 해당하는 결과 데이터들을 결합
    # 중복 SPEC NO 뽑아 리스트로 만들기
    listduSN = rDF5.loc[rDF5['SPEC_NO'].duplicated(), 'SPEC_NO'].drop_duplicates()
    # listduSN = ['DSKT2021441X00059']
    # listduSN = ['Competitive Tire_EXT-2021-00362_-']
    # 변경되어져야할 값을 저장할 DataFrame 생성
    newtmpDF = pd.DataFrame()

    ## 조건에 따라 결과들을 횡으로 연결, 연결될 결과 범위 설정
    # KV 데이터 처리용
    indStartResult = np.where(rDF3.columns == 'STEP_RATE')[0][0]
    indEndResult = len(rDF3.columns)
    rangeResult = range(indStartResult, indEndResult)
    # KD, KL, KT 데이터 처리용
    indStartResult2 = np.where(rDF3.columns == 'TEST_ITEM')[0][0]

    ## 결과 처리
    # 각 조건들에 대해서 MESR_FLAG에 대한 값들을 열에 추가
    # 각 조건들은 행으로 추가
    for specNo in listduSN:
        tmpDF = rDF3.loc[rDF3['SPEC_NO'] == specNo].copy()
        listduRN = tmpDF.loc[tmpDF['REQ_NO'].duplicated(), 'REQ_NO'].drop_duplicates()
        for reqNo in listduRN:
            tmpDFReq = tmpDF[tmpDF['REQ_NO'] == reqNo].copy()
            listduTN = tmpDFReq.loc[tmpDFReq['TIRE_NO'].duplicated(), 'TIRE_NO'] \
                .drop_duplicates().sort_values()
            for tireNo in listduTN:
                tmpDFTire = tmpDFReq[tmpDFReq['TIRE_NO'] == tireNo].copy()
                listduCN = tmpDFTire.loc[tmpDFTire['TEST_COND_NO'].duplicated(), 'TEST_COND_NO'] \
                    .drop_duplicates().sort_values()
                for condNo in listduCN:
                    # 모든 결과가 포함되어 있는 DF 생성
                    tmpAddDF = pd.DataFrame()
                    ## KV, KD, KL, KT 결과에 따라 각각의 DF 생성
                    # KV DF 생성
                    tmpDFCond1 = tmpDFTire[
                        (tmpDFTire['TEST_COND_NO'] == condNo) & (tmpDFTire['TEST_ITEM'] == 'KV')].copy()
                    # KD DF 생성
                    tmpDFCond2 = tmpDFTire[
                        (tmpDFTire['TEST_COND_NO'] == condNo) & (tmpDFTire['TEST_ITEM'] == 'KD')].copy()
                    tmpAddDF1 = tmpDFCond2.iloc[:, indStartResult2:]
                    for ind in range(len(tmpAddDF1.columns)):
                        tmpAddDF1.rename(columns={tmpAddDF1.columns[ind]: tmpAddDF1.columns[ind] + '_KD'},
                                        inplace=True)
                    # KL DF 생성
                    tmpDFCond3 = tmpDFTire[
                        (tmpDFTire['TEST_COND_NO'] == condNo) & (tmpDFTire['TEST_ITEM'] == 'KL')].copy()
                    tmpAddDF2 = tmpDFCond3.iloc[:, indStartResult2:]
                    for ind in range(len(tmpAddDF2.columns)):
                        tmpAddDF2.rename(columns={tmpAddDF2.columns[ind]: tmpAddDF2.columns[ind] + '_KL'},
                                        inplace=True)
                    # KT DF 생성
                    tmpDFCond4 = tmpDFTire[
                        (tmpDFTire['TEST_COND_NO'] == condNo) & (tmpDFTire['TEST_ITEM'] == 'KT')].copy()
                    tmpAddDF3 = tmpDFCond4.iloc[:, indStartResult2:]
                    for ind in range(len(tmpAddDF3.columns)):
                        tmpAddDF3.rename(columns={tmpAddDF3.columns[ind]: tmpAddDF3.columns[ind] + '_KT'},
                                        inplace=True)

                    # 무슨 오류인지 모르는데 같은 데이터가 중복으로 들어간 경우가 있다. 중북된 데이터 제거
                    # 어떤 값을 기준으로 사용해야 할지 모르는 경우와 같은 데이터가 중복으로 들어가 있는 모든 경우 제거
                    tmprDFCond1 = tmpDFCond1.drop_duplicates('MESR_FLAG').copy()
                    # KV 데이터 처리
                    tmpDF1 = fnAddConditionTestDB(tmprDFCond1, 'MESR_FLAG', rangeResult, 100)

                    # KV 데이터가 없는 경우 DB 제외
                    if len(tmpDF1) > 0 :
                       ## KD, KL, KT 처리
                       # KD
                        if len(tmpAddDF1) > 0 :
                            tmpAddDF1 = tmpAddDF1.rename(index={tmpAddDF1.index[0]: tmpDF1.index[0]}).copy()
                            tmpAddDF = pd.concat([tmpAddDF, tmpAddDF1], axis=1)
                        # KL
                        if len(tmpAddDF2) > 0 :
                            tmpAddDF2 = tmpAddDF2.rename(index={tmpAddDF2.index[0]: tmpDF1.index[0]}).copy()
                            tmpAddDF = pd.concat([tmpAddDF, tmpAddDF2], axis=1)
                        # KT
                        if len(tmpAddDF3) > 0 :
                            tmpAddDF3 = tmpAddDF3.rename(index={tmpAddDF3.index[0]: tmpDF1.index[0]}).copy()
                            tmpAddDF = pd.concat([tmpAddDF, tmpAddDF3], axis=1)
                        # 모든 결과값에 대해서 하나의 행으로 데이터 프레임 생성
                        # KV를 기준으로 KD, KL, KT를 연결
                        tmpDF2 = pd.concat([tmpDF1, tmpAddDF], axis=1).copy()
                        newtmpDF = newtmpDF.append(tmpDF2)

    # pickle.dump(newtmpDF, open(dirpath + 'pdSTUno.pkl', 'wb'))
    return newtmpDF.copy()