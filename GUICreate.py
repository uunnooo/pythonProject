from MakeGUI import MyApp
from PyQt5.QtWidgets import QListWidget, QPushButton, QLabel, QGridLayout

listTestItem = ['FT', 'ST', 'FS']
listTireSpec = ['TireInfor', 'CMP', 'CCS', 'BT1', 'BT2', 'JLC', 'BF', 'PCI', 'ETC', 'SPECALL']

class CreateGUI(MyApp):

    def CreateLWTestItem(MyApp):
        ## Test Item 선택 추후 멀티 선택 가능하게
        LWTestItem = QListWidget()
        LWTestItem.setSortingEnabled(True)
        listCount = 0
        for testItem in listTestItem:
            LWTestItem.insertItem(listCount, testItem)
            listCount = + 1
        LWTestItem.clicked.connect(MyApp.clickedLTI)
        return LWTestItem

    ## Tire Design Paramter 선택
    def CreateLWTireSpecMainPart(MyApp):
        LWTireSpecMainPart = QListWidget()
        LWTireSpecMainPart.setSortingEnabled(True)
        listCount = 0
        for TireSpec in listTireSpec :
            LWTireSpecMainPart.insertItem(listCount, TireSpec)
            listCount = + 1
        LWTireSpecMainPart.clicked.connect(MyApp.clickedLTS)
        return LWTireSpecMainPart


