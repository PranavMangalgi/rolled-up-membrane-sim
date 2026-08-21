"""Render an idealized rolled membrane as a three-dimensional tube surface."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from curvature import radius_of_curvature


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--windings", type=float, default=3.0)
    parser.add_argument("--length-um", type=float, default=12.0)
    parser.add_argument("--output", type=Path, default=Path("outputs/tube_3d.png"))
    args = parser.parse_args()

    layer_thickness = 20e-9
    radius = radius_of_curvature(layer_thickness, layer_thickness, 80e9, 80e9, 0.0071, 0.31, plane_strain=True)

    # Theta traces the rolled edge; z extrudes that edge along the tube axis.
    theta = np.linspace(0.0, 2.0 * np.pi * args.windings, 500)
    z_axis = np.linspace(0.0, args.length_um * 1e-6, 80)
    theta_grid, z_grid = np.meshgrid(theta, z_axis)
    # An Archimedean radius adds one complete bilayer thickness per revolution.
    radial_grid = radius + 2.0 * layer_thickness * theta_grid / (2.0 * np.pi)
    # Convert cylindrical coordinates into Cartesian coordinates for mplot3d.
    x_grid = radial_grid * np.cos(theta_grid)
    y_grid = radial_grid * np.sin(theta_grid)

    figure = plt.figure(figsize=(10, 7))
    axis = figure.add_subplot(111, projection="3d")
    axis.plot_surface(x_grid * 1e6, y_grid * 1e6, z_grid * 1e6, cmap="viridis", linewidth=0, alpha=0.9)
    axis.set(xlabel="x (µm)", ylabel="y (µm)", zlabel="tube axis (µm)", title="Idealized rolled-up bilayer tube")
    axis.set_box_aspect((1, 1, 1.8))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(args.output, dpi=180, bbox_inches="tight")
    plt.close(figure)
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()

