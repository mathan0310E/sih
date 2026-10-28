"""Render every vector icon used in the deck to a transparent PNG."""
import os
from svglib import icon, render, NAVY, ORANGE, TEAL, PURPLE, CRIMSON, GREEN
WHITE = "#FFFFFF"

OUT = "/workspace/project/assets/icons"
S = 24          # icon box in svg units
PX = 96         # rendered pixels (square, transparent)

NAMES = ["target", "bulb", "book", "scales", "gear", "search", "people", "globe",
         "shield", "pen", "check", "quest", "heart", "cap", "chat", "grid",
         "chart", "compass", "handshake"]

COLORS = {"navy": NAVY, "orange": ORANGE, "teal": TEAL, "purple": PURPLE,
          "crimson": CRIMSON, "green": GREEN, "white": WHITE}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for name in NAMES:
        for cname, cval in COLORS.items():
            body = icon(name, S / 2, S / 2, S * 0.94, cval)
            p = render(f"{name}_{cname}", S, S, body, OUT, bg=None, scale=PX / S)
            n += 1
    print(f"rendered {n} icons into {OUT}")
