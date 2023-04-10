from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import *
import numpy as np
import pandas as pd
import matplotlib.pylab as plt

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self,final_df):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)

        layout = QtWidgets.QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure(figsize=(10, 8)))
        layout.addWidget(NavigationToolbar(static_canvas, self))
        layout.addWidget(static_canvas)

        self._static_ax = static_canvas.figure.subplots()
        
        bar_labels = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'gray', 'cyan']
        bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:purple', 'tab:brown', 'tab:gray', 'tab:cyan']

        self._static_ax.bar(x = final_df["Grade"].value_counts().sort_index().index, height = final_df["Grade"].value_counts().sort_index().values, label=bar_labels, color=bar_colors)
        self._static_ax.set_title("Başarı Tablosu", fontsize=20)
        self._static_ax.set_ylabel('Count', fontsize=15)
        self._static_ax.set_xlabel('Grade', fontsize=15)
        self._static_ax.set_yticks(final_df["Grade"].value_counts().sort_index().values)
        self._static_ax.legend(title='Grades')

class ApplicationWindow2(QtWidgets.QMainWindow):
    def __init__(self,final_df):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)

        layout = QtWidgets.QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure(figsize=(20, 12)))
        layout.addWidget(NavigationToolbar(static_canvas, self))
        layout.addWidget(static_canvas)

        final_df['T-Puan'] = pd.to_numeric(final_df['T-Puan'])
        hist_list = []
        toplam = 0
        for i in range(50):
            if i != 0:
                hist_list.append(len(final_df[final_df['T-Puan'] <= (i+1)*2]["T-Puan"]) - toplam)
                toplam = len(final_df[final_df['T-Puan'] <= (i+1)*2]["T-Puan"])
            else:
                hist_list.append(len(final_df[final_df['T-Puan'] <= (i+1)*2]["T-Puan"]))
                toplam = toplam + len(final_df[final_df['T-Puan'] <= (i+1)*2]["T-Puan"])

        self._static_ax = static_canvas.figure.subplots()
        self._static_ax.bar(x = np.arange(0,100,2), height = hist_list, edgecolor="white")
        self._static_ax.set_xticks(np.arange(4,104,4))
        self._static_ax.set_yticks(np.arange(0,20,1))
                

class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("grade_calculator_tool/UU.ui", self)
        self.show()

        self.pushButton.clicked.connect(self.csv_browse)

        self.pushButton_2.clicked.connect(self.download_csv)

        self.pushButton_3.clicked.connect(self.grade_graph)

        self.pushButton_4.clicked.connect(self.tpuan_graph)

    def grade_graph(self):
        final_df = create_final_df(self)
        self.dialog = ApplicationWindow(final_df)
        self.dialog.show()

    def tpuan_graph(self):
        final_df = create_final_df(self)
        self.dialog = ApplicationWindow2(final_df)
        self.dialog.show()    

    def csv_browse(self):
        clear_tables(self)
        df = pd.DataFrame()
        df_height, df = self.open_dialog_box(df,)
        if df_height == 0 and df == 0:
            return 0
        class_dsn_std = df.describe().T["std"][0]
        class_dsn_avg = df.describe().T["mean"][0]
        calculate(df, class_dsn_std, class_dsn_avg, df_height, self)
        for r in range(df_height):
            self.tableWidget.insertRow(r)
            for k in range(3):
                self.tableWidget.setItem(r,k,QTableWidgetItem(str(df.loc[r][k]))) 

    def open_dialog_box(self, df):
        filename = QFileDialog.getOpenFileName(filter = '*.csv')
        path = filename[0]
        if path != "":
            df = pd.read_csv(path) 
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            return df.shape[0],df
        else:
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            return 0,0

    def download_csv(self):
        final_df = create_final_df(self)
        filename = QFileDialog.getExistingDirectory()  
        if filename != "":                       
            final_df.to_csv(filename + "/final_data2.csv", index=False)

def create_final_df(self):
    final_df = pd.DataFrame(columns=["First Name", "Last Name", "T-Puan", "Grade"])
    for r in range(self.tableWidget_4.rowCount()):
        final_df.loc[len(final_df)] = [self.tableWidget_4.item(r,0).text(), self.tableWidget_4.item(r,1).text(),
                                        self.tableWidget_4.item(r,2).text(), self.tableWidget_4.item(r,3).text()]
    return final_df

def clear_tables(self):
    for r in range(self.tableWidget.rowCount()):
        self.tableWidget.removeRow(0)
        self.tableWidget_4.removeRow(0)

def calculate(df, class_dsn_std, class_dsn_avg, df_height, self):
    if df_height != 0:
        t_list = []
        grade_list = []
        for student_avg in df["Puan"]:
            t_puan = ((student_avg - class_dsn_avg)/(class_dsn_std))*10 + 50
            t_list.append(t_puan)
            grade = class_grade_calculator(t_puan, class_dsn_avg)
            grade_list.append(grade)
        new_df_visualizer(t_list, df, grade_list, self)

def new_df_visualizer(t_list, df, grade_list, self):
    df_dict = {"First Name" : df["First Name"],
            "Last Name" : df["Last Name"],
            "T-PUAN" : t_list,
            "Grade" : grade_list}
    final_df = pd.DataFrame(data = df_dict)
    for r in range(final_df.shape[0]):
            self.tableWidget_4.insertRow(r)
            for k in range(4):
                self.tableWidget_4.setItem(r,k,QTableWidgetItem(str(final_df.loc[r][k]))) 

    
def class_grade_calculator(x, class_dsn_avg):
    if 80 <= class_dsn_avg and class_dsn_avg <= 100:
        if x < 30: 
            grade = "FF"
        elif 90 <= x and x <= 100:
            grade = "AA"
        elif 80 <= x and x < 90:
            grade = "BA"
        elif 75 <= x and x < 80:
            grade = "BB"
        elif 70 <= x and x < 75:
            grade = "CB"
        elif 60 <= x and x < 70:
            grade = "CC"
        elif 50 <= x and x < 60:
            grade = "DC"
        elif 40 <= x and x < 50:
            grade = "DD"
        elif 30 <= x and x < 40:
            grade = "FD"
            
    elif 70 < class_dsn_avg and class_dsn_avg < 80:
        return student_grade_calculator(x,24)
        
    elif 62.5 < class_dsn_avg and class_dsn_avg <= 70:
        return student_grade_calculator(x,26)
        
    elif 57.5 < class_dsn_avg and class_dsn_avg <= 62.5:
        return student_grade_calculator(x,28)
        
    elif 52.5 < class_dsn_avg and class_dsn_avg <= 57.5:
        return student_grade_calculator(x,30)
        
    elif 47.5 < class_dsn_avg and class_dsn_avg <= 52.5:
        return student_grade_calculator(x,32)
        
    elif 42.5 < class_dsn_avg and class_dsn_avg <= 47.5:
        return student_grade_calculator(x,34)
        
    elif class_dsn_avg and 42.5:
        return student_grade_calculator(x,36)
    

def student_grade_calculator(x,cgc):
    if x < cgc: 
        grade = "FF"
    elif cgc <= x and x <= (cgc+5-0.01):
        grade = "FD"
    elif (cgc+5) <= x and x <= (cgc+10-0.01):
        grade = "DD"
    elif (cgc+10) <= x and x <= (cgc+15-0.01):
        grade = "DC"
    elif (cgc+15) <= x and x <= (cgc+20-0.01):
        grade = "CC"
    elif (cgc+20) <= x and x <= (cgc+25-0.01):
        grade = "CB"
    elif (cgc+25) <= x and x <= (cgc+30-0.01):
        grade = "BB"
    elif (cgc+30) <= x and x <= (cgc+35-0.01):
        grade = "BA"
    elif (cgc+35) <= x:
        grade = "AA"
    return grade


def main():
    app = QApplication([])
    window= MyGUI()
    app.exec_()

if __name__ == '__main__':
   main()
