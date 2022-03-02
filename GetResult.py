import pandas as pd
import numpy as np
import pickle
import re
import _ModifyResult_
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit, QInputDialog)


pd.set_option('mode.chained_assignment',  None)

tmppath = 'D:\\uno\\unoDB\\'
tmppath2 = 'D:\\uno\\unoDB\\ResultDB\\'
tmppath3 = 'D:\\uno\\unoDB\\FinalDB\\'

itemNames = ['FT', 'ST', 'FS']

for itemName in itemNames :
    globals()[f'DB_{itemName}'] = \
        pickle.load(open(tmppath2 + 'ResultDBFull_' + itemName + '.pkl', 'rb'))
    globals()[f'ResultDB_{itemName}'] = _ModifyResult_.unoDB(globals()[f'DB_{itemName}'], itemName)
    pickle.dump(globals()[f'ResultDB_{itemName}'], open(tmppath3 + 'DBF_' + itemName + '.pkl', 'wb'))
