import cv2
import time
from ipycam import IPCamera, CameraConfig

VIDEO_PATH = "sample.mp4"

config = CameraConfig(
    name="Video File Camera",
    main_width=1280,
    main_height=720,
    main_fps=15,
)

camera = IPCamera(config)
camera.start()

cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS)
if not fps or fps <= 1:
    fps = 15

frame_interval = 1.0 / fps

try:
    while camera.is_running:
        start = time.time()

        ret, frame = cap.read()
        if not ret:
            # 動画末尾に達したら先頭へ戻す
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        camera.stream(frame)

        elapsed = time.time() - start
        sleep_time = frame_interval - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

except KeyboardInterrupt:
    pass
finally:
    cap.release()
    camera.stop()