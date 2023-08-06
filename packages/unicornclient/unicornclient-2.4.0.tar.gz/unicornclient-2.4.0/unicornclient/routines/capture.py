import threading
import queue
import time
import logging

from .. import message

try:
    from io import BytesIO
    from picamera import PiCamera
except ImportError:
    PiCamera = None
    logging.warning("No picamera module")

class Routine(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        self.manager = None

    def run(self):
        if not PiCamera:
            return

        camera = PiCamera()
        camera.resolution = (1024, 768)
        camera.start_preview()
        time.sleep(2) # Camera warm-up time

        while True:
            self.queue.get()

            pic_stream = BytesIO()
            camera.capture(pic_stream, 'jpeg', resize=(320, 240))
            data = pic_stream.read()
            header = {'type':'capture'}
            pic_message = message.Message(header)
            pic_message.set_body(data)
            self.manager.send(pic_message)
            time.sleep(10)

            self.queue.task_done()
