# ============================================================
# MAIN PIPELINE
# ============================================================
import json
from video_io.loader import load_all_frames_data
from video_io.video_reader import get_fps
from config.config import TIME_WINDOW
from preprocessing.track_builder import build_track_features
from segmentation.keyframes import semantic_keyframe_sampling
from segmentation.expansion import expand_keyframes
from preprocessing.frame_loader import load_selected_frames
from segmentation.gpt_segmentation import gpt_coarse_segmentation
from segmentation.refinement import refine_boundaries
from segmentation.final_segments import build_final_segments, sample_segment_frames
from analysis.story import analyze_video_story
from config.runtime.runtime_config import build_runtime_config
from config.runtime import runtime_state
from pipeline.helpers import save_results

def run_pipeline(video_file,
                 all_frames_data_file,
                 logger=None):

    # ========================================================
    # LOAD DATA
    # ========================================================

    all_frames_data = load_all_frames_data(
        all_frames_data_file
    )

    # ========================================================
    # VIDEO FPS
    # ========================================================

    fps = get_fps(video_file)

    print("\nFPS:", fps)
    if logger:
        logger(f"\nFPS: {fps}")

    # ========================================================
    # INIT DYNAMIC RUNTIME
    # ========================================================

    runtime_state.runtime_config = build_runtime_config(fps)

    # ========================================================
    # TEMPORAL WINDOW
    # ========================================================

    k = max(
        2,
        int(TIME_WINDOW * fps)
    )

    print("Temporal window k:", k)

    # ========================================================
    # BUILD TRACK FEATURES
    # ========================================================

    track_features = build_track_features(
        all_frames_data=all_frames_data,
        k=k
    )

    print("\nTracks:")
    print(list(track_features.keys()))
    if logger:
        logger("Tracks:")
        logger(list(track_features.keys()))


    final_results = {}

    for track_id, feats in track_features.items():
        embs = feats["embeddings"]
        motion_mag = feats["motion_mag"]
        motion_dir = feats["motion_dir"]

        if len(embs) < 30:
            continue

        print("\n===================================")
        print("TRACK:", track_id)
        print("===================================")
        if logger:
            logger("===================================")
            logger(f"TRACK: {track_id}")
            logger("===================================")

        # ========================================================
        # SEMANTIC PEAKS
        # ========================================================

        peak_ids = semantic_keyframe_sampling(
            embs,
            motion_mag
        )

        print("\nPeak Keyframes:")
        print(peak_ids)

        # ========================================================
        # EXPANDED CONTEXT
        # ========================================================

        expanded_ids = expand_keyframes(
            peak_ids,
            len(embs)
        )

        print("\nExpanded Keyframes:")
        print(expanded_ids)

        # ========================================================
        # LOAD FRAMES
        # ========================================================

        images, frame_ids = load_selected_frames(
            expanded_ids, video_file
        )

        # ========================================================
        # GPT SEGMENTATION
        # ========================================================

        coarse = gpt_coarse_segmentation(
            images,
            frame_ids,
            len(embs)
        )

        print("\nGPT Coarse Segments:")
        print(
            json.dumps(
                coarse,
                indent=2
            )
        )
        if logger:
            logger("GPT Coarse Segments:")
            logger(
                json.dumps(
                coarse,
                indent=2
                )
            )

        # ========================================================
        # REFINE BOUNDARIES
        # ========================================================

        refined_boundaries = refine_boundaries(
            embs,
            motion_dir,
            motion_mag,
            coarse["segments"]
        )

        print("\nRefined Boundaries:")
        print(refined_boundaries)

        # ========================================================
        # FINAL SEGMENTS
        # ========================================================

        final_segments = build_final_segments(
            refined_boundaries,
            len(embs)
        )

        print("\nFinal Segments:")
        print(final_segments)
        if logger:
            logger("Final Segments:")
            logger(final_segments)

        # ========================================================
        # PREP SEGMENT INPUTS
        # ========================================================

        segment_inputs = []

        for idx, segment in enumerate(
            final_segments
        ):

            seg_images, seg_frames = (
                sample_segment_frames(
                    segment,
                    video_file,
                    n_samples=7
                )
            )

            segment_inputs.append({

                "segment_id": idx,
                "frames": seg_frames,
                "images": seg_images

            })

        # ========================================================
        # STORY UNDERSTANDING
        # ========================================================

        story = analyze_video_story(
            segment_inputs
        )

        print("\n===================================")
        print("FINAL STORY")
        print("===================================")

        print(
            json.dumps(
                story,
                indent=2
            )
        )

        if logger:
            logger("===================================")
            logger("FINAL STORY")
            logger("===================================")

            logger(
                json.dumps(
                    story,
                    indent=2
                )
            )

        # ========================================================
        # SAVE RESULTS
        # ========================================================

        final_results[track_id] = {

            "peak_keyframes":
                peak_ids,

            "expanded_keyframes":
                expanded_ids,

            "gpt_segments":
                coarse["segments"],

            "refined_boundaries":
                refined_boundaries,

            "final_segments":
                final_segments,

            "story":
                story
        }

    # ========================================================
    # SAVE RESULTS
    # ========================================================

    save_results(final_results)

    return final_results