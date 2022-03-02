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
## GUI 구성을 위한 Item List 생성


class unoDB:
    def __init__(self, df, item):

        self.SpecNo = ['SPEC_NO']
        self.TireInfor = ['SPEC_SIZE', 'SIZE_NSW', 'SIZE_SERISE', 'SIZE_INCH', 'PATTERN']
        self.ResultInfor = ['REQ_NO', 'AIR', 'LOAD_100', 'TEST_LOAD', 'CONFIRM_DATE']
        self.PreInfor = self.SpecNo + self.TireInfor + self.ResultInfor
        self.CMP = ['CTB_COMPOUND', 'SUT_COMPOUND', 'BSW_COMPOUND']  # Compound
        self.CCS = ['C01_MATERIAL', 'C01_ROLLED', 'C01_EPI']  # 카카스
        self.BT1 = ['BT1_MATERIAL', 'BT1_WIDTH', 'BT1_EPI', 'BT1_ANGLE']  # 1벨트
        self.BT2 = ['BT2_MATERIAL', 'BT2_WIDTH', 'BT2_EPI', 'BT2_ANGLE']  # 2벨트
        self.JLC = ['JLC_MATERIAL', 'JLC_ROLLED', 'JLC_TYPE']  # 보강구조
        self.BF = ['FIL_COMPOUND', 'FIL_WIDTH', 'BEAD_BIC']  # Bead / Filer
        self.PCI = ['PCI_WIDTH', 'PCI_PRESS', 'CURING_TIME', 'PRE_CURING_TEMPERATURE']  # PCI
        self.ETC = ['TUH_1_2', 'MOLD_SD', 'CTS_BELT_LIFT']  # 벨트 리프트율
        self.RawResultFS = ['REQ_NO', 'REQ_REVISION', 'TEST_NO', 'TIRE_NO', 'TEST_COND_NO', 'TEST_COND_CODE',
                            'SPEC_SEQ', 'ITEM_SEQ', 'LOAD_KG', 'LOAD_RATE_PER', 'CONTACT_LENGTH_MM_MAX',
                            'CONTACT_LENGTH_MM_CENTER', 'CONTACT_LENGTH_MM_25', 'CONTACT_LENGTH_MM_75',
                            'CONTACT_WIDTH_MM_MAX', 'CONTACT_WIDTH_MM_CENTER', 'CONTACT_WIDTH_MM_25',
                            'CONTACT_WIDTH_MM_75', 'SQUARE_RATIO', 'CONTACT_RATIO', 'ROUNDNESS',
                            'ACTUAL_CONTACT_AREA', 'TOTAL_CONTACT_AREA', 'FILEPATH', 'FILENAME', 'HINT_DETAIL_OBJ_ID']
        self.RawResultST = ['REQ_NO', 'REQ_REVISION', 'TEST_NO', 'TIRE_NO', 'TEST_COND_NO', 'TEST_ITEM',
                            'STEP_RATE', 'MESR_FLAG', 'DISPLACE', 'LOAD', 'RESULT', 'GLOBAL_RESULT',
                            'GLOBAL_CONVERSION']
        self.RawResultFT = ['REQ_NO', 'REQ_REVISION', 'TEST_NO', 'TIRE_NO', 'TEST_COND_NO', 'TEST_COND_CODE',
                            'CA', 'CAT', 'PRAT', 'LOAD_N', 'REF_INFLATION', 'CA_COEF_A', 'CA_COEF_B', 'CA_COEF_C',
                            'LM_COEF_A', 'LM_COEF_B', 'LM_COEF_C', 'LOCAL_PRAT', 'GLOBAL_PRAT']
        self.SPECALL = self.CMP + self.CCS + self.BT1 + self.BT2 + self.JLC + self.BF + self.PCI + self.ETC

        if item != 'None':
            if item == 'FS':
                self.Result = self.FindResultCols(reFS, df)

            elif item == 'ST':
                self.Result = self.FindResultCols(reST, df)

            elif item == 'FT':
                self.Result = self.FindResultCols(reFT, df)

            self.ALL = self.PreInfor + self.SPECALL + self.Result
            tmpDB = self.SpecModify(df)

            self.DB = tmpDB[self.ALL]

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
