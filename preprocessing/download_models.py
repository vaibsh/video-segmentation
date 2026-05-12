import os
import urllib.request

# ============================================================
# YOLO26M
# ============================================================

YOLO26M_URL = (
    "https://github.com/ultralytics/assets/"
    "releases/download/v8.4.0/yolo26m.pt"
)

YOLO26M_PATH = (
    "checkpoints/yolo26m.pt"
)

# ============================================================
# SAM2
# ============================================================

SAM2_URL = (
    "https://dl.fbaipublicfiles.com/"
    "segment_anything_2/092824/"
    "sam2.1_hiera_large.pt"
)

SAM2_PATH = (
    "checkpoints/sam2.1_hiera_large.pt"
)

# ============================================================
# GENERIC DOWNLOADER
# ============================================================

def download_if_missing(
    url,
    save_path,
    model_name
):

    os.makedirs(
        "checkpoints",
        exist_ok=True
    )

    if os.path.exists(save_path):

        print(
            f"{model_name} already exists."
        )

        return save_path

    print(
        f"Downloading {model_name}..."
    )

    urllib.request.urlretrieve(
        url,
        save_path
    )

    print(
        f"Downloaded {model_name}"
    )

    return save_path

# ============================================================
# HELPERS
# ============================================================

def ensure_yolo26m():

    return download_if_missing(
        YOLO26M_URL,
        YOLO26M_PATH,
        "YOLO26M"
    )

def ensure_sam2_checkpoint():

    return download_if_missing(
        SAM2_URL,
        SAM2_PATH,
        "SAM2 checkpoint"
    )