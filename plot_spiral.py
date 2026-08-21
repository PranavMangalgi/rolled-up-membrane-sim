"""Plot an idealized 2D cross-section of a rolled-up membrane."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from curvature import radius_of_curvature


def spiral_coordinates(radius: float, total_thickness: float, windings: float, points: int = 1500):
    """Return polar coordinates for an Archimedean membrane spiral."""
    # Polar angle advances by 2*pi for every complete winding.
    theta = np.linspace(0.0, 2.0 * np.pi * windings, points)
    # Each full turn moves outward by one bilayer thickness, preventing overlap.
    radial_distance = radius + total_thickness * theta / (2.0 * np.pi)
    return theta, radial_distance


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--windings", type=float, default=3.0)
    parser.add_argument("--output", type=Path, default=Path("outputs/spiral.png"))
    args = parser.parse_args()

    radius = radius_of_curvature(20e-9, 20e-9, 80e9, 80e9, 0.0071, 0.31, plane_strain=True)
    theta, radial_distance = spiral_coordinates(radius, 40e-9, args.windings)

    figure, axis = plt.subplots(subplot_kw={"projection": "polar"}, figsize=(7, 7))
    axis.plot(theta, radial_distance * 1e6, linewidth=2)
    axis.set_title(f"Rolled bilayer cross-section ({args.windings:g} windings)")
    axis.set_ylabel("radius (µm)", labelpad=28)
    axis.grid(alpha=0.4)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(args.output, dpi=180, bbox_inches="tight")
    plt.close(figure)
    print(f"Saved {args.output} (equilibrium radius {radius * 1e6:.3f} µm)")


if __name__ == "__main__":
    main()

