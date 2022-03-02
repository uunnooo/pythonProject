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

itemNames = ['FT', 'ST', 'FS']

for itemName in itemNames :
    globals()[f'DB_{itemName}'] = \
        pickle.load(open(tmppath2 + 'ResultDBFull_' + itemName + '.pkl', 'rb'))
        # pickle.load(open(tmppath2 + 'ResultDBTotal_' + itemName + '.pkl', 'rb'))
    globals()[f'ResultDB_{itemName}'] = _ModifyResult_.unoDB(globals()[f'DB_{itemName}'], itemName)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btn = QPushButton('Dialog', self)
        self.btn.move(30, 30)
        self.btn.clicked.connect(self.showDialog)

        self.le = QLineEdit(self)
        self.le.move(120, 35)

        self.setWindowTitle('Input dialog')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')

        if ok:
            self.le.setText(str(text))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
