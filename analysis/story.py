from preprocessing.image_utils import pil_to_data_url
from utils.json_utils import safe_json
from config.config import client

# ============================================================
# STORY UNDERSTANDING
# ============================================================

def analyze_video_story(
    segments
):

    content = []

    prompt = """
You are analyzing a temporally segmented video.

Each segment contains frames that belong to a single coherent activity.

Your task:
For each segment, describe:
1. What the main activity is
2. What is visually happening
3. How the activity evolves if relevant

IMPORTANT PRINCIPLES:

1. Temporal consistency
- Each segment should represent one stable activity or phase
- Do not split or merge segments mentally

2. Visual grounding
- Only describe what is clearly visible
- Avoid guessing unseen actions or intent

3. Activity transitions
- Earlier segments may represent setup / introduction
- Middle segments represent the main activity
- Later segments may represent transition, completion, or rest

4. Granularity control
- Use natural human-level activity descriptions
- Do not over-fragment into micro-actions
- Do not over-generalize into vague labels

5. Consistency rule
- If an activity continues across segments, keep naming consistent
- If it changes meaningfully, reflect that change clearly

Return STRICT JSON ONLY:

{
  "overall_video": "One-sentence summary of the entire video",
  "segments": [
    {
      "segment_id": 0,
      "activity": "short descriptive label of activity",
      "about": "clear explanation grounded in visual evidence"
    }
  ]
}
"""

    content.append({
        "type": "input_text",
        "text": prompt
    })

    for seg in segments:

        content.append({
            "type": "input_text",
            "text":
            f"""
Segment {seg['segment_id']}
Frames: {seg['frames']}
"""
        })

        for img in seg["images"]:

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