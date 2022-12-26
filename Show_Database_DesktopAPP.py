from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import *
import numpy as np
import pandas as pd

# https://youtu.be/WXKypkhjY84
# Here is my youtube video link where I explain this code one by one

dfC = pd.read_csv("Temiz.csv", usecols = ['Product','Issue','Company','State','Complaint ID','ZIP code'])
dfC["Complaint ID"]= dfC["Complaint ID"].astype(str)
df = dfC[:10000].copy()

class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("untitledC.ui", self)
        self.show()

        self.pushButton.clicked.connect(self.df_visualize)

        self.pushButton_2.clicked.connect(self.df_clear)


    # def df_visualize(self):
    #     arr = df.to_numpy()
    #     for r in range(len(arr)):
    #         self.tableWidget.insertRow(r)
    #         for k in range(6):
    #             self.tableWidget.setItem(r,k,QTableWidgetItem(str(arr[r][k])))

    def df_visualize(self):
        for r in range(len(df['Complaint ID'])):
            self.tableWidget.insertRow(r)
            for k in range(6):
                self.tableWidget.setItem(r,k,QTableWidgetItem(str(df.loc[r][k])))            

    def df_clear(self):
        for i in range(self.tableWidget.rowCount()):
            # self.tableWidget.removeRow(0)
            self.tableWidget.clear()

def main():
    app = QApplication([])
    window= MyGUI()
    app.exec_()

if __name__ == '__main__':
   main()
