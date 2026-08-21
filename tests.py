"""Regression and sanity checks for the bilayer curvature model."""

import math
import unittest

from curvature import radius_of_curvature


class CurvatureTests(unittest.TestCase):
    def test_cendula_batch_a(self):
        radius = radius_of_curvature(20e-9, 20e-9, 80e9, 80e9, 0.0071, 0.31, plane_strain=True)
        self.assertAlmostEqual(radius, 2.9e-6, delta=0.05e-6)

    def test_cendula_batch_b_scales_with_thickness(self):
        radius = radius_of_curvature(10e-9, 10e-9, 80e9, 80e9, 0.0071, 0.31, plane_strain=True)
        self.assertAlmostEqual(radius, 1.45e-6, delta=0.03e-6)

    def test_equal_layer_timoshenko_limit(self):
        radius = radius_of_curvature(20e-9, 20e-9, 80e9, 80e9, 0.0071)
        self.assertAlmostEqual(radius, 4 * 20e-9 / (3 * 0.0071), places=15)

    def test_zero_mismatch_is_flat(self):
        self.assertTrue(math.isinf(radius_of_curvature(20e-9, 20e-9, 80e9, 80e9, 0.0)))

    def test_invalid_thickness_is_rejected(self):
        with self.assertRaises(ValueError):
            radius_of_curvature(0.0, 20e-9, 80e9, 80e9, 0.0071)


if __name__ == "__main__":
    unittest.main()
