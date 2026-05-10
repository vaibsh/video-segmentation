import numpy as np
from config.config import GLOBAL_ANCHOR_DIVISOR
from config.runtime import runtime_state
# ============================================================
# EXPAND TEMPORAL CONTEXT
# expanded = final set of frames fed to GPT-4o
# includes 1st frame, last frame, peak frames,
# neighbors of peaks, anchor frames
# ============================================================

def expand_keyframes(
    peak_ids,
    total_frames
):

    expanded = set()

    # ========================================================
    # adaptive global anchors
    # ========================================================

    n_anchors = max(
        4,
        total_frames // GLOBAL_ANCHOR_DIVISOR
    )

    anchors = np.linspace(
        0,
        total_frames - 1,
        n_anchors
    ).astype(int)

    for a in anchors:
        expanded.add(int(a))

    # ========================================================
    # temporal context around peaks
    # ========================================================

    for p in peak_ids:

        expanded.add(int(p))

        expanded.add(
            max(
                0,
                int(p - runtime_state.runtime_config.PEAK_CONTEXT)
            )
        )

        expanded.add(
            min(
                total_frames - 1,
                int(p + runtime_state.runtime_config.PEAK_CONTEXT)
            )
        )

    expanded = sorted([
        int(x)
        for x in expanded
    ])

    return expanded