"""Unit tests for problem7.py (Deliverable 3, Problem 8).

Uses Python's built-in unittest framework (PyUnit). math.acos() and
math.asin() are used only as verification oracles. The production module
does not import math.
"""

# pylint: disable=missing-function-docstring

import math
import unittest
from unittest.mock import patch

import problem7
from problem7 import (
    ConvergenceError,
    InputValidationError,
    PI,
    absolute_value,
    calculate_arccos,
    calculate_arcsin,
    calculate_square_root,
    is_finite_number,
    is_not_a_number,
)


class TestAbsoluteValue(unittest.TestCase):
    """Tests for absolute_value()."""

    def test_positive_value(self):
        self.assertEqual(absolute_value(3.5), 3.5)

    def test_negative_value(self):
        self.assertEqual(absolute_value(-3.5), 3.5)

    def test_zero(self):
        self.assertEqual(absolute_value(0.0), 0.0)


class TestIsNotANumber(unittest.TestCase):
    """Tests for is_not_a_number()."""

    def test_nan_is_detected(self):
        self.assertTrue(is_not_a_number(float("nan")))

    def test_finite_number_is_not_nan(self):
        self.assertFalse(is_not_a_number(1.0))


class TestIsFiniteNumber(unittest.TestCase):
    """Tests for is_finite_number()."""

    def test_nan_is_not_finite(self):
        self.assertFalse(is_finite_number(float("nan")))

    def test_positive_infinity_is_not_finite(self):
        self.assertFalse(is_finite_number(float("inf")))

    def test_negative_infinity_is_not_finite(self):
        self.assertFalse(is_finite_number(float("-inf")))

    def test_normal_values_are_finite(self):
        self.assertTrue(is_finite_number(0.0))
        self.assertTrue(is_finite_number(-0.75))
        self.assertTrue(is_finite_number(1.0))


class TestCalculateSquareRoot(unittest.TestCase):
    """Tests for calculate_square_root()."""

    def test_sqrt_zero(self):
        self.assertEqual(calculate_square_root(0.0), 0.0)

    def test_sqrt_one(self):
        self.assertAlmostEqual(calculate_square_root(1.0), 1.0, places=10)

    def test_sqrt_four(self):
        self.assertAlmostEqual(calculate_square_root(4.0), 2.0, places=10)

    def test_negative_input_raises(self):
        with self.assertRaises(InputValidationError):
            calculate_square_root(-1.0)


class TestCalculateArcsin(unittest.TestCase):
    """Tests for calculate_arcsin()."""

    def test_arcsin_zero_and_endpoints(self):
        """Test zero and both exact arcsin endpoints."""
        self.assertEqual(calculate_arcsin(0.0), 0.0)
        self.assertEqual(calculate_arcsin(1.0), PI / 2.0)
        self.assertEqual(calculate_arcsin(-1.0), -PI / 2.0)

    def test_arcsin_half(self):
        expected = math.asin(0.5)
        self.assertAlmostEqual(
            calculate_arcsin(0.5),
            expected,
            places=6,
        )

    def test_arcsin_domain_and_convergence_errors(self):
        """Test invalid input and the convergence-failure path."""
        with self.assertRaises(InputValidationError):
            calculate_arcsin(1.5)

        with patch.object(problem7, "MAX_ITERATIONS", 0):
            with self.assertRaises(ConvergenceError):
                problem7.calculate_arcsin(0.5)


class TestCalculateArccos(unittest.TestCase):
    """Tests for calculate_arccos()."""

    REQUIRED_TOLERANCE = 1e-6

    def assert_arccos_matches_reference(self, value):
        expected = math.acos(value)
        actual = calculate_arccos(value)
        error = abs(actual - expected)
        self.assertLessEqual(
            error,
            self.REQUIRED_TOLERANCE,
            msg=(
                "Absolute error for x="
                + str(value)
                + " was "
                + str(error)
                + ", exceeding 1e-6 radians."
            ),
        )

    def test_endpoint_positive_one(self):
        self.assertEqual(calculate_arccos(1.0), 0.0)

    def test_endpoint_negative_one(self):
        self.assertEqual(calculate_arccos(-1.0), PI)

    def test_zero_matches_reference(self):
        self.assert_arccos_matches_reference(0.0)

    def test_quarter_matches_reference(self):
        self.assert_arccos_matches_reference(0.25)

    def test_positive_half_matches_reference(self):
        self.assert_arccos_matches_reference(0.5)

    def test_three_quarters_matches_reference(self):
        self.assert_arccos_matches_reference(0.75)

    def test_negative_half_matches_reference(self):
        self.assert_arccos_matches_reference(-0.5)

    def test_near_upper_endpoint_matches_reference(self):
        self.assert_arccos_matches_reference(0.9999)

    def test_near_lower_endpoint_matches_reference(self):
        self.assert_arccos_matches_reference(-0.9999)

    def test_above_domain_raises(self):
        with self.assertRaises(InputValidationError):
            calculate_arccos(2.0)

    def test_below_domain_raises(self):
        with self.assertRaises(InputValidationError):
            calculate_arccos(-1.0001)

    def test_nan_raises(self):
        with self.assertRaises(InputValidationError):
            calculate_arccos(float("nan"))

    def test_positive_infinity_raises(self):
        with self.assertRaises(InputValidationError):
            calculate_arccos(float("inf"))

    def test_negative_infinity_raises(self):
        with self.assertRaises(InputValidationError):
            calculate_arccos(float("-inf"))


class TestPrincipalRange(unittest.TestCase):
    """Tests that arccos results stay in the principal range."""

    def test_results_in_principal_range(self):
        test_values = [
            -1.0,
            -0.9999,
            -0.75,
            -0.5,
            0.0,
            0.25,
            0.5,
            0.75,
            0.9999,
            1.0,
        ]

        for value in test_values:
            result = calculate_arccos(value)
            self.assertGreaterEqual(result, 0.0)
            self.assertLessEqual(result, PI)


if __name__ == "__main__":
    unittest.main()
