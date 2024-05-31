from cabinet.models import NeuralNetwork, Violation
import cv2, ultralytics, time, os
from datetime import datetime, timedelta


class IpCamera(object):
    def __init__(self, url):
        self.url = url
        self.capture = cv2.VideoCapture("static/video/video.mp4")   # "static/video/video.mp4"  self.url
        self.model = ultralytics.YOLO(NeuralNetwork.objects.get(pk=len(NeuralNetwork.objects.all())).file.url[1:])  # "yolov8n.pt"
        print(self.capture.isOpened())

    def __del__(self):
        self.capture.release()

    def get_frame(self, request):
        if not self.capture.isOpened():
            raise Exception("Could not open video")
        ret, frame = self.capture.read()
        if not ret:
            raise Exception("Could not read frame")
        results = self.model.track(frame, conf=0.5, verbose=False)
        for detection in results[0].boxes:
            detection_id = detection.cls
            detection_class = results[0].names[int(detection_id)]
            if detection_class == 'no vest':
                violation = Violation(
                    date_time=datetime.now(),
                    violation_class=detection_class,
                    description="Отсутствует светоотражающий жилет",
                    photo=results[0].save(os.path.join(f'{os.getcwd()[4:]}/static/images/', f'no-vest-{datetime.now().day}-{datetime.now().month}-{datetime.now().year}-{datetime.now().hour}-{datetime.now().minute}.jpg')),
                    user_id=request.user
                )
                cv2.imwrite(os.path.join(f'{os.getcwd()}/static/images/', f'no-vest-{datetime.now().day}-{datetime.now().month}-{datetime.now().year}-{datetime.now().hour}-{datetime.now().minute}.jpg'), results[0].plot())
                violation.save()
                print("Violation <no vest> detected")
            print(f"Detection, id: {int(detection_id)}\tClasses: {detection_class}")
        frame = results[0].plot()
        resize = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)
        _, jpeg = cv2.imencode('.jpg', resize)
        return jpeg.tobytes()