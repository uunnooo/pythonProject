def GetFSDB(specNo) :

    import pickle

    tmppath3 = 'D:\\uno\\unoDB\\FinalDB\\'
    colResult = [0, 4, 7, 10]

    DB_FS = pickle.load(open(tmppath3 + 'DBF_FS' + '.pkl', 'rb'))
    DB = []
    resultDB = []
    DB = DB_FS.DB[DB_FS.DB['SPEC_NO'] == specNo]
    if len(DB) :
        resultDB = DB[[DB_FS.SpecNo[0],DB_FS.ALL[36],DB_FS.Result[colResult[0]],
                       DB_FS.Result[colResult[1]],DB_FS.Result[colResult[2]],
                       DB_FS.Result[colResult[3]]]]
    return resultDB






