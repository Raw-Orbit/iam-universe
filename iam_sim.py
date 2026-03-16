"""
i.am — IAM Simulation
Raw Orbit / Vibe Wizzards Wyrd (vww 3³)

Visualise 2-D and 3-D IAM grids as heatmaps.

Usage
-----
    python iam_sim.py 2d                # 2-D final-state plot (32×32)
    python iam_sim.py 2d-live           # 2-D live animation
    python iam_sim.py 3d                # 3-D CLI slice at X=8 (16³)
    python iam_sim.py 3d-cosmos         # 3-D COSMOS slice at Y=8 (16³)
    python iam_sim.py --help
"""

import argparse
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ── constants ──────────────────────────────────────────────────────────────────
VMIN = 900
VMAX = 1100
SIZE_2D = 32
SIZE_3D = 16
INIT_STANDARD = 1000.0
INIT_COSMOS = 1075.0

# ── grid helpers ───────────────────────────────────────────────────────────────

def make_2d(size: int = SIZE_2D, init: float = INIT_STANDARD) -> np.ndarray:
    """Return a uniform 2-D IAM grid."""
    return np.full((size, size), init, dtype=float)


def make_3d(size: int = SIZE_3D, init: float = INIT_STANDARD) -> np.ndarray:
    """Return a uniform 3-D IAM grid."""
    return np.full((size, size, size), init, dtype=float)


def step(grid: np.ndarray) -> np.ndarray:
    """One nearest-neighbour averaging step (uniform grids stay uniform)."""
    out = grid.copy()
    slc = tuple(slice(1, -1) for _ in grid.shape)
    n = 2 * grid.ndim
    neighbors = sum(
        np.roll(grid, shift, axis=ax)[slc]
        for ax in range(grid.ndim)
        for shift in (+1, -1)
    )
    out[slc] = (neighbors + grid[slc]) / (n + 1)
    return out


# ── colormap helper ────────────────────────────────────────────────────────────

def _cmap(mode: str) -> str:
    return "plasma" if mode == "cosmos" else "viridis"


# ── visualisation functions ────────────────────────────────────────────────────

def show_2d_final(
    size: int = SIZE_2D,
    steps: int = 60,
    init: float = INIT_STANDARD,
) -> None:
    """Run a 2-D simulation and show the final state as a heatmap."""
    grid = make_2d(size, init)
    for _ in range(steps):
        grid = step(grid)

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    im = ax.imshow(
        grid, vmin=VMIN, vmax=VMAX, cmap="viridis", origin="lower", aspect="auto"
    )
    plt.colorbar(im, ax=ax)
    ax.set_title(f"IAM 2D \u2013 letzter Zustand ({size}x{size})")
    plt.tight_layout()
    plt.show()


def show_2d_live(
    size: int = SIZE_2D,
    frames: int = 60,
    init: float = INIT_STANDARD,
) -> None:
    """Run a 2-D simulation with a live animated heatmap."""
    grid = make_2d(size, init)
    t = [0]

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    im = ax.imshow(
        grid, vmin=VMIN, vmax=VMAX, cmap="viridis", origin="lower", aspect="auto"
    )
    plt.colorbar(im, ax=ax)
    ax.set_title(f"IAM 2D \u2013 live ({size}x{size})")
    ax.set_xlabel(f"t = {t[0]}")

    def _update(_frame):
        nonlocal grid
        grid = step(grid)
        t[0] += 1
        im.set_data(grid)
        ax.set_xlabel(f"t = {t[0]}")
        return [im]

    ani = animation.FuncAnimation(
        fig, _update, frames=frames, interval=100, blit=False
    )
    plt.tight_layout()
    plt.show()


def show_3d_slice(
    size: int = SIZE_3D,
    axis: str = "x",
    idx: int = 8,
    mode: str = "cli",
    init: float = INIT_STANDARD,
) -> None:
    """Show one axis-aligned slice of a 3-D IAM grid as a heatmap."""
    grid = make_3d(size, init)
    axis = axis.lower()

    if axis == "x":
        data, label = grid[idx, :, :], f"X={idx}"
    elif axis == "y":
        data, label = grid[:, idx, :], f"Y={idx}"
    else:
        data, label = grid[:, :, idx], f"Z={idx}"

    if mode == "cosmos":
        title = f"IAM COSMOS 3D ({size}\u00b3) \u2013 {label}"
    else:
        title = f"IAM 3D ({size}\u00b3, {mode.upper()}) \u2013 {label}"

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    im = ax.imshow(
        data, vmin=VMIN, vmax=VMAX, cmap=_cmap(mode), origin="lower", aspect="auto"
    )
    plt.colorbar(im, ax=ax)
    ax.set_title(title)
    plt.tight_layout()
    plt.show()


# ── CLI ────────────────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="iam_sim",
        description="i.am \u2014 IAM Simulation (Raw Orbit / Vibe Wizzards Wyrd)",
    )
    sub = p.add_subparsers(dest="cmd")

    # 2d ───────────────────────────────────────────────────────────────────────
    p2 = sub.add_parser("2d", help="2-D simulation \u2014 final state heatmap")
    p2.add_argument("--size", type=int, default=SIZE_2D, help="Grid side length")
    p2.add_argument("--steps", type=int, default=60, help="Simulation steps")
    p2.add_argument("--init", type=float, default=INIT_STANDARD, help="Initial value")

    # 2d-live ──────────────────────────────────────────────────────────────────
    pl = sub.add_parser("2d-live", help="2-D simulation \u2014 live animation")
    pl.add_argument("--size", type=int, default=SIZE_2D, help="Grid side length")
    pl.add_argument("--frames", type=int, default=60, help="Animation frames")
    pl.add_argument("--init", type=float, default=INIT_STANDARD, help="Initial value")

    # 3d ───────────────────────────────────────────────────────────────────────
    p3 = sub.add_parser("3d", help="3-D simulation \u2014 CLI mode slice")
    p3.add_argument("--size", type=int, default=SIZE_3D, help="Grid side length")
    p3.add_argument("--axis", choices=["x", "y", "z"], default="x", help="Slice axis")
    p3.add_argument("--idx", type=int, default=8, help="Slice index")
    p3.add_argument("--init", type=float, default=INIT_STANDARD, help="Initial value")

    # 3d-cosmos ────────────────────────────────────────────────────────────────
    pc = sub.add_parser("3d-cosmos", help="3-D simulation \u2014 COSMOS mode slice")
    pc.add_argument("--size", type=int, default=SIZE_3D, help="Grid side length")
    pc.add_argument("--axis", choices=["x", "y", "z"], default="y", help="Slice axis")
    pc.add_argument("--idx", type=int, default=8, help="Slice index")
    pc.add_argument("--init", type=float, default=INIT_COSMOS, help="Initial value")

    return p


def main(argv=None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.cmd == "2d":
        show_2d_final(size=args.size, steps=args.steps, init=args.init)
    elif args.cmd == "2d-live":
        show_2d_live(size=args.size, frames=args.frames, init=args.init)
    elif args.cmd == "3d":
        show_3d_slice(
            size=args.size, axis=args.axis, idx=args.idx, mode="cli", init=args.init
        )
    elif args.cmd == "3d-cosmos":
        show_3d_slice(
            size=args.size,
            axis=args.axis,
            idx=args.idx,
            mode="cosmos",
            init=args.init,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
