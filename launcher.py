'''
    To run multiple programs simultaneously through multi-procesing

'''

from multiprocessing import Process, Manager
from PyQt5.QtWidgets import QApplication
import time
import cv2
from camera import Camera 
from mainUI import Window
import sys
class runApplication:

    def runCamera(param):
        cam = Camera()
        cam.toDisplay = False
        cam.publish(param)

    def closeCamera(param):
        print("Opening Camera.")
        time.sleep(60)
        print("Closing Camera.")
        param['camStatus'].value = False

    def runUI(param):
        while param['frame'].value is None:
            continue # wait while frame is available
        app = QApplication(sys.argv)
        win = Window() #call pyqt5 window
        while(param['camStatus'].value):
            print(param['frame'].value)
            win
            #win.showFrame()
        #ip.closeDisplay()

if __name__ == '__main__':
    ra =runApplication
    param = {}

    param['camStatus'] = Manager().Value('camStatus', False)
    param['frame'] = Manager().Value('frame', None)
    

    p = [
        Process(target=ra.runCamera, args=(param,)),
        Process(target=ra.runUI, args=(param,)),
        # Process(target=closeCamera, args=(param,)),
    ]

    for process in p:
        process.start()

    for process in p:
        process.join()
