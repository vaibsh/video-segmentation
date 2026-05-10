from pipeline.runner import run_pipeline


def main():

    run_pipeline(
        video_file="inputs/gym.mp4",
        all_frames_data_file="inputs/all_frames_data.pkl.gz"
    )


if __name__ == "__main__":
    main()