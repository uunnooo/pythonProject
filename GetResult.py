import pandas as pd
import numpy as np
import pickle
import re
import _ModifyResult_


pd.set_option('mode.chained_assignment',  None)

tmppath = 'D:\\uno\\unoDB\\'
tmppath2 = 'D:\\uno\\unoDB\\ResultDB\\'

itemNames = ['FT', 'ST', 'FS']

for itemName in itemNames :
    globals()[f'DB_{itemName}'] = \
        pickle.load(open(tmppath2 + 'ResultDBTotal_' + itemName + '.pkl', 'rb'))


Result = _ModifyResult_.colsList(globals()['DB_FT'], 'FT', _ModifyResult_.colsSpecNo, _ModifyResult_.colsTireInfor,
                               _ModifyResult_.colsSpec, _ModifyResult_.colsResultInfor)

print('Done')
