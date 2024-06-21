from cabinet.models import NeuralNetwork, Violation
import cv2, ultralytics, os, time
from datetime import datetime, timedelta
from collections import deque


class IpCamera(object):
    def __init__(self, url):
        self.url = url
        self.capture = cv2.VideoCapture("static/video/video.mp4")  # "static/video/video.mp4"  self.url
        self.model = ultralytics.YOLO(
            NeuralNetwork.objects.get(pk=len(NeuralNetwork.objects.all())).file.url[1:])  # "yolov8n.pt"
        self.violations = ['no vest', 'no helmet', 'no boots', 'no glove']
        self.frame_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = 10
        self.buffer_seconds = 15
        self.buffer_size = int(self.buffer_seconds * self.fps)
        self.frame_buffer = deque(maxlen=self.buffer_size)
        self.video_writer = None
        self.loop_time = time.time()
        self.recording = False
        self.violation_detected = False
        self.record_start_time = None
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        print(self.capture.isOpened())

    def __del__(self):
        self.capture.release()
        self.video_writer.release() if self.video_writer is not None else None

    def get_frame(self, request):
        if not self.capture.isOpened():
            raise Exception("Could not open video")

        success, frame = self.capture.read()

        if not success:
            raise Exception("Could not read frame")
        self.loop_time = time.time()

        results = self.model.track(frame, conf=0.5, verbose=False)

        for detection in results[0].boxes:
            detection_id = detection.cls
            detection_class = results[0].names[int(detection_id)]
            if detection_class in self.violations and not self.violation_detected:
                description = None
                violation_class_ru = None
                self.violation_detected = True
                match detection_class:
                    case 'no vest':
                        description = "Отсутствует светоотражающий жилет"
                        violation_class_ru = "нет жилета"
                    case 'no helmet':
                        description = "Отсутствует защитная каска"
                        violation_class_ru = "нет каски"
                    case 'no glove':
                        description = "Отсутствуют защитные перчатки"
                        violation_class_ru = "нет перчаток"
                    case 'no boots':
                        description = "Отсутствует защитная обувь"
                        violation_class_ru = "нет обуви"
                    case _:
                        pass

                if not self.recording:
                    self.record_start_time = datetime.now()
                    self.video_writer = cv2.VideoWriter(os.path.join('media', 'violations', 'videos',
                                                                f'{"-".join(detection_class.split())}_{datetime.now().day}.{datetime.now().month}.{datetime.now().year}_{datetime.now().hour}-{datetime.now().minute}.mp4'),
                                                   self.fourcc, self.fps, (self.frame_width, self.frame_height))
                    cv2.imwrite(os.path.join('media', 'violations', 'images',
                                                          f'{"-".join(detection_class.split())} {datetime.now().day}.{datetime.now().month}.{datetime.now().year} {datetime.now().hour}:{datetime.now().minute}.jpg'),
                                             results[0].plot())
                    violation = Violation(
                        date_time=datetime.now().strftime('%y-%m-%d-%H:%M:%S'),
                        violation_class=detection_class,
                        violation_class_ru=violation_class_ru,
                        description=description,
                        photo=f'violations/images/{"-".join(detection_class.split())} {datetime.now().day}.{datetime.now().month}.{datetime.now().year} {datetime.now().hour}:{datetime.now().minute}.jpg',
                        user_id=request.user,
                        video=f'violations/videos/{"-".join(detection_class.split())}_{datetime.now().day}.{datetime.now().month}.{datetime.now().year}_{datetime.now().hour}-{datetime.now().minute}.mp4'
                    )
                    violation.save()
                    for buffered_frame in self.frame_buffer:
                        self.video_writer.write(buffered_frame)
                    self.recording = True

        frame = results[0].plot()

        if self.recording:
            self.video_writer.write(frame)
            if datetime.now() - self.record_start_time >= timedelta(seconds=10):
                self.recording = False
                self.violation_detected = False
                self.video_writer.release()
        resized_frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)
        _, frame = cv2.imencode('.jpg', resized_frame)
        return frame.tobytes()
