# Physics Study Note

## 1. Physical picture

A bilayer contains two perfectly bonded films. Layer 1 has thickness `t1`, modulus `E1`, and a preferred in-plane strain different from layer 2. While attached to a substrate, the pair cannot adopt both preferred lengths, so it stores elastic energy. Release removes the supporting constraint. Bending lets the outside of the curve become longer than the inside and therefore relieves part of the mismatch.

Curvature is `kappa = 1/R`, where `R` is radius. Large curvature means a tight tube; small curvature means a large tube.

## 2. From strain to force and moment

For a thin beam or membrane, axial strain changes linearly through thickness during bending:

```text
actual strain at height z = mid-plane strain + kappa * z
```

Each layer also has its own preferred, or built-in, strain. Elastic strain is the actual strain minus that preferred strain. Hooke's law then gives stress:

```text
stress = Young's modulus * elastic strain
```

The released strip has no external pull and no external bending moment. Integrating stress through both layers therefore gives two conditions: total axial force is zero, and total moment is zero. Solving those two equations removes the unknown mid-plane strain and leaves the Timoshenko composite-beam curvature:

```text
             6 E1 E2 t1 t2 (t1 + t2) Delta_epsilon
kappa = -------------------------------------------------------
        E1^2 t1^4 + E2^2 t2^4
        + 2 E1 E2 t1 t2 (2 t1^2 + 3 t1 t2 + 2 t2^2)
```

Here `Delta_epsilon = epsilon1 - epsilon2`. Its sign chooses the rolling direction. This project reports the positive radius `R = 1/abs(kappa)`.

The numerator is the mismatch-driven bending action. The denominator is the bilayer's resistance to bending, including coupling between the bonded layers. In a very thin film on a much thicker substrate, this family of force-and-moment balances leads to the familiar Stoney approximation. Because rolled membranes often have comparable layer thicknesses, the code keeps the full bilayer expression.

## 3. Equal-layer and plane-strain result

If `t1 = t2 = d` and `E1 = E2`, all modulus factors cancel and the expression simplifies to:

```text
kappa = 3 Delta_epsilon / (4d)
R = 4d / (3 abs(Delta_epsilon))
```

Cendula et al. assume no relaxation along the tube axis (plane strain). Under their convention, the effective mismatch is multiplied by `1 + nu`, where `nu` is Poisson's ratio:

```text
R0 = 4d / (3 abs(Delta_epsilon) (1 + nu))
```

For their strained layer `epsilon1` is negative and the other layer is unstrained, so their signed presentation is `R0 = 4d / (-3 epsilon1 (1 + nu))`.

## 4. Worked example: sample batch A

Given:

- `d = 20 nm = 20 x 10^-9 m`
- `abs(Delta_epsilon) = 0.71% = 0.0071`
- `nu = 0.31`
- both Young's moduli are `80 GPa`; they cancel for equal layers

Substitute into the specialized result:

```text
R0 = 4(20 x 10^-9) / [3(0.0071)(1 + 0.31)]
   = 80 x 10^-9 / 0.027903
   = 2.867 x 10^-6 m
   = 2.87 micrometres
```

The paper rounds the expected value to `2.9 µm`. Halving both layer thicknesses to 10 nm halves the radius to about `1.43 µm`, consistent with its reported `1.45 µm` for batch B.

## 5. Mapping the note to `curvature.py`

`radius_of_curvature` accepts SI units: metres, pascals, and dimensionless strain. It first checks that inputs are physically meaningful. With `plane_strain=True`, it converts the supplied mismatch to `mismatch * (1 + poisson_ratio)`. It then evaluates the numerator and denominator written above, computes curvature, and returns its inverse magnitude. A zero mismatch returns an infinite radius, representing a flat film.

The model assumes linear elasticity, perfect bonding, uniform layers, and thicknesses much smaller than the radius. Real released membranes may also wrinkle, crack, stick to nearby surfaces, or relax plastically. Those effects explain why a measured local radius need not equal this ideal equilibrium prediction.

## Reference

P. Cendula et al., [*Nano Letters* 14, 4839-4845 (2014)](https://doi.org/10.1021/nl502108q); [arXiv:1407.5811](https://arxiv.org/abs/1407.5811).

