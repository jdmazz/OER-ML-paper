"""dJ/dV curve model.

Shared by ``dJdVpreprocess.ipynb`` (fitting) and ``ml_djdv.ipynb``
(reconstruction), so the sigmoid-plus-Gaussian form lives in one place.
"""

import numpy as np


def logistic(V, k, V0):
    """Sigmoid describing the onset of OER kinetics."""
    return 1.0 / (1.0 + np.exp(-k * (V - V0)))


def hump(V, u, s):
    """Gaussian hump: the secondary dJ/dV feature."""
    return np.exp(-((V - u) ** 2) / (2.0 * s ** 2))


def djdv_model(V, p):
    """Full dJ/dV model: sigmoid plus Gaussian hump.

    Parameters
    ----------
    V : array-like
        Voltage grid.
    p : array-like
        Parameter vector ``[k, V0, u1, s1, A1, A2]``.
    """
    k, V0, u1, s1, A1, A2 = p
    return A1 * logistic(V, k, V0) + A2 * hump(V, u1, s1)


def residuals(p, V, y):
    """Residual vector for least-squares fitting."""
    return djdv_model(V, p) - y
