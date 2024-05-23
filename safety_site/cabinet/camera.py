from cabinet.models import Camera
import cv2


class IpCamera:
    def __init__(self, request, id):
        self.camera = Camera.objects.filter(pk=id, user_id=request.user)[0]
        self.url = self.camera.url
        # self.capture = cv2.VideoCapture(self.url)
        # print(self.capture.isOpened())

    # def __del__(self):
    #     self.capture.release()

    # def get_frame(self):
    #     if not self.capture.isOpened():
    #         raise Exception("Could not open video")
    #     ret, frame = self.capture.read()
    #     if not ret:
    #         raise Exception("Could not read frame")
    #     print(frame)
    #     img = cv2.imdecode(frame, 1)
    #     resize = cv2.resize(img, (640, 480), interpolation=cv2.INTER_LINEAR)
    #     _, jpeg = cv2.imencode('.jpg', resize)
    #     return jpeg.tobytes()