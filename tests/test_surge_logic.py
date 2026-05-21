def test_basic_math():
    demand = 10
    supply = 5
    alpha = 2.0
    ratio = demand / supply
    smoothed = 0.7 * ratio + 0.3 * alpha
    assert round(smoothed, 2) == 2.0
