from video_io.video_reader import read_frame
from preprocessing.image_utils import resize_for_gpt
from config.config import MAX_IMAGE_SIZE

# ============================================================
# LOAD FRAMES
# Loads specified frame_ids and prepares them for GPT processing
# ============================================================

def load_selected_frames(frame_ids, video_file):

    images = []
    valid_ids = []

    for fid in frame_ids:

        img = read_frame(
            video_file,
            fid
        )

        if img is None:
            continue

        img = resize_for_gpt(
            img,
            MAX_IMAGE_SIZE
        )

        images.append(img)
        valid_ids.append(int(fid))

    return images, valid_ids