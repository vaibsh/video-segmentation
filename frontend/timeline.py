# ============================================================
# BUILD TIMELINE SEGMENTS
# ============================================================

def build_segments(results):

    first_track = list(
        results.keys()
    )[0]

    story_segments = results[
        first_track
    ]["story"]["segments"]

    fps = 30

    timeline_segments = []

    for seg in story_segments:

        start_frame = seg["start_frame"]
        end_frame = seg["end_frame"]

        timeline_segments.append({

            "start_frame":
                start_frame,

            "end_frame":
                end_frame,

            "start_sec":
                start_frame / fps,

            "end_sec":
                end_frame / fps,

            "activity":
                seg["activity"],

            "about":
                seg["about"]

        })

    return timeline_segments