import argparse

from preprocessing.run_preprocessing import (
    run_preprocessing
)

from pipeline.runner import run_pipeline


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--preprocess",
        action="store_true"
    )

    parser.add_argument(
        "--segment",
        action="store_true"
    )

    parser.add_argument(
        "--video_file",
        type=str,
        required=True
    )

    parser.add_argument(
        "--pkl_gz_file",
        type=str,
        default=None
    )

    args = parser.parse_args()

    # ========================================================
    # VALIDATE MODE
    # ========================================================

    if args.preprocess == args.segment:

        raise ValueError(
            "Specify either "
            "--preprocess or --segment"
        )

    # ========================================================
    # PREPROCESS
    # ========================================================

    if args.preprocess:

        run_preprocessing(
            video_file=args.video_file
        )

    # ========================================================
    # SEGMENTATION
    # ========================================================

    if args.segment:

        if args.pkl_gz_file is None:

            raise ValueError(
                "--pkl_gz_file required "
                "with --segment"
            )

        run_pipeline(
            video_file=args.video_file,
            all_frames_data_file=args.pkl_gz_file
        )


# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":

    main()