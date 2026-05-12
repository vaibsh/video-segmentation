import argparse
from pipeline.runner import run_pipeline


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--video_file",
        type=str,
        required=True
    )

    parser.add_argument(
        "--pkl_gz_file",
        type=str,
        required=True
    )

    args = parser.parse_args()

    # ========================================================
    # SEGMENTATION
    # ========================================================

    run_pipeline(
        video_file=args.video_file,
        all_frames_data_file=args.pkl_gz_file
    )


# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":

    main()