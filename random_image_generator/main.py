import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from random_image_generator import Ui_MainWindow

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'


class Ui(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        self.setupUi(self)
        Ui.setWindowTitle(self, "Image Manipulator")

        self.figure_a1 = plt.figure()
        self.canvas_a1 = FigureCanvasQTAgg(self.figure_a1)
        self.ax = self.figure_a1.add_subplot(111)
        self.horizontalLayout.addWidget(self.canvas_a1)

        self.plot(np.random.rand(10, 20))

        self.pushButton.clicked.connect(self.btn_rgb_gray)

    def btn_rgb_gray(self):
        arr = np.random.rand(10, 20)
        self.ax.imshow(arr)
        self.canvas_a1.draw()

    def plot(self, arr):
        self.ax.imshow(arr)

    def clearLayout(self, layout):
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
                layout.removeItem(item)


def main(argv):
    start(argv)


def start(argv):
    app = QtWidgets.QApplication(argv)
    _main = Ui()
    _main.show()
    app.exec_()


if __name__ == "__main__":
    main(sys.argv)
