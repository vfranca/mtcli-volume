from click.testing import CliRunner
import pytest

import mtcli_volume.plugin as plugin

# Simula dados de candles M1
mock_rates = [
    {"close": 1000 + i, "real_volume": 10 + i, "tick_volume": 20 + i}
    for i in range(100)
]


@pytest.fixture
def runner():
    return CliRunner()


def test_volume_profile_saida_terminal(monkeypatch, runner):
    """Teste básico da execução do comando volume com dados mockados."""

    # Mock funções externas
    monkeypatch.setattr("mtcli_volume.plugin.conectar", lambda: None)
    monkeypatch.setattr("mtcli_volume.plugin.shutdown", lambda: None)
    monkeypatch.setattr(
        "mtcli_volume.plugin.mt5.copy_rates_from_pos", lambda *a, **kw: mock_rates
    )
    monkeypatch.setattr(
        "mtcli_volume.plugin.calcular_volume_profile",
        lambda rates, step, tipo: {1000: 300, 1010: 200},
    )
    monkeypatch.setattr(
        "mtcli_volume.plugin.calcular_estatisticas",
        lambda p: {
            "poc": 1000.0,
            "area_valor": (995.0, 1015.0),
            "hvns": [1000],
            "lvns": [1010],
        },
    )
    result = runner.invoke(
        plugin.volume, ["--symbol", "TESTE", "--periods", "100", "--step", "10"]
    )
    assert result.exit_code == 0
    assert "Volume Profile TESTE" in result.output
    assert "POC" in result.output
    assert "Área de Valor" in result.output


def test_volume_profile_sem_dados(monkeypatch, runner):
    """Teste para quando não há dados retornados do MT5."""

    monkeypatch.setattr("mtcli_volume.plugin.conectar", lambda: None)
    monkeypatch.setattr("mtcli_volume.plugin.shutdown", lambda: None)
    monkeypatch.setattr(
        "mtcli_volume.plugin.mt5.copy_rates_from_pos", lambda *a, **kw: []
    )

    result = runner.invoke(plugin.volume, ["--symbol", "TESTE"])
    assert result.exit_code == 0
    assert "Não foi possível obter os dados" in result.output


def test_volume_tipo_invalido(monkeypatch, runner):
    """Teste com tipo de volume inválido."""

    monkeypatch.setattr("mtcli_volume.plugin.conectar", lambda: None)
    monkeypatch.setattr("mtcli_volume.plugin.shutdown", lambda: None)

    result = runner.invoke(plugin.volume, ["--volume", "invalido"])
    assert result.exit_code == 0
    assert "Tipo de volume inválido" in result.output
