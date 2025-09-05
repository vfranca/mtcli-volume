import pytest
from mtcli_vprofile.volume_profile import calcular_volume_profile

@pytest.fixture
def dados_basicos():
    return [
        {"close": 100, "tick_volume": 10},
        {"close": 101, "tick_volume": 20},
        {"close": 102, "tick_volume": 30},
        {"close": 103, "tick_volume": 40},
        {"close": 104, "tick_volume": 50},
        {"close": 105, "tick_volume": 60},
    ]

def test_volume_profile_basico(dados_basicos):
    profile, poc, av_min, av_max = calcular_volume_profile(dados_basicos, step=1)
    assert poc in dict(profile)
    assert av_min <= poc <= av_max

def test_volume_profile_com_step_maior(dados_basicos):
    profile, poc, av_min, av_max = calcular_volume_profile(dados_basicos, step=5)
    assert len(profile) < len(dados_basicos)
    assert poc in dict(profile)

def test_volume_profile_volumes_iguais():
    dados = [{"close": p, "tick_volume": 100} for p in range(100, 106)]
    profile, poc, av_min, av_max = calcular_volume_profile(dados, step=1)
    assert poc in dict(profile)
    assert av_max - av_min <= 3  # Valor típico para 70% da área de valor


def test_volume_profile_com_dados_vazios():
    dados = []
    profile, poc, av_min, av_max = calcular_volume_profile(dados, step=1)
    assert profile == []
    assert poc is None
    assert av_min is None
    assert av_max is None

