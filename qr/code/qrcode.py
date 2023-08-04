import cv2
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from threading import Thread
from pynput.keyboard import Controller
import time


class VideoStreamWidget(object):
    def __init__(self, src=0):
        self.buffer = None
        self.count = 0
        self.time = time.time()
        self.capture = cv2.VideoCapture(src)
        self.thread = Thread(target=self.update, args=())
        self.detector = cv2.QRCodeDetector()
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def show_frame(self):
        self.count += 1
        #print(self.count)
        if time.time() - self.time > 2:
            self.buffer = ''
        img = self.frame        
        data, bbox, _ = self.detector.detectAndDecode(img)
        if data and self.buffer != data:
            self.time = time.time()
            self.buffer = data
            keyboard = Controller()
            keyboard.type(data)

app = QApplication([])
app.setQuitOnLastWindowClosed(False)

def capture():
    option1.setText('توقف اجرای کیوآر خوان')
    video_stream_widget = VideoStreamWidget()  
    while True:
        try:
            video_stream_widget.show_frame()
        except AttributeError:
            pass

my_loop = Thread(target=capture, args=())
icon = QIcon("./hello.png")
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)
menu = QMenu()
option1 = QAction("اجرای کیوآر خوان")
option1.triggered.connect(my_loop.start)
menu.addAction(option1)
tray.setContextMenu(menu)
app.exec_()
