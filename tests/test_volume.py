import pytest
from mtcli_volume.volume import calcular_volume_profile, calcular_estatisticas

# Mock simples de candles M1
mock_rates = [
    {"close": 117000, "tick_volume": 100},
    {"close": 117050, "tick_volume": 150},
    {"close": 117100, "tick_volume": 300},
    {"close": 117000, "tick_volume": 50},
    {"close": 117200, "tick_volume": 500},
]


def test_calcular_volume_profile():
    step = 100
    profile = calcular_volume_profile(mock_rates, step)

    assert isinstance(profile, dict)
    assert round(117000 / step) * step in profile
    total_volume = sum(profile.values())
    assert total_volume == 1100


def test_calcular_estatisticas():
    profile = {
        117000: 150,
        117100: 300,
        117200: 500,
        117300: 150,
    }

    stats = calcular_estatisticas(profile)

    assert "poc" in stats
    assert "area_valor" in stats
    assert "hvns" in stats
    assert "lvns" in stats

    assert stats["poc"] == 117200
    assert isinstance(stats["area_valor"], tuple)
    assert stats["area_valor"][0] <= stats["poc"] <= stats["area_valor"][1]


def test_volume_profile_vazio():
    profile = calcular_volume_profile([], step=100)
    assert profile == {}


def test_estatisticas_com_perfil_vazio():
    profile = {}
    stats = calcular_estatisticas(profile)
    assert stats["poc"] is None
    assert stats["area_valor"] == (None, None)
    assert stats["hvns"] == []
    assert stats["lvns"] == []


def test_estatisticas_volume_igual():
    profile = {
        117000: 100,
        117100: 100,
        117200: 100,
    }
    stats = calcular_estatisticas(profile)
    assert stats["poc"] in profile
    assert len(stats["hvns"]) == 0
    assert len(stats["lvns"]) == 0
    assert stats["area_valor"][0] <= stats["poc"] <= stats["area_valor"][1]


def test_estatisticas_sensibilidade_hvns_lvns():
    profile = {
        117000: 50,  # LVN (menor que 50% da média)
        117100: 500,  # HVN (maior que 150% da média)
        117200: 100,  # dentro do intervalo
    }
    stats = calcular_estatisticas(profile)
    assert 117100 in stats["hvns"]
    assert 117000 in stats["lvns"]
