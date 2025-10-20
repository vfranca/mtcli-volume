from click.testing import CliRunner
import pytest

from mtcli_volume.commands.volume_cli import volume
from mtcli_volume.controllers.volume_controller import calcular_volume_profile
from mtcli_volume.models import volume_model


@pytest.fixture
def mock_rates():
    """Simula dados OHLCV com volumes diferentes."""
    return [
        {"close": 100.0, "tick_volume": 10, "real_volume": 20},
        {"close": 100.5, "tick_volume": 15, "real_volume": 25},
        {"close": 101.0, "tick_volume": 30, "real_volume": 40},
        {"close": 101.0, "tick_volume": 5, "real_volume": 10},
        {"close": 102.0, "tick_volume": 40, "real_volume": 50},
    ]


def test_calcular_profile_tick(mock_rates, monkeypatch):
    monkeypatch.setattr(volume_model, "obter_rates", lambda s, p, b: mock_rates)
    profile, stats = calcular_volume_profile("WINZ25", "M1", 100, 1.0, "tick")

    # Verifica soma de volumes por faixa
    assert isinstance(profile, dict)
    assert sum(profile.values()) == sum(r["tick_volume"] for r in mock_rates)

    # Estatísticas devem existir
    assert "poc" in stats
    assert stats["poc"] is not None
    assert isinstance(stats["hvns"], list)


def test_calcular_profile_real(mock_rates, monkeypatch):
    monkeypatch.setattr(volume_model, "obter_rates", lambda s, p, b: mock_rates)
    profile, stats = calcular_volume_profile("WINZ25", "M1", 100, 1.0, "real")

    assert sum(profile.values()) == sum(r["real_volume"] for r in mock_rates)
    assert stats["poc"] in profile


def test_volume_invalido(monkeypatch):
    with pytest.raises(ValueError):
        calcular_volume_profile("WINZ25", "M1", 100, 1.0, "xyz")


def test_obter_rates_invalido(monkeypatch):
    monkeypatch.setattr(volume_model, "obter_rates", lambda s, p, b: None)
    profile, stats = calcular_volume_profile("WINZ25", "M1", 100, 1.0, "tick")
    assert profile == {}


def test_cli_execucao(monkeypatch, mock_rates):
    monkeypatch.setattr(volume_model, "obter_rates", lambda s, p, b: mock_rates)

    runner = CliRunner()
    result = runner.invoke(
        volume,
        ["-s", "WINZ25", "-p", "M1", "-b", "50", "-e", "1.0", "-v", "tick", "-sh"],
    )
    assert result.exit_code == 0
    assert "Volume Profile" in result.output
