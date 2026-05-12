import os
import cv2
import torch
import numpy as np

from PIL import Image
import torchvision.transforms as T
from preprocessing.device import get_device


# ============================================================
# DINO EMBEDDINGS
# ============================================================

def attach_dino_embeddings(
    all_frames_data,
    frames_dir
):

    device = get_device()

    dinov2 = torch.hub.load(
        'facebookresearch/dinov2',
        'dinov2_vits14'
    )

    dinov2 = dinov2.to(device).eval()

    transform = T.Compose([

        T.Resize((224, 224)),

        T.ToTensor(),

        T.Normalize(
            mean=(0.485, 0.456, 0.406),
            std=(0.229, 0.224, 0.225)
        )
    ])

    frame_names = sorted(
        [
            f for f in os.listdir(frames_dir)
            if f.endswith(".jpg")
        ],
        key=lambda x:
            int(os.path.splitext(x)[0])
    )

    for frame_idx, frame_name in enumerate(
        frame_names
    ):

        frame_path = os.path.join(
            frames_dir,
            frame_name
        )

        frame = cv2.imread(frame_path)

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        frame_data = all_frames_data[
            frame_idx
        ]

        embeddings = extract_embeddings(
            frame,
            frame_data,
            transform,
            dinov2,
            device
        )

        trackid_to_emb = {

            e["track_id"]:
                e["embedding"]

            for e in embeddings
        }

        for obj in frame_data:

            track_id = obj["track_id"]

            if track_id in trackid_to_emb:

                obj["embedding"] = (
                    trackid_to_emb[track_id]
                )

            else:

                obj["embedding"] = None

        print(
            f"Frame {frame_idx}: "
            f"{len(embeddings)} embeddings"
        )

    return all_frames_data


# ============================================================
# EXTRACT EMBEDDINGS
# ============================================================

def extract_embeddings(
    frame,
    frame_data,
    transform,
    dinov2,
    device,
    batch_size=8
):

    crops = []

    meta = []

    for obj in frame_data:

        mask = obj.get(
            "mask",
            None
        )

        track_id = obj["track_id"]

        if mask is None:
            continue

        if mask.ndim == 3:
            mask = mask[0]

        mask = mask.astype(np.uint8)

        masked = frame * mask[..., None]

        ys, xs = np.where(mask > 0)

        if len(xs) == 0:
            continue

        x1, x2 = xs.min(), xs.max()

        y1, y2 = ys.min(), ys.max()

        if (x2 - x1) < 10:
            continue

        crop = masked[
            y1:y2,
            x1:x2
        ].astype("uint8")

        crop_pil = Image.fromarray(crop)

        tensor = transform(crop_pil)

        crops.append(tensor)

        meta.append(track_id)

    if len(crops) == 0:
        return []

    crops = torch.stack(crops)

    crops = crops.to(device).float()

    embeddings = []

    with torch.no_grad():

        for i in range(
            0,
            len(crops),
            batch_size
        ):

            batch = crops[
                i:i+batch_size
            ]

            emb = dinov2(batch)

            emb = emb.cpu().numpy()

            for j in range(len(emb)):

                embeddings.append({

                    "track_id":
                        meta[i + j],

                    "embedding":
                        emb[j]
                })

    return embeddings