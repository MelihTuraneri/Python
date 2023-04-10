from PyQt5.QtWidgets import *
import sys, threading, queue, time
from PyQt5 import uic,QtWidgets
import numpy as np
import pandas as pd
import concurrent.futures
import logging
from numba import njit

df = pd.read_csv("Temiz.csv", usecols = ['Product','Issue','Company','State','Complaint ID','ZIP code'])
df["Complaint ID"]= df["Complaint ID"].astype(str)
sonuc_list = []
thread_start = []
thread_end = []
threash_list = []

class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("untitled.ui", self)
        self.show()

        self.pushButton.clicked.connect(self.ARAMA)

        self.pushButton_2.clicked.connect(self.text_search) 

        self.checkBox.stateChanged.connect(self.checked_item)

        self.checkBox_2.stateChanged.connect(self.checked_item_2)

        self.comboBox.activated.connect(self.combocu)

        self.comboBox_5.activated.connect(self.combocu2)

    def text_search(self):
        self.comboBox_2.insertItem(0, self.lineEdit.text())
        
    def combocu(self):
        self.comboBox_2.clear()
        Kolon_asil = self.comboBox.currentText()
        if Kolon_asil != "Complaint ID":
            for i in df[Kolon_asil].value_counts().index.tolist():
                self.comboBox_2.addItem(i)
        else:
            self.comboBox_2.addItem("Belirtilmemiş")

    def combocu2(self):
        self.comboBox_7.clear()
        Kolon_asil = self.comboBox_5.currentText()
        if Kolon_asil != "Complaint ID":
            for i in df[Kolon_asil].value_counts().index.tolist():
                self.comboBox_7.addItem(i)  
        else:
            self.comboBox_7.addItem("Belirtilmemiş")
    
    def checked_item(self):
        if self.checkBox.isChecked():
            self.comboBox_5.setEnabled(True)
            self.comboBox_6.setEnabled(True)
            if self.checkBox_2.isChecked():
                self.comboBox_7.setEnabled(True)
            self.comboBox_8.setEnabled(True)
        else:
            self.comboBox_5.setEnabled(False)
            self.comboBox_6.setEnabled(False)
            self.comboBox_7.setEnabled(False)
            self.comboBox_8.setEnabled(False)

    def checked_item_2(self):
        if self.checkBox_2.isChecked():
            self.comboBox_2.setEnabled(True)
            if self.comboBox_6.isEnabled():
                self.comboBox_7.setEnabled(True)
        else:
            self.comboBox_2.setEnabled(False)
            self.comboBox_7.setEnabled(False)  

    def ARAMA(self):
        df_yeni = df.copy()
        le_func_jitted = njit(islem, nogil=True)
        clear_table(self)
        self.textBrowser_2.clear()
        sonuc_list.clear()
        if self.checkBox.isChecked():
            if self.comboBox_2.currentText() == "Belirtilmemiş" or self.comboBox_3.currentText() == "Belirtilmemiş" or self.comboBox_4.currentText() == "Belirtilmemiş" or self.comboBox_7.currentText() == "Belirtilmemiş" or self.comboBox_6.currentText() == "Belirtilmemiş" or self.comboBox_8.currentText() == "Belirtilmemiş":
                self.textBrowser_2.setEnabled(False)
                self.label_3.setText("Lütfen kutucukları eksiksiz doldurunuz!!")
                
            else:
                self.textBrowser_2.setEnabled(True)
                self.label_3.setText("Başarılı!!")

                combo_mod = 0
                search_mod = 0
                if self.checkBox_2.isChecked():
                    search_mod = 1
                pre_war_recipe(self, df_yeni,search_mod,combo_mod)

                df_yeni = df.loc[sonuc_list, :]
                df_yeni.reset_index(drop = True,inplace = True)

                sonuc_list.clear()
                thread_start.clear()
                thread_end.clear()

                combo_mod = 1
                search_mod = 0
                pre_war_recipe(self, df_yeni, search_mod,combo_mod)  

                arr = df_yeni.loc[sonuc_list, :].to_numpy()
                for r in range(len(arr)):
                    # self.tableWidget.insertRow(r)
                    for k in range(6):
                        self.tableWidget.setItem(r,k+1,QTableWidgetItem(str(arr[r][k])))
                        if k == 0:
                            self.tableWidget.setItem(r,k,QTableWidgetItem(str(threash_list[r]))) 

                sonuc_list.clear()
                thread_start.clear()
                thread_end.clear()
                threash_list.clear()
        else:
            if self.comboBox_2.currentText() == "Belirtilmemiş" or self.comboBox_3.currentText() == "Belirtilmemiş" or self.comboBox_4.currentText() == "Belirtilmemiş":
                self.textBrowser_2.setEnabled(False)
                self.label_3.setText("Lütfen kutucukları eksiksiz doldurunuz!!")
                
            else:
                self.textBrowser_2.setEnabled(True)
                self.label_3.setText("Başarılı!!")
                combo_mod = 0
                search_mod = 0
                if self.checkBox_2.isChecked():
                    search_mod = 1
                pre_war_recipe(self, df_yeni,search_mod,combo_mod)  

                arr = df_yeni.loc[sonuc_list, :].to_numpy()
                for r in range(len(arr)):
                    # self.tableWidget.insertRow(r)
                    for k in range(6):
                        self.tableWidget.setItem(r,k+1,QTableWidgetItem(str(arr[r][k])))
                        if k == 0:
                            self.tableWidget.setItem(r,k,QTableWidgetItem(str(threash_list[r])))

                sonuc_list.clear()
                thread_start.clear()
                thread_end.clear()
                threash_list.clear()
#--------------------------------------------------------------------------------------------------------------------------------------------------------

def pre_war_recipe(self, df_yeni, search_mod, combo_mod):
    # q = queue.Queue()
    
    if combo_mod == 0:
        Kolon = self.comboBox.currentText()
        kayit_girisi = self.comboBox_2.currentText()
        thread_num = int(self.comboBox_3.currentText())
        Tresh= int(self.comboBox_4.currentText())
    else:    
        Kolon = self.comboBox_5.currentText()
        kayit_girisi = self.comboBox_7.currentText()
        thread_num = int(self.comboBox_6.currentText())
        Tresh= int(self.comboBox_8.currentText())

    if Kolon == "Complaint ID":
        kayit_girisi = str(df[df["Complaint ID"] == kayit_girisi].Issue.values[0])
        Kolon = "Issue"

    if search_mod == 1:
        with concurrent.futures.ThreadPoolExecutor(max_workers = thread_num) as executor:
                executor.submit(islem(1,Tresh,kayit_girisi,Kolon,df_yeni))
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers = thread_num) as executor:
            thread_name = 0
            for index in df[Kolon].value_counts().index.tolist():
                thread_name = thread_name + 1
                executor.submit(islem,thread_name,Tresh,index,Kolon,df_yeni)    
        
    # islem("Thread-{0}",q,Tresh,Kolon,df_yeni)

    for i in thread_start:
        self.textBrowser_2.append(i)

    self.textBrowser_2.append("\n-----------------------------------")

    for i in thread_end:
        self.textBrowser_2.append(i)  

    thread_start.clear()
    thread_end.clear()    

def clear_table(self):
    self.tableWidget.clear()

def islem(threadName,tresHold,kayit_girisi,Kolon,df):
        format = "%(asctime)s : %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")
        clk_ides = time.CLOCK_THREAD_CPUTIME_ID    
        t2 = time.clock_gettime(clk_ides)
        thread_start.append(logging.info("Thread Started"))
        thread_start.append("{} Başlangıç Zamanı : {}".format(threadName,t2))
        kayit = kayit_girisi
        for i in range(len(df["Product"])):
            karsilastirilan_satir = df[Kolon][i]
            donusturulmus_kayit = kayit.split()
            ayni_kelime_sayisi = 0
            if kayit == karsilastirilan_satir:
                ayni_kelime_sayisi = len(donusturulmus_kayit)
                sonuc_list.append(i)
                threash_list.append(100)
            else:  
                for arama in donusturulmus_kayit:
                    if karsilastirilan_satir.find(arama) != - 1:
                        ayni_kelime_sayisi = ayni_kelime_sayisi + 1
                donusturulmus_satir = karsilastirilan_satir.split()
                if ayni_kelime_sayisi == 0:
                    benzerlik_orani = float(0)
                elif len(donusturulmus_kayit) > len(donusturulmus_satir):
                    benzerlik_orani = float(ayni_kelime_sayisi/len(donusturulmus_kayit))
                elif len(donusturulmus_satir) > len(donusturulmus_kayit):
                    benzerlik_orani = float(ayni_kelime_sayisi/len(donusturulmus_satir))
                elif len(donusturulmus_satir) == len(donusturulmus_kayit):
                    benzerlik_orani = float(ayni_kelime_sayisi/len(donusturulmus_satir))
                if benzerlik_orani*100 >= tresHold:
                    sonuc_list.append(i)
                    threash_list.append(float(benzerlik_orani*100))
        print(kayit)            
        # q.task_done()  
        format = "%(asctime)s"
        logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")
        clk_ide = time.CLOCK_THREAD_CPUTIME_ID    
        t2 = time.clock_gettime(clk_ide)
        thread_end.append(logging.info("Thread ended"))
        thread_end.append("{} Bitiş Zamanı : {}".format(threadName,t2))

def main():
    app = QApplication([])
    window= MyGUI()
    app.exec_()

if __name__ == '__main__':
   main()
