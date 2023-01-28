from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import pymongo
from bson.objectid import ObjectId
from datetime import datetime


client = pymongo.MongoClient('<your updated connection string>')
#db = client.<your_db_name>
#personCollection = db.<your_collection_name>

#---------------------------------------------------------------------------------------------------------------------------
# update appointment panel
class update_app(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("barber_app/update.ui", self)
        self.show()
        
        self.pushButton.clicked.connect(self.duzenle)

        self.pushButton_2.clicked.connect(self.ara)

        self.pushButton_3.clicked.connect(self.sil)
        
        self.comboBox.activated.connect(self.combo_box)
        self.comboBox_2.activated.connect(self.combo_box)
        self.comboBox_3.activated.connect(self.combo_box)
        self.comboBox_4.activated.connect(self.combo_box)
    
    def combo_box(self):
            combocu(self)

    def ara(self):
        if self.lineEdit_4.text() == "":
            self.label_12.setText("Randevu No giriniz!!")
            self.pushButton.setEnabled(False)
            self.pushButton_3.setEnabled(False)
        else:
            self.pushButton.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            doc = personCollection.find_one({"_id" : ObjectId(self.lineEdit_4.text())})
            self.lineEdit.setText(doc["name"])
            self.lineEdit_2.setText(doc["surname"])
            self.lineEdit_3.setText(str(doc["age"]))
            #self.lineEdit_3.setText(str(doc["datetime"]["hour"]) + "." + str(doc["datetime"]["minute"]))
            self.comboBox.setCurrentText(doc["hair_cut"])
            self.comboBox_2.setCurrentText(doc["beard_cut"])
            self.comboBox_3.setCurrentText(doc["nape_cut"])
            self.comboBox_4.setCurrentText(doc["hair_wash"])
            self.comboBox_5.setCurrentText(doc["datetime"]["hour"])
            self.comboBox_6.setCurrentText(doc["datetime"]["minute"])
            self.label_8.setText(str(doc["charge"]) + " TL")
            self.calendarWidget.setSelectedDate(QDate(doc["datetime"]["year"],doc["datetime"]["month"],doc["datetime"]["day"]))
     
    def duzenle(self):
        if self.lineEdit_4.text() == "":
            self.label_12.setText("Randevu No giriniz!!")
            self.pushButton.setEnabled(False)
            self.pushButton_3.setEnabled(False)
        elif self.lineEdit.text() == "" or self.lineEdit_2.text() == "" or self.lineEdit_3.text() == "" or self.comboBox.currentText() == "Saç Kesimi" or self.comboBox_2.currentText() == "Sakal Kesimi" or self.comboBox_3.currentText() == "Ense Kesimi" or self.comboBox_4.currentText() == "Yıkama" or self.comboBox_5.currentText() == "Saat" or self.comboBox_6.currentText() == "Dakika":
            self.label_11.setText("Lütfen kutucukları eksiksiz doldurunuz!!")
        else:
            self.label_11.setText("Başarılı!!")
            doc = {"state" : "beklemede", "name" : self.lineEdit.text(), "surname" : self.lineEdit_2.text(),"age": int(self.lineEdit_3.text()),
                    "hair_cut" : self.comboBox.currentText(), "beard_cut" : self.comboBox_2.currentText(),
                    "nape_cut" : self.comboBox_3.currentText(), "hair_wash" : self.comboBox_4.currentText(),"charge" : self.label_8.text(),
                    "datetime" : {"year": self.calendarWidget.selectedDate().year(), "month" : self.calendarWidget.selectedDate().month(),
                    "day" : self.calendarWidget.selectedDate().day(), "hour" : str(self.comboBox_5.currentText()),
                    "minute" : str(self.comboBox_6.currentText())}}
            personCollection.update_one({"_id" : ObjectId(self.lineEdit_4.text())}, {"$set": doc})

    def sil(self):
        if self.lineEdit_4.text() == "":
            self.label_12.setText("Randevu No giriniz!!")
            self.pushButton.setEnabled(False)
            self.pushButton_3.setEnabled(False)
        else:
            self.label_11.setText("Başarılı!!")
            personCollection.delete_one({"_id" : ObjectId(self.lineEdit_4.text())})

#---------------------------------------------------------------------------------------------------------------------------
# add appointment panel
class add_app(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("barber_app/ekle.ui", self)
        self.show()

        self.pushButton.clicked.connect(self.add_new_appointment)

        self.comboBox.activated.connect(self.combo_box)
        self.comboBox_2.activated.connect(self.combo_box)
        self.comboBox_3.activated.connect(self.combo_box)
        self.comboBox_4.activated.connect(self.combo_box)

        self.calendarWidget.setMinimumDate(QDate(datetime.now().year, datetime.now().month, datetime.now().day))

    def combo_box(self):
        combocu(self)

    def add_new_appointment(self):
        if self.lineEdit.text() == "" or self.lineEdit_2.text() == "" or self.lineEdit_3.text() == "" or self.comboBox.currentText() == "Saç Kesimi" or self.comboBox_2.currentText() == "Sakal Kesimi" or self.comboBox_3.currentText() == "Ense Kesimi" or self.comboBox_4.currentText() == "Yıkama" or self.comboBox_5.currentText() == "Saat" or self.comboBox_6.currentText() == "Dakika":
            self.label_9.setText("Lütfen kutucukları eksiksiz doldurunuz!!")
        else:
            self.label_9.setText("Başarılı!!")
            doc = {"state" : "beklemede", "name" : self.lineEdit.text(), "surname" : self.lineEdit_2.text(),"age": int(self.lineEdit_3.text()),
                    "hair_cut" : self.comboBox.currentText(), "beard_cut" : self.comboBox_2.currentText(),
                    "nape_cut" : self.comboBox_3.currentText(), "hair_wash" : self.comboBox_4.currentText(),"charge" : self.label_8.text(),
                    "datetime" : {"year": self.calendarWidget.selectedDate().year(), "month" : self.calendarWidget.selectedDate().month(),
                    "day" : self.calendarWidget.selectedDate().day(), "hour" : str(self.comboBox_5.currentText()),
                    "minute" : str(self.comboBox_6.currentText())}}
            personCollection.insert_one(doc)    

#---------------------------------------------------------------------------------------------------------------------------
# main panel
class MyGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("barber_app/appointment.ui", self)
        self.show()
        
        self.calendarWidget.clicked.connect(self.calendar)

        self.lineEdit_2.textChanged.connect(self.search_bar)

        self.pushButton.clicked.connect(self.to_randevu_ekle)

        self.pushButton_3.clicked.connect(self.return_main)

        self.pushButton_4.clicked.connect(self.to_randevu_duzenle)

        self.pushButton_6.clicked.connect(self.randevu_ok)

        self.pushButton_7.clicked.connect(self.calendar)

    def search_bar(self):
        for r in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(r,0).text() == self.lineEdit.text() and self.tableWidget.item(r,1).text() == self.lineEdit_2.text():
                row_color_maker(self,r,0)

    def randevu_ok(self):
        personCollection.update_one({"_id" : ObjectId(self.tableWidget.item(self.tableWidget.currentRow(),8).text())}, {"$set": {"state" : "tamamlandi"}})
        row_color_maker(self,self.tableWidget.currentRow(),1)

    def return_main(self):
        self.close()
        self.dialog = MyGUI()

    def to_randevu_ekle(self):
        self.dialog = add_app()

    def to_randevu_duzenle(self):
        self.dialog = update_app()

    def calendar(self):
        clear_tables(self)
        r = 0
        for doc in personCollection.find({"datetime.year" : self.calendarWidget.selectedDate().year()
                                        ,"datetime.month" : self.calendarWidget.selectedDate().month() 
                                        ,"datetime.day" : self.calendarWidget.selectedDate().day()}).sort("datetime.hour"):
            update_table(self,r,doc)
            r = r + 1   
        tamamlannalar = personCollection.count_documents({"datetime.year" : self.calendarWidget.selectedDate().year()
                                        ,"datetime.month" : self.calendarWidget.selectedDate().month() 
                                        ,"datetime.day" : self.calendarWidget.selectedDate().day()
                                        ,"state": "tamamlandi"})
        self.label_11.setText(str(tamamlannalar))
        self.label_12.setText(str(r - tamamlannalar))
        self.label_13.setText(str(r))

def update_table(self,r,doc):
    self.tableWidget.insertRow(r)                            
    self.tableWidget.setItem(r,0,QTableWidgetItem(str(doc["name"])))
    self.tableWidget.setItem(r,1,QTableWidgetItem(str(doc["surname"])))
    self.tableWidget.setItem(r,2,QTableWidgetItem(str(doc["age"])))
    self.tableWidget.setItem(r,3,QTableWidgetItem(str(doc["hair_cut"])))
    self.tableWidget.setItem(r,4,QTableWidgetItem(str(doc["beard_cut"])))
    self.tableWidget.setItem(r,5,QTableWidgetItem(str(doc["nape_cut"])))
    self.tableWidget.setItem(r,6,QTableWidgetItem(str(doc["hair_wash"])))
    self.tableWidget.setItem(r,7,QTableWidgetItem(str(doc["charge"]) + " TL"))
    self.tableWidget.setItem(r,8,QTableWidgetItem(str(doc["_id"])))
    self.tableWidget.setItem(r,9,QTableWidgetItem(str(doc["datetime"]["hour"]) + "." + str(doc["datetime"]["minute"])))
    if doc["state"] == "tamamlandi":
        row_color_maker(self,r,1)

def combocu(self):            
    charge = 0
    if self.comboBox.currentText() == "EVET":
        charge = charge + 50
    if self.comboBox_2.currentText() == "EVET":
        charge = charge + 25
    if self.comboBox_3.currentText() == "EVET":
        charge = charge + 10
    if self.comboBox_4.currentText() == "EVET":
        charge = charge + 10
    self.label_8.setText(str(charge))

def row_color_maker(self,r,mod):
    if mod == 1:
        self.tableWidget.item(r,0).setBackground(QBrush(Qt.green))
        self.tableWidget.item(r,1).setBackground(QBrush(Qt.green))
        self.tableWidget.item(r,2).setBackground(QBrush(Qt.green))
        self.tableWidget.item(r,3).setBackground(QBrush(Qt.green))
        self.tableWidget.item(r,4).setBackground(QBrush(Qt.green))
        self.tableWidget.item(r,5).setBackground(QBrush(Qt.green))
        self.tableWidget.item(r,6).setBackground(QBrush(Qt.green))
        self.tableWidget.item(r,7).setBackground(QBrush(Qt.green))
        self.tableWidget.item(r,8).setBackground(QBrush(Qt.green))
        self.tableWidget.item(r,9).setBackground(QBrush(Qt.green))
    else:
        self.tableWidget.item(r,0).setBackground(QBrush(Qt.yellow))
        self.tableWidget.item(r,1).setBackground(QBrush(Qt.yellow))
        self.tableWidget.item(r,2).setBackground(QBrush(Qt.yellow))
        self.tableWidget.item(r,3).setBackground(QBrush(Qt.yellow))
        self.tableWidget.item(r,4).setBackground(QBrush(Qt.yellow))
        self.tableWidget.item(r,5).setBackground(QBrush(Qt.yellow))
        self.tableWidget.item(r,6).setBackground(QBrush(Qt.yellow))
        self.tableWidget.item(r,7).setBackground(QBrush(Qt.yellow))
        self.tableWidget.item(r,8).setBackground(QBrush(Qt.yellow))
        self.tableWidget.item(r,9).setBackground(QBrush(Qt.yellow))

def clear_tables(self):
    for r in range(self.tableWidget.rowCount()):
        self.tableWidget.removeRow(0)

def main():
    app = QApplication([])
    window= MyGUI()
    app.exec_()

if __name__ == '__main__':
   main()
