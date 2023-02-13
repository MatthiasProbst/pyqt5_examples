import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

frame_rate = None
BINS = 255


class VideoThread(QThread):
    """Video Thread"""
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, parent_gui):
        super().__init__()
        self.parent_gui = parent_gui
        self.running = False

    def run(self):
        # capture from webcam
        self.parent_gui.btn_start.setText('Waiting for camera stream')
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, frame_rate)
        self.parent_gui.btn_start.setText('Start')
        self.parent_gui.btn_stop.setEnabled(True)
        while self.running:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self.running = False
        self.wait()


class Canvas(FigureCanvasQTAgg):
    """Plotting canvas"""

    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(5, 2), dpi=200)
        self.axline, = self.ax.plot(np.arange(BINS),
                                    np.zeros((BINS,)),
                                    c='r',
                                    lw=1,
                                    alpha=1,
                                    label='Red')
        plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.2)
        self.ax.set_ylim([0, 1])
        self.ax.set_xlabel('pixel value')
        self.ax.set_ylabel('count')
        super().__init__(fig)
        self.setParent(parent)

    def hist(self, x, bins, **kwargs):
        gray = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
        histogramR = cv2.calcHist([gray], [0], None, [bins], [0, 255])
        self.axline.set_ydata(histogramR / np.max(histogramR))


class App(QWidget):
    """Main app"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Webcam stream demo")
        self.stream_image_width = 640
        self.stream_image_height = 480

        self.btn_start = QPushButton()
        self.btn_start.setText('Start')
        self.btn_start.pressed.connect(self.start)
        self.btn_start.setEnabled(True)

        self.btn_stop = QPushButton()
        self.btn_stop.setText('Stop')
        self.btn_stop.pressed.connect(self.stop)
        self.btn_stop.setEnabled(False)

        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.stream_image_width * 2, self.stream_image_height)
        # create a text label
        self.image_label = QLabel('Webcam')
        self.image_label.setFixedWidth(self.stream_image_width)
        self.image_label.setFixedHeight(self.stream_image_height)

        self.chart = Canvas(self)

        # create a vertical box layout and add the two labels
        vbox1 = QVBoxLayout()

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.btn_start)
        hbox1.addWidget(self.btn_stop)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.image_label)
        hbox2.addWidget(self.chart)

        vbox1.addLayout(hbox1)
        vbox1.addLayout(hbox2)

        self.setLayout(vbox1)

        # create the video capture thread
        self.thread = VideoThread(parent_gui=self)
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img, bins=BINS):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
        # self.chart.plot(np.random.rand(10))
        self.chart.hist(cv_img, bins=bins)
        self.chart.draw()

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.stream_image_width, self.stream_image_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def start(self):
        if not self.thread.running:
            self.btn_start.setEnabled(False)
            self.thread.running = True
            self.thread.start()

    def stop(self):
        if self.thread.running:
            self.btn_start.setEnabled(True)
            self.btn_stop.setEnabled(False)
            self.thread.running = False
            self.thread.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
