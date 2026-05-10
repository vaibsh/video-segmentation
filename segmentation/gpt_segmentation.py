from preprocessing.image_utils import pil_to_data_url
from utils.json_utils import safe_json
from config.config import client

# ============================================================
# GPT SEGMENTATION
# ============================================================

def gpt_coarse_segmentation(
    images,
    frame_ids,
    total_frames
):

    content = []

    prompt = f"""
You are analyzing temporally ordered keyframes from a video.

Each image corresponds to a frame in time order.

Your task:
Segment the video into coherent temporal activity segments.

A segment represents a period where:
- the main action is consistent
- the scene context is stable
- the intent or behavior does not change significantly

IMPORTANT PRINCIPLES:

1. Temporal coherence
- Do not split segments for minor visual changes
- Only create a new segment when there is a meaningful shift in activity, context, or intent

2. Visual grounding
- Base decisions ONLY on visible information
- Avoid guessing hidden intent or unseen actions

3. Granularity control
- Prefer fewer, more meaningful segments over many small ones
- Avoid micro-segmentation of continuous actions

4. Transition handling
- Early frames may represent setup or preparation
- Later frames may represent completion or transition out of activity

Return STRICT JSON ONLY:

{{
  "segments": [
    {{
      "start_frame": 0,
      "end_frame": 120,
      "activity": "short human-readable description of activity"
    }}
  ]
}}

RULES:
- Segments must fully cover the video [0 → {total_frames-1}]
- No overlaps between segments
- No gaps between segments
- Segments must be ordered in time
- Final segment must end at {total_frames - 1}
"""

    content.append({
        "type": "input_text",
        "text": prompt
    })

    for img, fid in zip(
        images,
        frame_ids
    ):

        content.append({
            "type": "input_text",
            "text": f"Frame {fid}"
        })

        content.append({
            "type": "input_image",
            "image_url":
                pil_to_data_url(img)
        })

    response = client.responses.create(
        model="gpt-4o",
        input=[{
            "role": "user",
            "content": content
        }]
    )

    return safe_json(
        response.output_text
    )