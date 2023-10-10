""" Module for storing constants for electric vehicle modeling."""

# third-party imports
import numpy as np

# pylint: disable=missing-function-docstring
# pylint: disable=invalid-name


def evolve_default_charge_func(x: float) -> float:
    return np.piecewise(
        x,
        [x == 0, (x > 0) & (x <= 25), (x > 25) & (x <= 80), x > 80],
        [
            0.24,
            lambda a: 0.24 + a * 0.76 / 25,
            lambda a: 1 - (0.2 / 55) * (a - 25),
            lambda a: 0.8 - (0.8 / 20) * (a - 80),
        ],
    )
