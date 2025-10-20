from click.testing import CliRunner

from mtcli_volume.plugin import volume


def test_volume_log_erro_quando_rates_vazio(monkeypatch, caplog):
    # Simula rates vazios retornados pelo MetaTrader5
    monkeypatch.setattr(
        "mtcli_volume.plugin.mt5.copy_rates_from_pos", lambda *a, **kw: []
    )
    monkeypatch.setattr("mtcli_volume.plugin.conectar", lambda: None)
    monkeypatch.setattr("mtcli_volume.plugin.shutdown", lambda: None)

    runner = CliRunner()
    result = runner.invoke(
        volume, ["--symbol", "TESTE", "--periods", "10", "--step", "100"]
    )

    assert result.exit_code == 0
    assert "Não foi possível obter os dados" in result.output
    # assert any("Não foi possível obter os dados" in m for m in caplog.messages)
