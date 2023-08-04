import cv2
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from threading import Thread
from pyzbar import pyzbar
from pynput.keyboard import Controller
import time
import os



class VideoStreamWidget(object):
    def __init__(self, src=0):
        self.buffer = None
        self.count = 0
        self.time = time.time()
        self.capture = cv2.VideoCapture(src)
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def show_frame(self):
        self.count += 1
        print(self.count)
        img = self.frame
        detectedBarcodes = pyzbar.decode(img)
        if time.time() - self.time > 2:
            self.buffer = ''
        if not detectedBarcodes:
            pass
        else:
            for barcode in detectedBarcodes: 
                (x, y, w, h) = barcode.rect
                cv2.rectangle(img, (x-10, y-10),
                            (x + w+10, y + h+10),
                            (255, 0, 0), 2)
                
                if barcode.data != "" and self.buffer!= barcode.data.decode('utf-8'):
                    self.time = time.time()
                    self.buffer = barcode.data.decode('utf-8')
                    # Print the barcode data
                    keyboard = Controller()
                    keyboard.type(barcode.data.decode('utf-8'))

app = QApplication([])
app.setQuitOnLastWindowClosed(False)

def capture():
    option1.setText('توقف اجرای بارکد خوان')
    video_stream_widget = VideoStreamWidget()  
    while True:
        try:
            video_stream_widget.show_frame()
        except AttributeError:
            pass


my_loop = Thread(target=capture, args=())
icon = QIcon('./img.jpg')
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)
tray.show()
menu = QMenu()
option1 = QAction("اجرای بار کد خوان")
option1.triggered.connect(my_loop.start)
menu.addAction(option1)
tray.setContextMenu(menu)
app.exec_()
