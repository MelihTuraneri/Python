from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import pandas as pd 
import numpy as np
import sys

final_df = pd.read_csv("hist_graph_for_pyqt5/final_data2.csv")

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
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
        self._static_ax.bar(x = np.arange(0,100,2), height = hist_list, edgecolor="blue")
        self._static_ax.set_xticks(np.arange(4,104,4))
        self._static_ax.set_yticks(np.arange(0,20,1))

if __name__ == "__main__":
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()