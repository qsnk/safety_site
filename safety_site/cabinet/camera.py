from cabinet.models import NeuralNetwork
import cv2, ultralytics


class IpCamera(object):
    def __init__(self, url):
        self.url = url
        self.capture = cv2.VideoCapture("static/video/video.mp4")   # self.url
        self.model = ultralytics.YOLO(NeuralNetwork.objects.get(pk=len(NeuralNetwork.objects.all())).file.url[1:])
        print(self.capture.isOpened())

    def __del__(self):
        self.capture.release()

    def get_frame(self):
        if not self.capture.isOpened():
            raise Exception("Could not open video")
        ret, frame = self.capture.read()
        if not ret:
            raise Exception("Could not read frame")
        results = self.model.track(frame, conf=0.1)
        frame = results[0].plot()
        resize = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)
        _, jpeg = cv2.imencode('.jpg', resize)
        return jpeg.tobytes()