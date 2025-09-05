import pytest
from mtcli_vprofile.volume_profile import calcular_volume_profile


@pytest.fixture
def dados_mock():
    # Simula candles com preços e volumes
    return [
        {"close": 100, "tick_volume": 10},
        {"close": 101, "tick_volume": 20},
        {"close": 102, "tick_volume": 30},
        {"close": 103, "tick_volume": 40},
        {"close": 104, "tick_volume": 50},
        {"close": 105, "tick_volume": 60},
    ]


def test_calcular_volume_profile(dados_mock):
    step = 1
    profile, poc, av_min, av_max = calcular_volume_profile(dados_mock, step)

    assert isinstance(profile, list)
    assert all(isinstance(p, tuple) for p in profile)
    assert isinstance(poc, (int, float))
    assert isinstance(av_min, (int, float))
    assert isinstance(av_max, (int, float))
    assert av_min <= poc <= av_max
    assert sum(v for _, v in profile) == sum(d["tick_volume"] for d in dados_mock)
