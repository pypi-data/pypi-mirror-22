import numpy as np
import pytest
from sklearn.exceptions import FitFailedWarning

from sparsereg.sindy import *

test_settings = (
    dict(knob=0.5, copy_x=True, normalize=True, fit_intercept=True),
    dict(knob=0.1, copy_x=True, normalize=False, fit_intercept=True),
    dict(knob=0.1, l1=0, copy_x=True, normalize=True, fit_intercept=True),
)


@pytest.mark.parametrize("kw", test_settings)
def test_sindy_normalize(data, kw):
    x, y = data
    s = SINDy(**kw).fit(x, y)

    np.testing.assert_allclose(s.coef_, np.array([0, 2]), atol=1e-7)
    np.testing.assert_allclose(s.predict(x), y)


def test_sindy_raise(data):
    x, y = data
    with pytest.raises(FitFailedWarning):
        s = SINDy(knob=10000).fit(x, y)
