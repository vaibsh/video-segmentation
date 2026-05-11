import base64
from io import BytesIO
from PIL import Image
from config.config import JPEG_QUALITY

# ============================================================
# IMAGE RESIZE
# ============================================================

def resize_for_gpt(
    img,
    max_size=512
):

    w, h = img.size

    scale = min(
        max_size / w,
        max_size / h
    )

    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))

    return img.resize(
        (new_w, new_h),
        Image.LANCZOS
    )


# ============================================================
# PIL → DATA URL
# Converts PIL image to base64-encoded data url
# ============================================================

def pil_to_data_url(img):

    buffer = BytesIO()

    img.save(
        buffer,
        format="JPEG",
        quality=JPEG_QUALITY
    )

    b64 = base64.b64encode(
        buffer.getvalue()
    ).decode()

    return (
        f"data:image/jpeg;base64,{b64}"
    )