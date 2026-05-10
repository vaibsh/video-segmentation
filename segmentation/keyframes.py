import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
from config.config import SMOOTH_SIGMA, TOP_K_PEAKS
from config.runtime import runtime_state

# ============================================================
# SEMANTIC KEYFRAME SAMPLING
# Samples 1st frame, last frame and peaks
# ============================================================

def semantic_keyframe_sampling(
    embs,
    motion_mag
):

    # embedding difference = scene change
    emb_diff = np.linalg.norm(
        embs[1:] - embs[:-1],
        axis=1
    )

    emb_diff = np.pad(
        emb_diff,
        (1, 0),
        mode="edge"
    )

    semantic_score = (
        0.8 * emb_diff +
        0.2 * motion_mag
    )

    semantic_score = gaussian_filter1d(
        semantic_score,
        sigma=SMOOTH_SIGMA
    )

    peaks, _ = find_peaks(
        semantic_score,
        distance=runtime_state.runtime_config.PEAK_DISTANCE
    )

    if len(peaks) > TOP_K_PEAKS:

        strongest = np.argsort(
            semantic_score[peaks]
        )[-TOP_K_PEAKS:]

        peaks = peaks[strongest]

    peaks = sorted([
        int(p)
        for p in peaks.tolist()
    ])

    # Add 1st frame
    final_ids = [0]

    # Add Peak Frames
    final_ids.extend(peaks)

    # Add last frame
    final_ids.append(
        len(embs) - 1
    )

    # sort chronologically, duplicates removed
    final_ids = sorted([
        int(x)
        for x in set(final_ids)
    ])

    return final_ids