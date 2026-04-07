"""
scenarios/local_crisis.py — IAM scenario: local crisis propagation

A 32×32 grid where a 5×5 "crisis region" in the centre is initialised at 1500.0
while the rest of the field sits at the standard 1000.0.

Import and use directly:
    from scenarios.local_crisis import make_crisis_grid
    grid = make_crisis_grid()

Or run standalone to see the live animation:
    python scenarios/local_crisis.py
"""

import numpy as np

INIT_NORMAL = 1000.0
INIT_CRISIS = 1500.0
SIZE = 32
CRISIS_RADIUS = 2  # cells on each side of centre


def make_crisis_grid(size: int = SIZE) -> np.ndarray:
    """Return a 2-D grid with a central crisis patch at INIT_CRISIS."""
    grid = np.full((size, size), INIT_NORMAL, dtype=float)
    cx, cy = size // 2, size // 2
    r = CRISIS_RADIUS
    grid[cx - r : cx + r + 1, cy - r : cy + r + 1] = INIT_CRISIS
    return grid


if __name__ == "__main__":
    import sys
    import os

    # Allow running as: python scenarios/local_crisis.py
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from iam_sim import step, VMIN, VMAX

    grid = make_crisis_grid()
    t = [0]
    frames = 120
    state = {"grid": grid}

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    im = ax.imshow(state["grid"], vmin=VMIN, vmax=VMAX, cmap="viridis", origin="lower", aspect="auto")
    plt.colorbar(im, ax=ax)
    ax.set_title(f"3\u00b3OS — Local Crisis Scenario (32\u00d732)")
    ax.set_xlabel(f"t = {t[0]}")

    def _update(_frame):
        state["grid"] = step(state["grid"])
        t[0] += 1
        im.set_data(state["grid"])
        ax.set_xlabel(f"t = {t[0]}")
        return [im]

    ani = animation.FuncAnimation(fig, _update, frames=frames, interval=80, blit=False)
    plt.tight_layout()
    plt.show()
