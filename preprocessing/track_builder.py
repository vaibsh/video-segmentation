import numpy as np
from collections import defaultdict

# ============================================================
# FEATURE EXTRACTION
# Track Wise Feature Extraction
# Features = Object Embeddings, Motion Mag, Motion Dir
# ============================================================

def build_track_features(all_frames_data, k):

    tracks = defaultdict(list)

    for frame_data in all_frames_data:

        for obj in frame_data:

            if obj.get("embedding") is None:
                continue

            track_id = obj["track_id"]

            emb = obj["embedding"]

            x1, y1, x2, y2 = obj["bbox"]

            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2

            tracks[track_id].append({

                "embedding": emb,

                "center": np.array([
                    cx,
                    cy
                ])

            })


    track_features = {}

    # seq = temporal sequence of observations for an object / track_id
    for track_id, seq in tracks.items():

        # ignore short tracks - insufficient data
        if len(seq) < k + 5:
            continue

        embs = np.stack([
            s["embedding"]
            for s in seq
        ])

        centers = np.stack([
            s["center"]
            for s in seq
        ])

        # ========================================================
        # normalize embeddings
        # L2 norm, 1e-6 to avoid near zero norms
        # ========================================================

        embs = embs / (
            np.linalg.norm(
                embs,
                axis=1,
                keepdims=True
            ) + 1e-6
        )

        # ========================================================
        # motion
        # ========================================================

        motion = np.diff(
            centers,
            axis=0
        )

        # (1, 0) = Add 1 row before 0th element, Add 0 rows after last element
        # (0, 0) = Keep columns unchanged
        # Padded element is same as 0th element, "edge" = use edge element for padding
        motion = np.pad(
            motion,
            ((1, 0), (0, 0)),
            mode="edge"
        )

        motion_mag = np.linalg.norm(
            motion,
            axis=1
        )

        motion_dir = motion / (
            np.linalg.norm(
                motion,
                axis=1,
                keepdims=True
            ) + 1e-6
        )

        track_features[track_id] = {

            "embeddings": embs,

            "motion_mag": motion_mag,

            "motion_dir": motion_dir

        }

    return track_features