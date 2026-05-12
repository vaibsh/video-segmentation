import os
import cv2

from ultralytics import YOLO
from preprocessing.device import get_device
from preprocessing.download_models import ensure_yolo26m

# ============================================================
# YOLO + BOTSORT
# ============================================================

def run_yolo_botsort(
    video_file,
    output_frame_dir
):

    os.makedirs(
        output_frame_dir,
        exist_ok=True
    )


    model_path = ensure_yolo26m()
    model = YOLO(model_path)

    device = get_device()

    model.to(device)

    cap = cv2.VideoCapture(video_file)

    frame_id = 0

    all_frames_data = []

    track_to_object = {}

    next_object_id = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        results = model.track(
            source=frame,
            persist=True,
            tracker="botsort.yaml",
            classes=[0],
            device=device,
            verbose=False
        )

        r = results[0]

        boxes = r.boxes

        frame_data = []

        if (
            boxes is not None
            and
            boxes.id is not None
        ):

            track_ids = boxes.id.cpu().numpy()

            xyxy = boxes.xyxy.cpu().numpy()

            confs = boxes.conf.cpu().numpy()

            clss = boxes.cls.cpu().numpy()

            for i in range(len(track_ids)):

                track_id = int(track_ids[i])

                x1, y1, x2, y2 = xyxy[i]

                conf = float(confs[i])

                cls = int(clss[i])

                class_name = model.names[cls]

                if track_id not in track_to_object:

                    track_to_object[
                        track_id
                    ] = next_object_id

                    next_object_id += 1

                object_id = track_to_object[
                    track_id
                ]

                frame_data.append({

                    "frame_id":
                        frame_id,

                    "track_id":
                        track_id,

                    "object_id":
                        object_id,

                    "class":
                        class_name,

                    "bbox": [
                        float(x1),
                        float(y1),
                        float(x2),
                        float(y2)
                    ],

                    "probability":
                        conf
                })

        frame_path = os.path.join(
            output_frame_dir,
            f"{frame_id:06d}.jpg"
        )

        cv2.imwrite(
            frame_path,
            frame
        )

        all_frames_data.append(
            frame_data
        )

        frame_id += 1

    cap.release()

    print(
        f"\nFrames processed: {frame_id}"
    )

    return all_frames_data