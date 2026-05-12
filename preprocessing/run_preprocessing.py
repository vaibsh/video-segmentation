import os
from preprocessing.yolo_tracker import run_yolo_botsort
from preprocessing.sam2_processor import attach_sam2_masks
from preprocessing.embedding_extractor import attach_dino_embeddings
from preprocessing.save_utils import save_all_frames_data

# ============================================================
# MAIN PREPROCESSING PIPELINE
# ============================================================

def run_preprocessing(video_file):

    frames_dir = "outputs/frames_out"

    os.makedirs(
        frames_dir,
        exist_ok=True
    )

    # ========================================================
    # YOLO + BOTSORT
    # ========================================================

    all_frames_data = run_yolo_botsort(
        video_file=video_file,
        output_frame_dir=frames_dir
    )

    # ========================================================
    # SAM2
    # ========================================================

    all_frames_data = attach_sam2_masks(
        all_frames_data,
        frames_dir
    )

    # ========================================================
    # DINO
    # ========================================================

    all_frames_data = attach_dino_embeddings(
        all_frames_data,
        frames_dir
    )

    # ========================================================
    # SAVE
    # ========================================================

    save_all_frames_data(
        all_frames_data,
        "outputs/all_frames_data.pkl.gz"
    )