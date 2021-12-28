import re
import pandas as pd
import numpy as np
import _PLMChangeSpec_

# footshape 결과값
reFS = re.compile('CONTACT|SQUARE|ROUNDNESS')
# static 결과값
reST = re.compile('^RESULT(?!_DATE)')
# flattrac 결과값
reFT = re.compile('^CA_?(?![^0-9])')

# 스펙 정보 Modify
colsSpecNo = ['SPEC_NO']
colsTireInfor = ['SPEC_SIZE', 'SIZE_NSW', 'SIZE_SERISE', 'SIZE_INCH', 'PATTERN']
colsResultInfor = ['REQ_NO', 'AIR', 'LOAD_100', 'TEST_LOAD', 'CONFIRM_DATE']
colsSpecCompound = ['CTB_COMPOUND', 'SUT_COMPOUND', 'BSW_COMPOUND'] # Compound
colsSpecCarcass = ['C01_MATERIAL', 'C01_ROLLED', 'C01_EPI'] # 카카스
colsSpecBelt1 = ['BT1_MATERIAL', 'BT1_WIDTH', 'BT1_EPI', 'BT1_ANGLE'] # 1벨트
colsSpecBelt2 = ['BT2_MATERIAL', 'BT2_WIDTH', 'BT2_EPI', 'BT2_ANGLE'] # 2벨트
colsSpecJLC = ['JLC_MATERIAL', 'JLC_ROLLED', 'JLC_TYPE'] # 보강구조
colsSpecBF = ['FIL_COMPOUND', 'FIL_WIDTH', 'BEAD_BIC'] # Bead / Filer
colsSpecPCI = ['PCI_WIDTH', 'PCI_PRESS', 'CURING_TIME', 'PRE_CURING_TEMPERATURE'] # PCI
colsSpecETC = ['TUH_1_2', 'MOLD_SD', 'CTS_BELT_LIFT'] # 벨트 리프트율


class spec :
    def __init__(self, colsSpecCompound, colsSpecCarcass, colsSpecBelt1, colsSpecBelt2,
                 colsSpecJLC, colsSpecBF, colsSpecPCI, colsSpecETC) :
        self.CMP = colsSpecCompound
        self.CCS = colsSpecCarcass
        self.BT1 = colsSpecBelt1
        self.BT2 = colsSpecBelt2
        self.JLC = colsSpecJLC
        self.BF = colsSpecBF
        self.PCI = colsSpecPCI
        self.ETC = colsSpecETC
        self.ALL = colsSpecCompound + colsSpecCarcass + colsSpecBelt1 +\
                   colsSpecBelt2 + colsSpecJLC + colsSpecBF + colsSpecPCI + colsSpecETC

'''
colsSpec = ['CTB_COMPOUND', 'SUT_COMPOUND', 'BSW_COMPOUND',  # Compound
            'C01_MATERIAL', 'C01_ROLLED', 'C01_EPI',  # 카카스
            'BT1_MATERIAL', 'BT1_WIDTH', 'BT1_EPI', 'BT1_ANGLE',  # 1벨트
            'BT2_MATERIAL', 'BT2_WIDTH', 'BT2_EPI', 'BT2_ANGLE',  # 2벨트
            'CTS_BELT_LIFT',  # 벨트 리프트율
            'JLC_MATERIAL', 'JLC_ROLLED', 'JLC_TYPE',  # 보강구조
            'FIL_COMPOUND', 'FIL_WIDTH', 'BEAD_BIC',  # Bead / Filer
            'PCI_WIDTH', 'PCI_PRESS', 'CURING_TIME', 'PRE_CURING_TEMPERATURE',  # PCI
            'TUH_1_2', 'MOLD_SD'
            ]
'''

class colsList:
    def __init__(self, df, item, colsspecno, colstireinfor, colsspec, colsresultinfor):
        self.SpecNo = colsspecno
        self.TireInfor = colstireinfor
        self.Spec = colsspec
        self.ResultInfor = colsresultinfor
        self.PreInfor = colsspecno + colstireinfor + colsspec + colsresultinfor
        if item == 'FS':
            self.Result = self.FindResultCols(reFS, df)
        elif item == 'ST':
            self.Result = self.FindResultCols(reST, df)
        elif item == 'FT':
            self.Result = self.FindResultCols(reFT, df)
        self.All = self.PreInfor + self.Result
        tmpDB = self.SpecModify(df)
        self.DB = tmpDB[self.All]

    def SetResultCols(self, ft, st, fs):
        self.ResultFT = ft
        self.ResultST = st
        self.ResultFS = fs

    @staticmethod
    def FindResultCols(reg, df):
        resultArray = pd.DataFrame([reg.findall(name) for name in df.columns])
        resultInd = np.where(resultArray)[0]
        resultStr = list(df.columns[resultInd])
        return resultStr

    @staticmethod
    def SpecModify(df):
        tmpDF = df.copy()
        tmpDF['JLC_MATERIAL'] = df['JLC_MATERIAL'].replace \
            (_PLMChangeSpec_.JLC_MATERIAL_ASIS, _PLMChangeSpec_.JLC_MATERIAL_TOBE)
        tmpDF['C01_MATERIAL'] = df['C01_MATERIAL'].replace \
            (_PLMChangeSpec_.C01_MATERIAL_ASIS, _PLMChangeSpec_.C01_MATERIAL_TOBE)
        return tmpDF


# cols = colsList(colsSpecNo, colsTireInfor, colsSpec, colsResultInfor)
