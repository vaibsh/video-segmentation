import os
import streamlit as st

from pipeline.runner import run_pipeline
from frontend.player import render_segmented_video

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Video Segmentation",
    layout="wide"
)

st.title(
    "Video Segmentation"
)

# ============================================================
# FILE UPLOADS
# ============================================================

video_file = st.file_uploader(
    "Upload Video",
    type=["mp4", "mov", "avi"]
)

pkl_file = st.file_uploader(
    "Upload all_frames_data.pkl.gz",
    type=["gz"]
)

run_button = st.button(
    "Run Segmentation"
)

# ============================================================
# RUN
# ============================================================

if run_button:

    if video_file is None or pkl_file is None:

        st.error(
            "Please upload both files."
        )

    else:

        os.makedirs(
            "uploads",
            exist_ok=True
        )

        # ====================================================
        # SAVE VIDEO
        # ====================================================

        video_path = os.path.join(
            "uploads",
            video_file.name
        )

        with open(video_path, "wb") as f:

            f.write(
                video_file.read()
            )

        # ====================================================
        # SAVE PKL
        # ====================================================

        pkl_path = os.path.join(
            "uploads",
            pkl_file.name
        )

        with open(pkl_path, "wb") as f:

            f.write(
                pkl_file.read()
            )

        # ====================================================
        # LOG STORAGE
        # ====================================================

        logs = []

        # ====================================================
        # LOGGER FUNCTION
        # ====================================================

        def streamlit_logger(msg):

            logs.append(str(msg))

        # ====================================================
        # RUN PIPELINE
        # ====================================================

        with st.spinner(
            "Running segmentation..."
        ):

            results = run_pipeline(
                video_file=video_path,
                all_frames_data_file=pkl_path,
                logger=streamlit_logger
            )

        st.success(
            "Segmentation Complete"
        )

        # ====================================================
        # VIDEO + TIMELINE + DESCRIPTION
        # ====================================================

        render_segmented_video(
            video_path,
            results
        )

        # ====================================================
        # LOGS SECTION (BELOW VIDEO)
        # ====================================================

        st.markdown("---")

        st.subheader(
            "Pipeline Logs"
        )

        st.code(
            "\n\n".join(logs),
            language="text"
        )