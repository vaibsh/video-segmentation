import numpy as np
from video_io.video_reader import read_frame
from feature_processing.image_utils import resize_for_gpt
from config.config import MAX_IMAGE_SIZE

# ============================================================
# BUILD FINAL SEGMENTS
# Convert refined transition points into segments
# ============================================================

def build_final_segments(
    refined_boundaries,
    total_frames
):

    segments = []

    current_start = 0

    for boundary in refined_boundaries:

        segments.append((
            int(current_start),
            int(boundary)
        ))

        current_start = boundary + 1

    segments.append((
        int(current_start),
        int(total_frames - 1)
    ))

    return segments


# ============================================================
# SAMPLE SEGMENT FRAMES
# Uniformly sample each segment to be sent to GPT
# ============================================================

def sample_segment_frames(
    segment,
    video_file,
    n_samples=7
):

    start, end = segment

    ids = [
        int(x)
        for x in np.linspace(
            start,
            end,
            n_samples
        )
    ]

    images = []
    valid_ids = []

    for fid in ids:

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