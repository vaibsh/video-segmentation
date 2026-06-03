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

api_key = st.text_input(
    "OpenAI API Key",
    type="password"
)

run_button = st.button(
    "Run Segmentation"
)

# ============================================================
# RUN
# ============================================================

if run_button:

    if (
        video_file is None
        or pkl_file is None
        or not api_key
    ):
        st.error(
            "Please upload both files and specify OPENAI_API_KEY."
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
                logger=streamlit_logger,
                api_key=api_key
            )

        st.success(
            "Segmentation Complete"
        )

        # ====================================================
        # OVERALL VIDEO DESCRIPTION (NEW)
        # ====================================================

        overall_desc = results.get("overall_video", None)

        first_track = list(results.keys())[0]
        overall_desc = results[first_track]["story"]["overall_video"]

        st.markdown("### Overall Video Description")

        if overall_desc:
            #st.markdown("### Overall Video Description")
            st.info(overall_desc)

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