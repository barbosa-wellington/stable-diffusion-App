# Ensure that all libraries are installed before testing the code
# torch, numpy, PIL, cv2
import os
import sys
import cv2
import numpy as np
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image

# Descobre onde o script atual está (...\backend\Dsine)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define o caminho exato para a subpasta do projeto DSINE
DSINE_PATH = os.path.join(current_dir, 'DSINE-main')

# Adiciona ao sistema para que o import 'from utils...' funcione
if DSINE_PATH not in sys.path:
    sys.path.append(DSINE_PATH)



# reference source
# DSINE - Rethinking Inductive Biases for Surface Normal Estimation
# https://github.com/baegwangbin/DSINE
# CVPR 2024 Oral

# ── DSINE path setup ──────────────────────────────────────
# DSINE_PATH = './Dsine'
# sys.path.append(DSINE_PATH)

from utils.projection import intrins_from_fov
import utils.utils as utils
# ──────────────────────────────────────────────────────────

# test image
filename = 'Dsine/data/forest-scene.png'

# device setup
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
print(f"Using device: {device}")

# load model
print("Loading DSINE model...")
CORRECT_DSINE_PATH = ("C:/Users/user/Documents/GitHub/stable-diffusion-App/backend/Dsine/DSINE-main")

model = torch.hub.load(CORRECT_DSINE_PATH, 'DSINE', source='local', trust_repo=True)

model.to(device)
model.eval()
print("Model loaded successfully!")

# normalisation
normalize = transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
)

def test_dsine(image_path):
    """ Simple test function to verify DSINE is working. """
    print(f"Processing: {image_path}")

    # load image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # convert to tensor
    img_np = img.astype(np.float32) / 255.0
    img_tensor = torch.from_numpy(img_np).permute(2, 0, 1).unsqueeze(0).to(device)
    _, _, orig_H, orig_W = img_tensor.shape

    # pad input
    lrtb = utils.get_padding(orig_H, orig_W)
    img_tensor = F.pad(img_tensor, lrtb, mode="constant", value=0.0)
    img_tensor = normalize(img_tensor)

    # intrinsics
    intrins = intrins_from_fov(
        new_fov=60.0, H=orig_H, W=orig_W, device=device
    ).unsqueeze(0)
    intrins[:, 0, 2] += lrtb[0]
    intrins[:, 1, 2] += lrtb[2]

    # run inference
    print("Running inference...")
    with torch.no_grad():
        pred_norm = model(img_tensor, intrins=intrins)[-1]

    # remove padding
    pred_norm = pred_norm[:, :, lrtb[2]:lrtb[2]+orig_H, lrtb[0]:lrtb[0]+orig_W]

    # convert to numpy
    pred_norm_np = pred_norm.detach().cpu().permute(0, 2, 3, 1).numpy()[0]

    # save result
    os.makedirs('data/output', exist_ok=True)
    normal_vis = (((pred_norm_np + 1) * 0.5) * 255).astype(np.uint8)
    im = Image.fromarray(normal_vis)
    im.save('data/output/normal_map.png')

    print(f"Success! Normal map saved to data/output/normal_map.png")
    print(f"Output shape: {pred_norm_np.shape}")
    return pred_norm_np

# run test
test_dsine(filename)