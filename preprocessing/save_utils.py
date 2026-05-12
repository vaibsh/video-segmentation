import os
import gzip
import pickle


def save_all_frames_data(
    all_frames_data,
    output_path
):

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    with gzip.open(
        output_path,
        "wb"
    ) as f:

        pickle.dump(
            all_frames_data,
            f
        )

    print(
        f"\nSaved -> {output_path}"
    )