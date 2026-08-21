"""Sweep equal layer thickness and strain mismatch, then plot tube diameter."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from curvature import radius_of_curvature


def main() -> None:
    thickness_nm = np.linspace(5.0, 50.0, 100)
    mismatch_percent = np.linspace(0.2, 1.2, 100)
    thickness_grid, mismatch_grid = np.meshgrid(thickness_nm, mismatch_percent)

    # Evaluate each thickness/strain pair after converting nm and percent to SI.
    diameter_um = np.empty_like(thickness_grid)
    for index in np.ndindex(thickness_grid.shape):
        radius = radius_of_curvature(
            thickness_grid[index] * 1e-9,
            thickness_grid[index] * 1e-9,
            80e9,
            80e9,
            mismatch_grid[index] / 100.0,
            0.31,
            plane_strain=True,
        )
        diameter_um[index] = 2.0 * radius * 1e6

    figure, axis = plt.subplots(figsize=(8, 6))
    contours = axis.contourf(thickness_grid, mismatch_grid, diameter_um, levels=25, cmap="viridis")
    figure.colorbar(contours, ax=axis, label="tube diameter (µm)")
    axis.set(xlabel="thickness of each layer (nm)", ylabel="strain mismatch (%)", title="Bilayer tube diameter parameter sweep")
    output = Path("outputs/parameter_sweep.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(figure)
    print(f"Saved {output}")


if __name__ == "__main__":
    main()

