import gzip
import pickle

def load_all_frames_data(pkl_file):

    with gzip.open(
        pkl_file,
        "rb"
    ) as f:

        all_frames_data = pickle.load(f)

    return all_frames_data