'''
    To run multiple programs simultaneously through multi-procesing

'''

from multiprocessing import Process, Manager
from PyQt5.QtWidgets import QApplication
import time
import cv2
from camera import Camera 
from detection import Model
from openVideo import Video

import sys
class runApplication:

    def runCamera(param):
        cam = Camera()
        cam.toDisplay = False
        cam.publish(param)

    def runVideo(param):
        cam = Video()#Camera()
        cam.toDisplay = True
        cam.publish(param)

    def closeCamera(param):
        print("Opening Camera.")
        time.sleep(60)
        print("Closing Camera.")
        param['camStatus'].value = False

    def runModel(param):
        while param['videoframe'].value is None:
            continue # wait while frame is available
        mod = Model()
        while(param['camStatus'].value):
            mod.receiveFrame(param)


if __name__ == '__main__':
    ra =runApplication
    param = {}

    param['camStatus'] = Manager().Value('camStatus', False)
    param['frame'] = Manager().Value('frame', None)
    param['videoframe'] = Manager().Value('frame', None)

    

    p = [
        #Process(target=ra.runCamera, args=(param,)),
        Process(target=ra.runVideo, args=(param,)),
        Process(target=ra.runModel, args=(param,)),
        # Process(target=closeCamera, args=(param,)),
    ]

    for process in p:
        process.start()

    for process in p:
        process.join()
