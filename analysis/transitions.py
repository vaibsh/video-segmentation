import numpy as np
from scipy.ndimage import gaussian_filter1d
from analysis.similarity import cosine_similarity
from config.runtime import runtime_state
from config.config import TRANSITION_SMOOTH_SIGMA

# ============================================================
# SEMANTIC TRANSITION SCORE
# ============================================================

def semantic_transition_score(
    embs,
    motion_dir,
    motion_mag
):

    n = len(embs)

    score = np.zeros(n)

    for t in range(
        runtime_state.runtime_config.SEMANTIC_CONTEXT,
        n - runtime_state.runtime_config.SEMANTIC_CONTEXT
    ):

        emb_before = embs[
            t - runtime_state.runtime_config.SEMANTIC_CONTEXT
        ]

        emb_after = embs[
            t + runtime_state.runtime_config.SEMANTIC_CONTEXT
        ]

        emb_change = np.linalg.norm(
            emb_after - emb_before
        )

        dir_before = motion_dir[t - 1]
        dir_after = motion_dir[t]

        dir_change = (
            1 -
            cosine_similarity(
                dir_before,
                dir_after
            )
        )

        mag_change = abs(
            motion_mag[t] -
            motion_mag[t - 1]
        )

        score[t] = (
            0.6 * emb_change +
            0.3 * dir_change +
            0.1 * mag_change
        )

    score = gaussian_filter1d(
        score,
        sigma=TRANSITION_SMOOTH_SIGMA
    )

    return score