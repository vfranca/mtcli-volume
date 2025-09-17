import os
import csv
from datetime import datetime
from click.testing import CliRunner
from mtcli_volume.plugin import volume


def test_exporta_csv_tem_saida_valida(monkeypatch, tmp_path):
    # Mocka dados simulados de candles
    dados_falsos = [{"close": 117000 + i * 100, "tick_volume": 1000} for i in range(5)]

    monkeypatch.setattr(
        "mtcli_volume.plugin.mt5.copy_rates_from_pos", lambda *a, **kw: dados_falsos
    )
    monkeypatch.setattr("mtcli_volume.plugin.conectar", lambda: None)
    monkeypatch.setattr("mtcli_volume.plugin.shutdown", lambda: None)

    # Mocka datetime.now()
    class FakeDatetime(datetime):
        @classmethod
        def now(cls):
            return cls(2025, 9, 17, 10, 30)

    monkeypatch.setattr("mtcli_volume.plugin.datetime", FakeDatetime)

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(volume, ["--symbol", "TESTE", "--exporta-csv"])

        assert result.exit_code == 0
        assert "Exportado para" in result.output

        # Extrai nome do arquivo exportado
        for line in result.output.splitlines():
            if "Exportado para" in line:
                caminho_csv = line.split("Exportado para")[1].strip()
                break

        assert os.path.exists(caminho_csv)

        with open(caminho_csv, encoding="utf-8") as f:
            reader = csv.reader(f)
            linhas = list(reader)

        assert linhas[0] == ["Faixa de Preço", "Volume"]
        assert len(linhas) > 1
