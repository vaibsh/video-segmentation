import cv2
from PIL import Image

# ============================================================
# FRAME READER
# ============================================================

def read_frame(video_file, frame_idx):

    cap = cv2.VideoCapture(video_file)

    cap.set(
        cv2.CAP_PROP_POS_FRAMES,
        int(frame_idx)
    )

    ret, frame = cap.read()

    cap.release()

    if not ret:
        return None

    frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    return Image.fromarray(frame)


# ============================================================
# VIDEO FPS
# ============================================================

def get_fps(video_file):
    cap = cv2.VideoCapture(video_file)

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    cap.release()

    if fps is None or fps == 0:
        fps = 30

    return fps