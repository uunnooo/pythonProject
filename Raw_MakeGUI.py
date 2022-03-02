import pandas as pd
import numpy as np
import pickle
import _ModifyResult_
import sys
from PyQt5.QtWidgets import *
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats

tmppath = 'D:\\uno\\unoDB\\'
tmppath2 = 'D:\\uno\\unoDB\\ResultDB\\'
tmppath3 = 'D:\\uno\\unoDB\\FinalDB\\'

listTestItem = ['FT', 'ST', 'FS']
listTireSpec = ['TireInfor', 'CMP', 'CCS', 'BT1', 'BT2', 'JLC', 'BF', 'PCI', 'ETC', 'SPECALL']

DB_FT = pickle.load(open(tmppath3 + 'DBF_FT' + '.pkl', 'rb'))
DB_FS = pickle.load(open(tmppath3 + 'DBF_FS' + '.pkl', 'rb'))
DB_ST = pickle.load(open(tmppath3 + 'DBF_ST' + '.pkl', 'rb'))

colName = _ModifyResult_.unoDB(pd.DataFrame(), 'None')


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        # GUI Global 변수 선언
        self.itemConstraint = []

    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)
        ## Test Item 선택 추후 멀티 선택 가능하게
        self.listwidgetTestItem = QListWidget()
        self.listwidgetTestItem.setSortingEnabled(True)
        listCount = 0
        for testItem in listTestItem :
            self.listwidgetTestItem.insertItem(listCount, testItem)
            listCount =+ 1
        self.listwidgetTestItem.clicked.connect(self.clickedLTI)
        ## Tire Design Paramter 선택
        self.listwidgetTireSpec = QListWidget()
        self.listwidgetTireSpec.setSortingEnabled(True)
        listCount = 0
        for TireSpec in listTireSpec :
            self.listwidgetTireSpec.insertItem(listCount, TireSpec)
            listCount = + 1
        self.listwidgetTireSpec.clicked.connect(self.clickedLTS)
        ## Tire Spec Detail 리스트창
        self.listwidgetSpecDetail = QListWidget()
        self.listwidgetSpecDetail.setSortingEnabled(True)
        self.listwidgetSpecDetail.clicked.connect(self.clickedLSD)
        ## 보고 싶은 스펙 리스트 창
        self.listwidgetSpecItem = QListWidget()
        self.listwidgetSpecItem.setSortingEnabled(True)
        self.listwidgetSpecItem.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listwidgetSpecItem.clicked.connect(self.clickedLSA)
        ## 보고 싶은 결과 Parameter 창
        self.listwidgetResultItem = QListWidget()
        self.listwidgetResultItem.setSortingEnabled(True)
        self.listwidgetResultItem.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listwidgetResultItem.clicked.connect(self.clickedLRI)
        ## 그래프 출력 버튼
        self.pbPlot = QPushButton()
        self.pbPlot.setText('PLOT')
        self.pbPlot.setEnabled(False)
        self.pbPlot.clicked.connect(self.clickedPPL)
        ## 구속조건 추가 버튼
        self.pbADDConst = QPushButton()
        self.pbADDConst.setText('ADD Constrain')
        self.pbADDConst.setEnabled(False)
        self.pbADDConst.clicked.connect(self.clickedPAC)
        ## 구속조건리스트
        self.listwidgetConstrainItem = QListWidget()
        self.listwidgetConstrainItem.setSortingEnabled(True)
        self.listwidgetConstrainItem.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listwidgetConstrainItem.clicked.connect(self.clickedLCI)

        layout.addWidget(self.listwidgetTestItem, 0, 0)
        layout.addWidget(self.listwidgetTireSpec, 1, 0)
        layout.addWidget(self.listwidgetSpecDetail, 0, 1, 2, 1)
        layout.addWidget(self.listwidgetSpecItem, 0, 2, 2, 1)
        layout.addWidget(self.listwidgetResultItem, 0, 3, 2, 1)
        layout.addWidget(self.pbPlot, 0, 4, 1, 1)
        layout.addWidget(self.pbADDConst, 1, 4, 1, 1)
        layout.addWidget(self.listwidgetConstrainItem, 2, 1, 1, 2)
        self.setGeometry(300, 300, 1200, 500)

    def clickedLTI(self, qmodelindex) :
        self.DB = []
        item = self.listwidgetTestItem.currentItem()
        if item.text() == 'FT' : self.DB = DB_FT
        elif item.text() == 'ST' : self.DB = DB_ST
        elif item.text() == 'FS' : self.DB = DB_FS
        else : print('There are no Matching Test Item')

    def clickedLTS(self, qmodelindex) :
        item = self.listwidgetTireSpec.currentItem()
        listSpecDetail = self.DB.__dict__.get(item.text())
        listCount = 0
        self.listwidgetSpecDetail.clear()
        for Spec in listSpecDetail :
            self.listwidgetSpecDetail.insertItem(listCount, Spec)
            listCount = + 1

    def clickedLSD(self, qmodelindex) :
        selSpec = self.listwidgetSpecDetail.currentItem()
        selTest = self.listwidgetTestItem.currentItem()
        self.itemTest = selTest.text()
        self.itemSpec = selSpec.text()
        listSpec = self.DB.DB[self.itemSpec].drop_duplicates()
        listCount = 0
        self.listwidgetSpecItem.clear()
        for Spec in listSpec:
            self.listwidgetSpecItem.insertItem(listCount, Spec)
            listCount = + 1

    def clickedLSA(self, qmodelindex) :
        self.itemSpecApplied = []
        selSpec = self.listwidgetSpecItem.selectedItems()
        for i in range(len(selSpec)) :
            self.itemSpecApplied.append(selSpec[i].text())
        listCount = 0
        self.listwidgetResultItem.clear()
        for data in self.DB.__dict__.get('Result') :
            self.listwidgetResultItem.insertItem(listCount, data)
            listCount = + 1
        print(self.itemSpecApplied)

    def clickedLRI(self, qmodelindex) :
        self.itemResult = []
        selResultItem = self.listwidgetResultItem.selectedItems()
        for i in range(len(selResultItem)):
            self.itemResult.append(selResultItem[i].text())
        self.pbPlot.setEnabled(True)
        self.pbADDConst.setEnabled(True)
        print(self.itemResult)

    def clickedPPL(self, qmodelindex) :
        figF = go.Figure()
        for data in self.itemResult :
            for selSpec in self.itemSpecApplied :
                figDB = self.DB.DB[self.DB.DB[self.itemSpec].isin([selSpec])]
                # fig = px.scatter(figDB, y=data, x=self.itemSpec)
                figF.add_box(y=figDB[data], x=figDB[self.itemSpec], boxpoints='all',
                             name=selSpec+'_'+data)
                print(figDB[data].astype('float').describe())
                # fig.update_traces(marker_size=2)
                # fig = px.scatter(resultDB, y=data, x=self.itemSpec)
                # fig.update_traces(marker_size=2)
                # fig.data[1].xaxis = 'x'
                # figF.add_trace(fig.data[0])
                # figF.add_trace(fig.data[1])
        figF.show()
        print('Good')

    def clickedPAC(self, qmodelindex) :

        listCount = 0
        for selSpec in self.itemSpecApplied :
            constraintItem = self.itemSpec + '@' + selSpec
            self.listwidgetConstrainItem.insertItem(listCount, constraintItem)
            self.itemConstraint.append(constraintItem)
            listCount = + 1
        print(self.itemSpec)
        print(self.itemSpecApplied)

    def clickedLCI(self, qmodelindex) :
        ConstranitSpec = self.listwidgetConstrainItem.currentItem()
        print('List MSG' + ConstranitSpec.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())