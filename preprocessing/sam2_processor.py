import os
import numpy as np
import torch

from sam2.build_sam import build_sam2_video_predictor
from preprocessing.device import get_device
from preprocessing.download_models import ensure_sam2_checkpoint

# ============================================================
# SAM2 MASK PROPAGATION
# ============================================================

def attach_sam2_masks(
    all_frames_data,
    frames_dir
):

    device = get_device()

    if device == "cuda":

        torch.autocast(
            "cuda",
            dtype=torch.bfloat16
        ).__enter__()

    '''
    sam2_checkpoint = (
        "preprocessing/checkpoints/"
        "sam2.1_hiera_large.pt"
    )
    '''

    sam2_checkpoint = ensure_sam2_checkpoint()

    model_cfg = (
        "configs/sam2.1/"
        "sam2.1_hiera_l.yaml"
    )

    predictor = build_sam2_video_predictor(
        model_cfg,
        sam2_checkpoint,
        device=device
    )

    frame_names = sorted(
    [
        p for p in os.listdir(frames_dir)
        if p.endswith(".jpg")
    ],
    key=lambda x:
        int(os.path.splitext(x)[0])
    )

    inference_state = predictor.init_state(
        video_path=frames_dir
    )

    ann_frame_idx = 0

    frame_data = all_frames_data[
        ann_frame_idx
    ]

    for obj in frame_data:

        track_id = obj["track_id"]

        bbox = obj["bbox"]

        box = np.array(
            bbox,
            dtype=np.float32
        )

        predictor.add_new_points_or_box(
            inference_state=inference_state,
            frame_idx=ann_frame_idx,
            obj_id=track_id,
            box=box,
        )

    video_segments = {}

    seen_track_ids = set()

    prop_gen = predictor.propagate_in_video(
        inference_state
    )

    for frame_idx in range(
        len(frame_names)
    ):

        frame_data = all_frames_data[
            frame_idx
        ]

        for obj in frame_data:

            track_id = obj["track_id"]

            if track_id not in seen_track_ids:

                bbox = obj["bbox"]

                box = np.array(
                    bbox,
                    dtype=np.float32
                )

                predictor.add_new_points_or_box(
                    inference_state=inference_state,
                    frame_idx=frame_idx,
                    obj_id=track_id,
                    box=box,
                )

                seen_track_ids.add(
                    track_id
                )

        (
            out_frame_idx,
            out_obj_ids,
            out_mask_logits
        ) = next(prop_gen)

        video_segments[out_frame_idx] = {}

        for i, out_obj_id in enumerate(
            out_obj_ids
        ):

            mask = (
                out_mask_logits[i] > 0.0
            ).cpu().numpy()

            video_segments[
                out_frame_idx
            ][out_obj_id] = mask

        for obj in frame_data:

            track_id = obj["track_id"]

            if (
                track_id
                in
                video_segments[out_frame_idx]
            ):

                obj["mask"] = video_segments[
                    out_frame_idx
                ][track_id]

            else:

                obj["mask"] = None

    return all_frames_data