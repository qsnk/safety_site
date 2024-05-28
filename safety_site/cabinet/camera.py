from cabinet.models import NeuralNetwork
import cv2, ultralytics


class IpCamera(object):
    def __init__(self, url):
        self.url = url
        self.capture = cv2.VideoCapture(self.url)
        print(self.capture.isOpened())

    def __del__(self):
        self.capture.release()

    def get_frame(self):
        if not self.capture.isOpened():
            raise Exception("Could not open video")
        ret, frame = self.capture.read()
        if not ret:
            raise Exception("Could not read frame")
        resize = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)
        _, jpeg = cv2.imencode('.jpg', resize)
        return jpeg.tobytes()