# Ensure that all libraries are installed before testing the code
# torch, numpy, PIL, cv2
import os
import sys
import glob
import cv2
import numpy as np
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image

# Reference: DSINE - Rethinking Inductive Biases for Surface Normal Estimation
# https://github.com/baegwangbin/DSINE
# CVPR 2024 Oral

# ── PATH SETUP ────────────────────────────────────────────
# point this to where you downloaded DSINE
DSINE_PATH = 'path/to/your/DSINE'
sys.path.append(DSINE_PATH)

import utils.utils as utils
from utils.projection import intrins_from_fov
# ──────────────────────────────────────────────────────────

# device setup - GPU if available, otherwise CPU
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

# load DSINE model via torch hub
model = torch.hub.load(
    DSINE_PATH,
    "DSINE",
    source="local",
    trust_repo=True
)
model.to(device)
model.eval()

# input normalisation - same values DSINE was trained with
normalize = transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
)

# output folder
os.makedirs('data/output', exist_ok=True)


def generate_normal_map(image_path):
    """ Generates a surface normal map from a given image using DSINE.
        Saves the result to data/output as a PNG.
        Returns the raw normal map as a numpy array for use in Open3D.
    """
    print(f"Processing: {image_path}")

    # load and preprocess image
    img = Image.open(image_path).convert('RGB')
    img_np = np.array(img).astype(np.float32) / 255.0
    img_tensor = torch.from_numpy(img_np).permute(2, 0, 1).unsqueeze(0).to(device)

    # store original dimensions
    _, _, orig_H, orig_W = img_tensor.shape

    # pad so dimensions are multiples of 32
    lrtb = utils.get_padding(orig_H, orig_W)
    img_tensor = F.pad(img_tensor, lrtb, mode="constant", value=0.0)
    img_tensor = normalize(img_tensor)

    # estimate camera intrinsics from FOV
    intrins = intrins_from_fov(
        new_fov=60.0,
        H=orig_H,
        W=orig_W,
        device=device
    ).unsqueeze(0)

    # adjust intrinsics for padding
    intrins[:, 0, 2] += lrtb[0]
    intrins[:, 1, 2] += lrtb[2]

    # run inference
    with torch.no_grad():
        pred_norm = model(img_tensor, intrins=intrins)[-1]

    # remove padding
    pred_norm = pred_norm[:, :, lrtb[2]:lrtb[2]+orig_H, lrtb[0]:lrtb[0]+orig_W]

    # convert to numpy - shape (H, W, 3) range [-1, 1]
    pred_norm_np = pred_norm.detach().cpu().permute(0, 2, 3, 1).numpy()[0]

    # save as PNG for visualisation
    filename = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join('data/output', filename + '_normal.png')

    pred_norm_vis = (((pred_norm_np + 1) * 0.5) * 255).astype(np.uint8)
    im = Image.fromarray(pred_norm_vis)
    im.save(output_path)
    print(f"Saved normal map to: {output_path}")

    return pred_norm_np  # raw float32 array for Open3D


def process_all_images():
    """ Process all images in the data folder. """
    img_paths = glob.glob('data/*.png') + glob.glob('data/*.jpg')
    img_paths.sort()

    if not img_paths:
        print("No images found in data/ folder")
        return

    results = {}
    for img_path in img_paths:
        normal_map = generate_normal_map(img_path)
        results[img_path] = normal_map
        print(f"Normal map shape: {normal_map.shape}")

    return results


# run
process_all_images()