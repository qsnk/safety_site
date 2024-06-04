from cabinet.models import NeuralNetwork, Violation
import cv2, ultralytics, time, os
from datetime import datetime, timedelta, timezone


class IpCamera(object):
    def __init__(self, url):
        self.url = url
        self.capture = cv2.VideoCapture(self.url)   # "static/video/video.mp4"  self.url
        self.model = ultralytics.YOLO(NeuralNetwork.objects.get(pk=len(NeuralNetwork.objects.all())).file.url[1:])  # "yolov8n.pt"
        self.violations = ['no vest', 'no helmet', 'no boots', 'no glove']
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
            if detection_class in self.violations:
                description = None

                match detection_class:
                    case 'no vest':
                        description = "Отсутствует светоотражающий жилет"
                    case 'no helmet':
                        description = "Отсутствует защитная каска"
                    case 'no glove':
                        description = "Отсутствуют защитные перчатки"
                    case 'no boots':
                        description = "Отсутствует защитная обувь"
                    case _:
                        pass
                saved_file = cv2.imwrite(os.path.join('media', 'violations', f'{"-".join(detection_class.split())} {datetime.now().day}.{datetime.now().month}.{datetime.now().year} {datetime.now().hour}:{datetime.now().minute}.jpg'), results[0].plot())

                if saved_file:
                    violation = Violation(
                        date_time=datetime.now().strftime('%y-%m-%d-%H:%M:%S'),
                        violation_class=detection_class,
                        description=description,
                        photo=f'violations/{"-".join(detection_class.split())} {datetime.now().day}.{datetime.now().month}.{datetime.now().year} {datetime.now().hour}:{datetime.now().minute}.jpg',
                        user_id=request.user
                    )
                    violation.save()
                    print(f"Detection, id: {int(detection_id)}\tClasses: {detection_class}")

        frame = results[0].plot()
        resize = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)
        _, jpeg = cv2.imencode('.jpg', resize)
        return jpeg.tobytes()