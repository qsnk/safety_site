import cv2
import ultralytics
import os
import time
from datetime import datetime, timedelta
from collections import deque
from cabinet.models import NeuralNetwork, Violation


class IpCamera(object):
    def __init__(self, url):
        self.url = url
        self.capture = cv2.VideoCapture(self.url)
        neural_network = NeuralNetwork.objects.order_by('pk').last()
        self.model = ultralytics.YOLO(neural_network.file.url[1:])
        self.violations = ['no vest', 'no helmet', 'no boots', 'no glove', 'no hat']
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
        if self.video_writer is not None:
            self.video_writer.release()

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
                    case 'no hat':
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
                    video_path = os.path.join('media', 'violations', 'videos',
                                              f'{"-".join(detection_class.split())}_{self.record_start_time.strftime("%d.%m.%Y_%H-%M-%S")}.mp4')
                    self.video_writer = cv2.VideoWriter(video_path, self.fourcc, self.fps,
                                                        (self.frame_width, self.frame_height))
                    if not self.video_writer.isOpened():
                        raise Exception("Could not open video writer")

                    img_path = os.path.join('media', 'violations', 'images',
                                            f'{"-".join(detection_class.split())}_{self.record_start_time.strftime("%d.%m.%Y_%H-%M-%S")}.jpg')
                    cv2.imwrite(img_path, results[0].plot())
                    violation = Violation(
                        date_time=self.record_start_time.strftime('%y-%m-%d-%H:%M:%S'),
                        violation_class=detection_class,
                        violation_class_ru=violation_class_ru,
                        description=description,
                        photo=f'violations/images/{"-".join(detection_class.split())}_{self.record_start_time.strftime("%d.%m.%Y_%H-%M-%S")}.jpg',
                        user_id=request.user,
                        video=f'violations/videos/{"-".join(detection_class.split())}_{self.record_start_time.strftime("%d.%m.%Y_%H-%M-%S")}.mp4'
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
                if self.video_writer is not None:
                    self.video_writer.release()
                    self.video_writer = None
        resized_frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)
        _, frame = cv2.imencode('.jpg', resized_frame)
        return frame.tobytes()
