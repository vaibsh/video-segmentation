import os
from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# LOAD ENV
# ============================================================

load_dotenv()

# ============================================================
# OPENAI CLIENT
# ============================================================

def get_openai_client(api_key=None):

    if api_key is None:

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

    if not api_key:

        raise ValueError(
            "No OpenAI API key provided."
        )

    return OpenAI(
        api_key=api_key
    )
# ============================================================
# STATIC HYPER-PARAMETERS
# ============================================================

# Max Image Size and Quality - sent to GPT
MAX_IMAGE_SIZE = 512
JPEG_QUALITY = 65

# used to compute number of anchor frames uniformly spread across video
# to capture frames other than peaks
GLOBAL_ANCHOR_DIVISOR = 80

# Variance of Gaussian Filter to smoothen segment boundary during refinement
TRANSITION_SMOOTH_SIGMA = 2

# Variance of Gaussian Filter to smoothen semantic transition curve
SMOOTH_SIGMA = 2

# Only retain TOP_K_PEAKS as input to GPT-4o
TOP_K_PEAKS = 12

TIME_WINDOW = 0.5

# ============================================================
# DYNAMIC HYPER-PARAMETERS
# ============================================================

# how far to move segment boundary during refinement
SEARCH_RADIUS_FACTOR = 1.0

# how far to look before/after a frame to compute semantic score
SEMANTIC_CONTEXT_FACTOR = 0.4

# how many neighboring frames to include around each detected semantic peak
# frames within 0.25 sec are considered neighbors, min 3 frames included
PEAK_CONTEXT_FACTOR = 0.25

# Min distance between two peaks (peaks are major frame transitions (motion changes / scene changes))
PEAK_DISTANCE_FACTOR = 1.0
