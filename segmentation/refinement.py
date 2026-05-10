import numpy as np
from scipy.signal import find_peaks
from analysis.transitions import semantic_transition_score
from config.runtime import runtime_state

# ============================================================
# LOCAL SEMANTIC REFINEMENT
# ============================================================

def refine_boundaries(
    embs,
    motion_dir,
    motion_mag,
    gpt_segments
):

    transition_score = semantic_transition_score(
        embs,
        motion_dir,
        motion_mag
    )

    refined_boundaries = []

    rough_boundaries = []

    for seg in gpt_segments[:-1]:

        rough_boundaries.append(
            int(seg["end_frame"])
        )

    n = len(embs)

    for i, boundary in enumerate(
        rough_boundaries
    ):

        # ====================================================
        # midpoint constraints
        # prevents refined boundary overlaps
        # refined boundaries don't cross mid-points of coarse boundaries
        # ====================================================

        if i == 0:

            left_limit = 0

        else:

            prev_b = rough_boundaries[i - 1]

            left_limit = (
                prev_b + boundary
            ) // 2

        if i == len(rough_boundaries) - 1:

            right_limit = n - 1

        else:

            next_b = rough_boundaries[i + 1]

            right_limit = (
                boundary + next_b
            ) // 2

        # ====================================================
        # clipped search window
        # only search near GPT coarse boundary
        # GPT semantics should be respected, search should remain local
        # ====================================================

        left = max(
            left_limit,
            boundary - runtime_state.runtime_config.SEARCH_RADIUS
        )

        right = min(
            right_limit,
            boundary + runtime_state.runtime_config.SEARCH_RADIUS
        )

        # ====================================================
        # local transition scores
        # semantic_transition_scores in local window around coarse boundary
        # ====================================================

        local_scores = transition_score[
            left:right+1
        ]

        # ====================================================
        # detect local peaks
        # ====================================================

        peaks, _ = find_peaks(
            local_scores
        )

        # ====================================================
        # fallback if no peaks
        # ====================================================

        # if no peaks, choose strongest semantic score as peak in the local window
        if len(peaks) == 0:

            best_local = np.argmax(
                local_scores
            )

            refined = left + best_local

        else:

            candidate_boundaries = []

            for p in peaks:

                global_pos = left + int(p)

                # --------------------------------------------
                # distance from GPT boundary
                # --------------------------------------------

                dist = abs(
                    global_pos - boundary
                )

                # --------------------------------------------
                # transition strength
                # --------------------------------------------

                strength = local_scores[p]

                # --------------------------------------------
                # score = how close are we to GPT boundary and how
                # strong (peaky) is the peak
                # --------------------------------------------

                score = (
                    strength
                    -
                    0.02 * dist
                )

                candidate_boundaries.append({

                    "score": score,

                    "position": global_pos,

                    "distance": dist,

                    "strength": strength

                })

            # =================================================
            # choose best candidate
            # =================================================

            candidate_boundaries = sorted(
                candidate_boundaries,
                key=lambda x: x["score"],
                reverse=True
            )

            refined = candidate_boundaries[0][
                "position"
            ]

        # ====================================================
        # enforce non-overlapping refined boundaries
        # current segment start is at least one frame after
        # prev segment end
        # ====================================================

        if len(refined_boundaries) > 0:

            refined = max(
                refined,
                refined_boundaries[-1] + 1
            )

        refined_boundaries.append(
            int(refined)
        )

    return refined_boundaries