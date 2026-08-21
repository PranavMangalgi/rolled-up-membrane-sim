# Code Overview

## Repository map

```text
curvature.py          physics calculation shared by every simulation
plot_spiral.py        2D polar cross-section
plot_3d_tube.py       3D extrusion of the spiral along a tube axis
parameter_sweep.py    thickness/strain study and diameter contour plot
tests.py              literature regression checks and edge cases
requirements.txt      Python packages needed to run the project
docs/PHYSICS.md       formula, derivation logic, and worked example
docs/CODE_OVERVIEW.md this file
```

## Data flow

```text
thicknesses + moduli + strain mismatch
                    |
                    v
       curvature.radius_of_curvature
                    |
             radius in metres
          /         |          \
         v          v           v
  2D spiral     3D tube    parameter sweep
```

## `curvature.py`

`radius_of_curvature(t1, t2, E1, E2, mismatch, poisson_ratio=None, *, plane_strain=False)` is the central function. Thickness inputs are metres, moduli are pascals, and mismatch is a decimal strain such as `0.0071`, not the number `0.71`. It returns a positive radius in metres. Set `plane_strain=True` and provide Poisson's ratio to use the convention of the validation paper.

## `plot_spiral.py`

This script calculates the batch-A radius, samples angle from zero to the requested number of turns, and increases radial distance by one bilayer thickness per complete turn. Matplotlib displays those arrays in polar coordinates. `--windings` controls the number of turns and `--output` chooses the image path.

The helper `spiral_coordinates(radius, total_thickness, windings, points=1500)` accepts metres and returns two NumPy arrays: angle in radians and radial distance in metres.

## `plot_3d_tube.py`

This repeats the spiral across positions along the tube axis. A mesh of angle and axial position is converted from cylindrical coordinates to Cartesian `x`, `y`, and `z`, then drawn as a surface. `--windings`, `--length-um`, and `--output` are command-line inputs.

## `parameter_sweep.py`

This varies equal layer thickness from 5 to 50 nm and mismatch from 0.2% to 1.2%. Every grid point calls the same curvature function. Radius is doubled to obtain diameter, converted to micrometres, and displayed as a filled contour plot. This makes two trends easy to see: thicker films form larger tubes, while larger mismatch produces tighter, smaller tubes.

## `tests.py`

The standard-library `unittest` runner checks Cendula et al.'s 20+20 nm and 10+10 nm batches, the equal-layer analytical limit, the flat zero-mismatch case, and invalid input handling. Run it with `python tests.py`.

All plot scripts save into `outputs/`, a generated folder excluded from Git. They use the non-interactive save workflow, so they also work on machines without a desktop display.
