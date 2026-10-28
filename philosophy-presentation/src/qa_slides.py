"""Detect text clipping at slide edges and elements colliding with the frame."""
import glob, os, sys
from PIL import Image
import numpy as np

W, H = 1334, 750          # 100 dpi render of 13.333x7.5in
SAFE = 14                 # px margin we require inside the page edge

def ink(a):
    r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
    lum = 0.299*r + 0.587*g + 0.114*b
    sat = a.max(axis=2) - a.min(axis=2)
    return (lum < 210) | (sat > 45)

def qa(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    m = ink(a)
    # ignore the intentional left orange spine (x<16) and header rule band
    m2 = m.copy()
    m2[:, :17] = False
    ys, xs = np.nonzero(m2)
    if len(xs) == 0:
        return ["EMPTY slide"], None
    marg = dict(l=int(xs.min()), r=int(W-1-xs.max()), t=int(ys.min()), b=int(H-1-ys.max()))
    probs = []
    if marg["r"] < SAFE: probs.append(f"text/graphic near RIGHT edge (margin {marg['r']}px)")
    if marg["b"] < 8:    probs.append(f"content near BOTTOM edge (margin {marg['b']}px)")
    if marg["t"] < 4:    probs.append(f"content at TOP edge (margin {marg['t']}px)")
    return probs, marg

files = sorted(glob.glob("/workspace/project/out/slides/*.png"))
tot = 0
for f in files:
    probs, marg = qa(f)
    tag = os.path.basename(f)
    if probs:
        tot += len(probs)
        print(f"WARN {tag} margins={marg}")
        for p in probs: print("      ->", p)
    else:
        print(f" ok  {tag} margins={marg}")
print("total layout problems:", tot)
