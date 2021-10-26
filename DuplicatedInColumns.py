def fnDuplicatedInColumns(df,keep) :
    """
    같은 columns 제거

    # 같은 columns 찾기
    duplicate_cols = df.columns[df.columns.duplicated()]
    """
    import pandas

    ddf = pandas.DataFrame()

    ddf = df.T
    ddf.reset_index(inplace = True)
    ddf.drop(ddf[ddf.duplicated(['index'],keep)].index, inplace=True)
    ddf.set_index('index', inplace = True)
    ddf = ddf.T
    ddf.index = range(0, len(ddf.index))

    if not ddf.columns[ddf.columns.duplicated()].empty :
        print("there is duplication pleas check directly")

    return ddf

def fnEmptyRowReplace(df, colRef, colName) :
    '''
    같은 column(정보)들인데 DB Table의 종류에 따라 데이터가 없는것들이 있다.
    이러한 경우 두가지의 정보들을 합쳐서 하나로 반환한다.
    선택된 기준 열을 기준으로 합치다. 기준열에 값이 없는 부분을 다른 열들의 값으로 채움
    colRef = number
    colName = string

    '''

    # import pandas
    import numpy

    ddf = df[colName]

    if len(ddf.columns) > 1 :
        for i in numpy.where(ddf.loc[colRef:, 'SPEC_NO'].isnull())[0].tolist() :
            ddf.loc[i][colRef] = ddf.loc[i][colRef-1]
        df[colName] = ddf[colName]
    else :
        print("there is no duplicated columns")
    return df