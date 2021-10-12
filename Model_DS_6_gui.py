import sys
import io
import csv
from PyQt5 import uic
# from PyQt5 import QtWidgets
# from PyQt5 import QtCore
# from PyQt5.QtCore import QSize
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from datetime import datetime
import _use_cols
import pickle
import pandas as pd
pd.set_option('mode.chained_assignment',  None)
import cx_Oracle
import _auth_config as auth
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import random

#UI파일 연결
Ui_MainWindow = uic.loadUiType("UI_Main.ui")[0]
# from UI_Main import Ui_MainWindow
# pyuic5 -x UI_Main.ui -o UI_Main.py # UI 파일을 Py 파일로 변환 < 커맨드창에서 실행
# from UI_Sub1 import Ui_SubWindow1

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import RobustScaler

global df2, df5, df6, df7, df50, df50_X, df60, new_spec_no, specs, \
    check_btn_ck, check_btn5_ck, doe_items, df_doe, df4_1,col_names,effects
new_spec_no = 1
check_btn_ck = 0
check_btn5_ck = 0
g_row = 100
g_colm = 100

class ohe():  # One Hot Encording (OHE)
    def __init__(self, dfs, use_cols):
        self.dfs = dfs
        self.use_cols = use_cols

    def scale_columns(self):
        return self.dfs[0][self.use_cols].select_dtypes(exclude='object').columns.tolist()

    def dummify(self, target):
        sizes = [df.shape[0] for df in self.dfs]

        df_dummies = self.dfs[0].copy()
        for df in self.dfs[1:]:
            df_dummies = df_dummies.append(df)
        df_dummies = pd.get_dummies(df_dummies[self.use_cols + [target]])

        dummy_dfs = []
        for i, size in enumerate(sizes):
            if -sum(sizes[i + 1:]) != 0:
                dummy_dfs.append(df_dummies.iloc[-sum(sizes[i:]):-sum(sizes[i + 1:]), :].reset_index(drop=True))
            else:
                dummy_dfs.append(df_dummies.iloc[-sum(sizes[i:]):, :].reset_index(drop=True))

        return dummy_dfs

def prediction_run (targets, ohe, df5, use_cols, scale_cols, samples, scaler_alldata, _DS_data, df2):
    target = targets[0] #임의의 target을 설정하고, 그래야 one-hot-encording 실행을 위해서...
    df5[target] = 0
    df_ohe = ohe([df5, df5],use_cols) #문자열은 one hot encording을 적용하고
    [dummy_df5, dummy_df5] = df_ohe.dummify(target)
    temp_input = dummy_df5.drop(target, axis=1)

    # Input Sample과 동일한 열 이름으로 만들어 주기
    temp_input2 = pd.concat([samples, temp_input]).reset_index(drop=True)
    temp_input3 = temp_input2.iloc[1:,0:samples.size] # sample input에 들어 있지 않은 문자열을 삭제하기
    drop_value = temp_input2.iloc[:,samples.size:].columns
    if drop_value.size >=1 :
        print("다음 데이터가 학습 모델에 누락되어 있습니다.")
        for drop_value_i in drop_value:
            print(f"{drop_value_i}")
    Xinput = temp_input3.fillna(0)

    # Normalize하는 작업
    xinput = Xinput.copy()
    xinput[scale_cols] = scaler_alldata.transform(Xinput[scale_cols])

    ##########################################################
    # 예측하기
    df6 = df5.copy()
    df6["SPEC_NO"] = df2["SPEC_NO"]
    # df6.to_csv("Q:\\_Prediction\\df6.csv", mode='w')

    for target in targets:

        reg_nn1 = _DS_data[f"5.FinalModel for MLP(NN)_{target}"]
        reg_XGV1 = _DS_data[f"5.FinalModel for XGV_{target}"]
        reg_RandF1 = _DS_data[f"5.FinalModel for RandF_{target}"]

        df6[f"{target}_PRED"] = (reg_nn1.predict(xinput) + reg_XGV1.predict(Xinput) )/2
        # df6.to_csv("Q:\\_Prediction\\KTcode_withResult.csv", mode='w')
    return df6

def import_spec_from_PLM(specs1):
    credentials = f"{auth.username}/{auth.password}@{auth.host}:{auth.port}/{auth.servicename}/"
    connection = cx_Oracle.connect(credentials, encoding="UTF-8", nencoding="UTF-8")
    # df = pd.DataFrame()  # 모든 정보 추출
    df1 = pd.DataFrame()  # Spec 정보만 추출
    if isinstance(specs1,list):
        for spec_no1 in specs1:
            ################# QUERY #################
            query1 = "SELECT * \
                        FROM enoviaif.tr_plmspec_rcx \
                        WHERE tr_plmspec_rcx.spec_no = " + "'" + str(spec_no1) + "'"
            spec_data = pd.read_sql(query1, connection)
            df1 = pd.concat([df1, spec_data])
    else:
        query1 = f"SELECT * \
                                FROM enoviaif.tr_plmspec_rcx \
                                WHERE tr_plmspec_rcx.spec_no = '{specs1}'"
        spec_data = pd.read_sql(query1, connection)
        df1 = pd.concat([df1, spec_data])
    connection.close()
    # 스펙을 변환하기
    import _PLM_SPEC_CHANGE  # 필요한 스펙으로 변환하는 함수 정의
    df2 = _PLM_SPEC_CHANGE.Change1(df1)

    df2["TEST_LOAD"] = 450
    df2["RIM_WIDTH"] = 7.0
    df2["AIR"] = 2.2
    df2 = df2.copy().reset_index(drop=True)

    df3 = df2[use_cols]
    df3 = df3.dropna()
    df4 = df3.copy().astype('object')  # Data Type을 모두 object로 통일화 하기
    df5 = df4.copy()
    for col in scale_cols:
        df5 = df5.astype({col: 'float16'})
    return df2, df5

_DS_data = pickle.load(open('Z:\\_DATA_Traing\\DS\\_DS_data5.pkl', 'rb'))
scaler_alldata = _DS_data["4.Scaler (with all data)"]
categoricals = _DS_data["4.Category"]
min_max = _DS_data["4.Min_Max information (all data)"]
use_cols = _DS_data["1.Input Properties list"]
scale_cols = _DS_data["1.Input Properties list (number)"]
targets = _DS_data['1.Target list']
all_data = _DS_data['3.Input Data (Removed Outlier)']
samples = _DS_data['4.Input_Sample for New Prediction']
samples = samples.drop(1,0)
allrows = _use_cols.cols
# categoricals dict type 일 경우, 아래 코드 사용
for i in categoricals:
    categoricals[i].sort()
# categoricals dataframe type 일 경우, 아래 코드 사용
# for i in range(categoricals.shape[0]):
#     t1 = categoricals.iloc[i,:].sort_values()
#     categoricals.iloc[i,:] = t1
min_max['min'].round()
np.round(min_max['min'],1)
a = np.round(min_max['min'],1)


#화면을 띄우는데 사용되는 Class 선언
class Main_Window(QMainWindow, Ui_MainWindow) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        # self.showMaximized()

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)


        self.pushButton_1.setEnabled(True) # Import Ref. Spec.
        self.pushButton_2.setDisabled(True) # Plot Scatter
        self.pushButton_3.setDisabled(True)  # Copy From Ref (DOE)
        # self.pushButton_4.setDisabled(True)  # Execute New Window UI
        # self.pushButton_5.setDisabled(True)  # Copy From Ref (Table 1)
        self.pushButton_6.setDisabled(True)  # Calculate DOE

        # 버튼에 기능을 연결하는 코드
        self.pushButton_1.clicked.connect(self.button1Function)
        self.pushButton_2.clicked.connect(self.button2Function)
        self.pushButton_3.clicked.connect(self.button3Function)
        # self.pushButton_5.clicked.connect(self.button5Function)
        self.pushButton_6.clicked.connect(self.button6Function)



        # tableWidget_1
        # Mouse Left Click
        self.tableWidget_1.cellClicked.connect(self.select_cell)
        # Mouse Right Click
        self.tableWidget_1.setContextMenuPolicy(Qt.ActionsContextMenu)
        change_action = QAction("Change Value with Range Box Value", self.tableWidget_1)
        # recalculate_action = QAction("Re-Calculate from changed input value", self.tableWidget_1)
        self.tableWidget_1.addAction(change_action)
        # self.tableWidget_1.addAction(recalculate_action)
        change_action.triggered.connect(self.change_from)
        # recalculate_action.triggered.connect(self.recalculate)

        # tableWidget_3
        # Mouse Left Click
        self.tableWidget_3.cellClicked.connect(self.select_cell3)
        # Mouse Right Click
        self.tableWidget_3.setContextMenuPolicy(Qt.ActionsContextMenu)
        add_action = QAction("Add Value from Range Box", self.tableWidget_3)
        self.tableWidget_3.addAction(add_action)
        add_action.triggered.connect(self.add_to_table3)

    def select_cell(self, row, column):
        item = self.tableWidget_1.item(row, column)
        try:
            value = item.text()
        except:
            value = 'No value'
        label_string = 'Row: ' + str(row) + ', Column: ' + str(column-1) + ', Value: ' + str(value)
        print(label_string)
        global g_row, g_colm, g_value
        g_row = row
        g_colm = column

    def select_cell3(self, row, column):
        item = self.tableWidget_3.item(row, column)
        try:
            value = item.text()
        except:
            value = 'No value'
        label_string = 'Row: ' + str(row) + ', Column: ' + str(column-1) + ', Value: ' + str(value)
        print(label_string)
        global g_row, g_colm, g_value
        g_row = row
        g_colm = column

    def add_to_table3(self):
        print("add add")
        print("add at row " + str(g_row))
        item = allrows[g_row]
        print(item)
        try:
            value = eval(f"self.combo1_{item}.currentText()")
            print(value)
            value2 = self.tableWidget_3.currentItem().text() + ';' + value
            print(value2)
            print(str(g_row))
            print(str(g_colm))
            self.tableWidget_3.setItem(g_row, g_colm, QTableWidgetItem(value2))
        except:
            value2 = self.tableWidget_3.currentItem().text()

    def change_from(self):
        print("copy copy")
        print("copy_spec at row " + str(g_row))
        item = allrows[g_row]
        try:
            value = eval(f"self.combo1_{item}.currentText()")
            self.tableWidget_1.setItem(g_row, g_colm, QTableWidgetItem(str(value)))
        except:
            value = self.tableWidget_1.currentItem().text()

    def cell_changed(self, row, column):
        print(row)

    def recalculate(self):
        print("re calculate all")
        global df5, df6, df7, check_btn5_ck

        if check_btn5_ck == 0:
            df7 = df5.drop(targets[0], axis=1)
        else:
            df7 = df7.copy()

        widget_row = 0
        df_row = 0
        for item in allrows:
            if item in use_cols:
                for i in range(df7.shape[0]):
                    df7.iloc[i,df_row] = self.tableWidget_1.item(widget_row, i + 1).text()
                df_row += 1
            widget_row += 1
        # df7.to_csv("Q:\\df7.csv", mode='w')
        for col in scale_cols:
            df7 = df7.astype({col: 'float16'})

        df6 = prediction_run(targets, ohe, df7, use_cols, scale_cols, samples, scaler_alldata, _DS_data, df2)

        target_row = len(allrows)
        df6_row = len(use_cols) + 1
        for target_i in targets:
            for i in range(df6.shape[0]):
                self.tableWidget_1.setItem(target_row, i + 1,
                                           QTableWidgetItem(str(round(df6.iloc[i, df6_row + 1], 1))))
            target_row += 1
            df6_row += 1

    def keyPressEvent(self, ev):
        if (ev.key() == Qt.Key_C) and (ev.modifiers() & Qt.ControlModifier):
            self.copySelection()

    def copySelection(self):
        selection = self.tableWidget_1.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream).writerows(table)
            QApplication.clipboard().setText(stream.getvalue())

    #btn_1이 눌리면 작동할 함수
    def button1Function(self) :
        global df2, df5, df50, df50_X, df6, df60, check_btn_ck, specs
        check_btn_ck = 1
        specs1 = self.lineEdit_1.text()
        [df2, df5] = import_spec_from_PLM(specs1)
        df5["TEST_LOAD"] = float(self.lineEdit_2.text())
        df5["RIM_WIDTH"] = float(self.lineEdit_3.text())
        df5["AIR"] = float(self.lineEdit_4.text())

        df50 = all_data[(all_data['SIZE_NSW'] == df5['SIZE_NSW'][0]) \
                        & (all_data['SIZE_SERISE'] == df5['SIZE_SERISE'][0]) \
                        & (all_data['SIZE_INCH'] == df5['SIZE_INCH'][0])].reset_index(drop=True)
        df50_X = df50[use_cols]

        df6 = pd.DataFrame()
        df6 = prediction_run(targets, ohe, df5, use_cols, scale_cols, samples, scaler_alldata, _DS_data, df2)

        if df50.shape[0] != 0:
            df60 = pd.DataFrame()
            df60 = prediction_run(targets, ohe, df50_X, use_cols, scale_cols, samples, scaler_alldata, _DS_data, df50)
        else:
            print('동일한 사이즈의 시험 결과가 없습니다.')

        for target in targets:
            print(target)
            exec(f"self.comboBox_select_target.addItem('{target}_PRED')")
        print(specs1)

        self.comboBox_select_target.currentIndexChanged.connect(self.arrangement)

        self.tableWidget_1.setRowCount(len(allrows)+len(targets))
        self.tableWidget_1.setColumnCount(df6.shape[0]+1)
        specs=['Range']
        specs.append(specs1)
        for i in range(len(specs1)):
            self.tableWidget_1.setColumnWidth(i, 120)
        self.tableWidget_1.setHorizontalHeaderLabels(specs)
        self.tableWidget_1.setVerticalHeaderLabels(allrows+targets)
        self.tableWidget_1.resizeRowsToContents()

        row = 0
        for item in allrows:
            if item in use_cols:
                if item in categoricals:
                    exec(f"self.combo1_{item}=QComboBox()")
                    for item_item in categoricals[item]:
                        exec(f"self.combo1_{item}.addItem('{item_item}')")
                    exec(f"self.tableWidget_1.setCellWidget(row, 0, self.combo1_{item})")
                    for i in range(df6.shape[0]):
                        self.tableWidget_1.setItem(row, i + 1, QTableWidgetItem(str(df6[item][i])))
                        if df6[item][i] != df6[item][0]:
                            self.tableWidget_1.item(row, i+1).setBackground(QColor(143,188,143))
                        if df6[item][i] in categoricals[item]:
                            pass
                            # self.tableWidget_1.item(row, i+1).setForeground(QColor(0,0,0)) # 글색 변경
                        else:
                            self.tableWidget_1.item(row, i+1).setForeground(QColor(255,0,0))
                else:
                    min = min_max['min'][min_max['list'].index(item)]
                    max = min_max['max'][min_max['list'].index(item)]
                    print(round(max,1))
                    self.tableWidget_1.setItem(row, 0, QTableWidgetItem(str(f"{round(float(min),1)} ~ {round(float(max),1)}")))
                    for i in range(df6.shape[0]):
                        self.tableWidget_1.setItem(row, i+1, QTableWidgetItem(str(df6[item][i])))
                        if df6[item][i] < min and df6[item][i] > max:
                            self.tableWidget_1.item(row, i + 1).setForeground(QColor(255, 0, 0))
                        if df6[item][i] != df6[item][0]:
                            self.tableWidget_1.item(row, i+1).setBackground(QColor(143,188,143))
            row += 1

        target_row = len(allrows)
        df6_row = len(use_cols) + 1
        for target_i in targets:
            for i in range(df6.shape[0]):
                self.tableWidget_1.setItem(target_row, i + 1, QTableWidgetItem(str(round(df6.iloc[i,df6_row+1],1))))
                # print( df6.iloc[i, df6_row+1] )
                # print(round(df6.iloc[i, df6_row + 1], 1))
            target_row += 1
            df6_row += 1

        self.pushButton_1.setEnabled(True) # Import Ref. Spec.
        self.pushButton_2.setEnabled(True) # Plot Scatter
        self.pushButton_3.setEnabled(True)  # Copy From Ref (DOE)
        # self.pushButton_4.setDisabled(True)  # Execute New Window UI
        # self.pushButton_5.setEnabled(True)  # Copy From Ref (Table 1)
        self.pushButton_6.setDisabled(True)  # Calculate DOE

    def button2Function(self) :
        if df50.shape[0] != 0:
            x = df50['DYNAMINC_STIFFNESS']
            y = df60['DYNAMINC_STIFFNESS_PRED']
            x1 = df6['DYNAMINC_STIFFNESS_PRED']
            y1 = df6['DYNAMINC_STIFFNESS_PRED']
            self.MplWidget_1.canvas.axes.clear()
            self.MplWidget_1.canvas.axes.scatter(x, y, c='black')
            self.MplWidget_1.canvas.axes.scatter(x1, y1, c='red')
            self.MplWidget_1.canvas.axes.set_title('Scatter Plot')
            self.MplWidget_1.canvas.draw()
            now = datetime.now()
            time_id = f"{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}"
            df50.to_csv(f"z:\\_Tool_TPC\\DS_Data_{time_id}.csv", mode='w')
        else:
            x1 = df6['DYNAMINC_STIFFNESS_PRED']
            y1 = df6['DYNAMINC_STIFFNESS_PRED']
            self.MplWidget_1.canvas.axes.clear()
            self.MplWidget_1.canvas.axes.scatter(x1, y1, c='red')
            self.MplWidget_1.canvas.axes.set_title('Scatter Plot')
            self.MplWidget_1.canvas.draw()


    def button3Function(self) :
        self.tableWidget_3.setRowCount(len(allrows))
        self.tableWidget_3.setColumnCount(1)
        self.tableWidget_3.resizeRowsToContents()
        self.tableWidget_3.setColumnWidth(0, 300)

        print("copy from reference")
        widget_row = 0
        df_row = 0
        for item in allrows:
            if item in use_cols:
                tmp = self.tableWidget_1.item(widget_row, 1).text()
                # print(str(self.tableWidget_1.item(widget_row, 1).text()))
                self.tableWidget_3.setItem(widget_row, 0, QTableWidgetItem(tmp))
                df_row += 1
            widget_row += 1
        self.pushButton_6.setEnabled(True)  # Calculate DOE

    def button5Function(self) :
        global specs, new_spec_no, df5, df7, check_btn5_ck
        df5_1 = df5.drop(targets[0], axis=1)
        if check_btn5_ck == 0:
            df7 = pd.concat([df5_1, df5_1], axis=0)
        else:
            df7 = pd.concat([df7.copy(), df5_1], axis=0)

        specs.append(f"New {new_spec_no}")
        self.tableWidget_1.setColumnCount(len(specs))
        for i in range(len(specs)):
            self.tableWidget_1.setColumnWidth(i, 120)
        self.tableWidget_1.setHorizontalHeaderLabels(specs)
        self.tableWidget_1.setVerticalHeaderLabels(allrows+targets)
        self.tableWidget_1.resizeRowsToContents()
        print("copy from reference")
        print(specs)
        widget_row = 0
        df_row = 0
        for item in allrows:
            if item in use_cols:
                tmp = self.tableWidget_1.item(widget_row, 1).text()
                # print(str(self.tableWidget_1.item(widget_row, 1).text()))
                self.tableWidget_1.setItem(widget_row, new_spec_no+1, QTableWidgetItem(tmp))
                df_row += 1
            widget_row += 1
        new_spec_no = new_spec_no + 1
        check_btn5_ck = check_btn5_ck +1

    def button6Function(self) :
        global specs, new_spec_no, df5, df7, doe_items, df_doe, df4_1, col_names, effects
        doe_items = []
        widget_row = 0
        df_row = 0
        for item in allrows:
            if item in use_cols:
                tmp = self.tableWidget_3.item(widget_row, 0).text()
                print(item)
                tmp1 = tmp.split(';')
                if len(tmp1) > 1:
                    doe_items.append((item, tmp1))
                df_row += 1
            widget_row += 1
        print(doe_items)

        col_names = []
        levels_list = []
        for column in doe_items:
            levels_list.append(len(column[1]))
            col_names.append(column[0])
        levels=np.array(levels_list)

        n = len(levels)  # number of factors
        nb_lines = np.prod(levels)  # number of trial conditions
        H = np.zeros((nb_lines, n))

        level_repeat = 1
        range_repeat = np.prod(levels)
        for i in range(n):
            range_repeat = range_repeat // levels[i]
            lvl = []
            for j in range(levels[i]):
                lvl += [j] * level_repeat
            rng = lvl * range_repeat
            level_repeat = level_repeat * levels[i]
            H[:, i] = rng

        df_doe = H
        df_doe = pd.DataFrame(H, columns = col_names)
        i = 0
        for colmn in col_names:
            # print(i)
            for j in range(int(levels[i])):
                # print(j)
                df_doe[colmn] = df_doe.copy()[colmn].replace(j, doe_items[i][1][j] )
            i = i + 1

        for col in use_cols:
            if col not in col_names:
                df_doe[col] = df5[col][0]

        df4_1 = df_doe.astype('object')  # Data Type을 모두 object로 통일화 하기
        for col in scale_cols:
            df4_1 = df4_1.astype({col: 'float16'})

        df_doe = prediction_run(targets, ohe, df4_1, use_cols, scale_cols, samples, scaler_alldata, _DS_data, df2)
        print('Done')

        if df50.shape[0] != 0:
            x = df50['DYNAMINC_STIFFNESS']
            y = df60['DYNAMINC_STIFFNESS_PRED']
            x1 = df_doe['DYNAMINC_STIFFNESS_PRED']
            y1 = df_doe['DYNAMINC_STIFFNESS_PRED']

            self.MplWidget_2.canvas.axes.clear()
            self.MplWidget_2.canvas.axes.scatter(x, y, c='black')
            self.MplWidget_2.canvas.axes.scatter(x1, y1, c='red')
            self.MplWidget_2.canvas.axes.set_title('Scatter Plot')
            self.MplWidget_2.canvas.draw()
        else:
            x1 = df_doe['DYNAMINC_STIFFNESS_PRED']
            y1 = df_doe['DYNAMINC_STIFFNESS_PRED']
            self.MplWidget_2.canvas.axes.clear()
            self.MplWidget_2.canvas.axes.scatter(x1, y1, c='red')
            self.MplWidget_2.canvas.axes.set_title('Scatter Plot')
            self.MplWidget_2.canvas.draw()

        self.tableWidget_2.setRowCount(len(allrows)+len(targets))
        self.tableWidget_2.setColumnCount(5)
        for i in range(5):
            self.tableWidget_2.setColumnWidth(i, 80)
        self.tableWidget_2.setVerticalHeaderLabels(allrows+targets)
        self.tableWidget_2.setHorizontalHeaderLabels(['Contribution','Lowest 1','Lowest 2','Lowest 3','Lowest 4'])
        self.tableWidget_2.resizeRowsToContents()
        print(self.comboBox_select_target.currentText())
        # df_doe_top = df_doe.sort_values(by=[self.comboBox_select_target.currentText()], ascending=[False])
        df_doe_bot = df_doe.sort_values(by=[self.comboBox_select_target.currentText()], ascending=[True])
        print('f')
        df_row = 0
        for item in allrows:
            if item in use_cols:
                for i in range(4):
                    self.tableWidget_2.setItem(df_row, i+1, QTableWidgetItem(str(df_doe_bot[item][i])))
                    # self.tableWidget_2.setItem(df_row, i+3, QTableWidgetItem(str(df_doe_bot[item][i])))
            df_row += 1
        target_row = len(allrows)
        df6_row = len(use_cols) + 1
        for target_i in targets:
            for i in range(4):
                self.tableWidget_2.setItem(target_row, i+1, QTableWidgetItem(str(round(df_doe_bot.iloc[i, df6_row + 1], 1))))
                # self.tableWidget_2.setItem(target_row, i+3, QTableWidgetItem(str(round(df_doe_bot.iloc[i, df6_row + 1], 1))))
            target_row += 1
            df6_row += 1

        targets1=[]
        for target_i in targets:
            targets1.append(target_i + '_PRED')

        effects = {}
        effects[0] = {}
        for target_i in targets1:
            # Start with the constant effect: this is $\overline{y}$
            effects[0][target_i] = df_doe[f"{target_i}"].mean()

        effects[1] = {}
        df_row = 0
        for item in allrows:
            if item in col_names:
                # print(item)
                effects_result = []
                for target_i in targets1:
                    effects_df = df_doe.groupby(item)[target_i].mean()
                    result = effects_df.values.max() - effects_df.values.min()
                    effects_result.append(result)
                effects[1][item] = effects_result

        targets1_index = targets1.index(self.comboBox_select_target.currentText())
        targets1_value = self.comboBox_select_target.currentText()

        row = 0
        for item in allrows:
            if item in use_cols:
                if item in col_names:
                    exec(f"self.pbar_{item}=QProgressBar()")
                    valuei = effects[1][item][targets1_index] / effects[0][targets1_value] *100
                    exec(f"self.pbar_{item}.setValue(valuei)")
                    exec(f"self.tableWidget_2.setCellWidget(row, 0, self.pbar_{item})")
            row = row + 1

        now = datetime.now()
        time_id = f"{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}"
        df_doe.to_csv(f"z:\\_Tool_TPC\\DS_DOE_{time_id}.csv", mode='w')

    def arrangement(self):
        global effects, col_names
        print('arrangement')
        print(self.comboBox_select_target.currentText())
        # df_doe_top = df_doe.sort_values(by=[self.comboBox_select_target.currentText()], ascending=[False])
        df_doe_bot = df_doe.sort_values(by=[self.comboBox_select_target.currentText()], ascending=[True])
        print('f')
        df_row = 0
        for item in allrows:
            if item in use_cols:
                for i in range(4):
                    self.tableWidget_2.setItem(df_row, i+1, QTableWidgetItem(str(df_doe_bot[item][i])))
                    # self.tableWidget_2.setItem(df_row, i+3, QTableWidgetItem(str(df_doe_bot[item][i])))
            df_row += 1
        target_row = len(allrows)
        df6_row = len(use_cols) + 1
        for target_i in targets:
            for i in range(4):
                self.tableWidget_2.setItem(target_row, i+1,
                                           QTableWidgetItem(str(round(df_doe_bot.iloc[i, df6_row + 1], 1))))
                # self.tableWidget_2.setItem(target_row, i+3, QTableWidgetItem(str(round(df_doe_bot.iloc[i, target_row + 1], 1))))
            target_row += 1
            df6_row += 1

        targets1=[]
        for target_i in targets:
            targets1.append(target_i + '_PRED')

        targets1_index = targets1.index(self.comboBox_select_target.currentText())
        targets1_value = self.comboBox_select_target.currentText()

        row = 0
        for item in allrows:
            if item in use_cols:
                if item in col_names:
                    exec(f"self.pbar_{item}=QProgressBar()")
                    valuei = effects[1][item][targets1_index] / effects[0][targets1_value] *100
                    exec(f"self.pbar_{item}.setValue(valuei)")
                    exec(f"self.tableWidget_2.setCellWidget(row, 0, self.pbar_{item})")
            row = row + 1
        temp_txt1 = self.comboBox_select_target.currentText()
        temp_txt2 = temp_txt1[:-5]
        if df50.shape[0] != 0:
            x = df50[temp_txt2]
            y = df60[temp_txt1]
            x1 = df_doe[temp_txt1]
            y1 = df_doe[temp_txt1]
            self.MplWidget_2.canvas.axes.clear()
            self.MplWidget_2.canvas.axes.scatter(x, y, c='black')
            self.MplWidget_2.canvas.axes.scatter(x1, y1, c='red')
            self.MplWidget_2.canvas.axes.set_title(temp_txt1)
            self.MplWidget_2.canvas.draw()
        else:
            x1 = df_doe[temp_txt1]
            y1 = df_doe[temp_txt1]
            self.MplWidget_2.canvas.axes.clear()
            self.MplWidget_2.canvas.axes.scatter(x1, y1, c='red')
            self.MplWidget_2.canvas.axes.set_title(temp_txt1)
            self.MplWidget_2.canvas.draw()

# class Sub_Window1(QMainWindow,Ui_SubWindow1):
#   def __init__(self):
#     super(Sub_Window1, self).__init__()
#     self.setupUi(self)
#     # self.pushButton_4.clicked.connect(self.close)
#   def OPEN(self):
#     self.show()


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #Main의 인스턴스 생성
    main = Main_Window()
    # ch = Sub_Window1()

    #프로그램 화면을 보여주는 코드
    main.show()
    # main.firstAction()
    # main.pushButton_4.clicked.connect(ch.OPEN)

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
    # sys.exit(app.exec_())