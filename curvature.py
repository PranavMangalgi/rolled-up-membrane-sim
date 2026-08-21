"""Elastic curvature models for released, strained bilayer membranes.

The implementation uses the classical composite-beam result associated with
Timoshenko's bimetal-strip analysis.  Stoney's equation is recovered as the
thin-coating/thick-substrate limit, while the full expression remains valid
when both layers contribute appreciably to the bending stiffness.
"""

from __future__ import annotations

import math


def radius_of_curvature(
    thickness_1: float,
    thickness_2: float,
    youngs_modulus_1: float,
    youngs_modulus_2: float,
    strain_mismatch: float,
    poisson_ratio: float | None = None,
    *,
    plane_strain: bool = False,
) -> float:
    """Return the equilibrium radius of a freely bending bilayer, in metres.

    Parameters
    ----------
    thickness_1, thickness_2:
        Thicknesses of layers 1 and 2 in metres.  Both must be positive.  A
        thickness sets both the lever arm of a layer's internal force and its
        resistance to bending, so changing it affects more than total film
        thickness.
    youngs_modulus_1, youngs_modulus_2:
        Young's moduli in pascals.  A larger modulus makes a layer carry more
        force for the same elastic strain.  Both must be positive.
    strain_mismatch:
        Dimensionless difference in the layers' preferred in-plane strains,
        ``epsilon_1 - epsilon_2``.  For example, 0.0071 means 0.71%.  The sign
        selects which way the bilayer curls; this function returns the
        positive radius (the magnitude of inverse curvature).
    poisson_ratio:
        Poisson's ratio used by the optional plane-strain correction.  It must
        satisfy ``-1 < nu < 0.5``.  It may be omitted for the ordinary
        one-dimensional Timoshenko strip model.
    plane_strain:
        If true, multiply the supplied mismatch by ``1 + poisson_ratio``.
        This reproduces the no-longitudinal-relaxation convention used for the
        equal-layer InGaAs/GaAs tubes in Cendula et al. (their Equation 3).

    Returns
    -------
    float
        Positive radius in metres.  Zero mismatch has zero curvature, so its
        radius is mathematically infinite and ``math.inf`` is returned.

    Notes
    -----
    Imagine cutting a narrow strip from the membrane.  If released layers
    could separate, their different preferred strains would give them
    different lengths.  Bonding prevents that.  The bilayer therefore adopts
    a common mid-plane stretch plus a linear strain change through thickness;
    that linear change is curvature.

    Force balance says the tensile and compressive forces across the free
    cross-section must cancel.  Moment balance says their bending moments must
    cancel too.  Integrating ``stress = E * elastic_strain`` through each
    layer, then solving those two balance equations, gives

    ``kappa = 6 E1 E2 t1 t2 (t1+t2) delta_epsilon / denominator``,

    where the denominator is the sum of the individual bending stiffnesses
    and their coupling about the bonded interface.  Radius is ``1/|kappa|``.
    For equal thickness ``d`` and equal modulus, this reduces to
    ``R = 4d/(3|delta_epsilon|)``.  With this project's plane-strain option it
    becomes ``R = 4d/(3|delta_epsilon|(1+nu))``, exactly the specialized form
    used in the validation paper.

    The model assumes linear elasticity, perfect bonding, uniform properties,
    small thickness compared with radius, and no plastic relaxation.
    """
    values = (thickness_1, thickness_2, youngs_modulus_1, youngs_modulus_2)
    if not all(math.isfinite(value) and value > 0 for value in values):
        raise ValueError("Thicknesses and Young's moduli must be positive and finite.")
    if not math.isfinite(strain_mismatch):
        raise ValueError("strain_mismatch must be finite.")
    if plane_strain:
        if poisson_ratio is None:
            raise ValueError("poisson_ratio is required when plane_strain=True.")
        if not math.isfinite(poisson_ratio) or not -1.0 < poisson_ratio < 0.5:
            raise ValueError("poisson_ratio must lie between -1 and 0.5.")

    mismatch = strain_mismatch * (1.0 + poisson_ratio) if plane_strain else strain_mismatch
    if mismatch == 0.0:
        return math.inf

    t1, t2 = thickness_1, thickness_2
    e1, e2 = youngs_modulus_1, youngs_modulus_2
    numerator = 6.0 * e1 * e2 * t1 * t2 * (t1 + t2) * mismatch
    denominator = (
        (e1 * t1**2) ** 2
        + (e2 * t2**2) ** 2
        + 2.0 * e1 * e2 * t1 * t2 * (2.0 * t1**2 + 3.0 * t1 * t2 + 2.0 * t2**2)
    )
    curvature = numerator / denominator
    return 1.0 / abs(curvature)

