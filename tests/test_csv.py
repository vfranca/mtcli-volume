from unittest.mock import mock_open, patch
import builtins
import csv


def test_exportacao_csv():
    dados = [
        {"close": 100, "tick_volume": 50},
        {"close": 100, "tick_volume": 30},
    ]
    profile, _, _, _ = calcular_volume_profile(dados, step=1)

    m = mock_open()
    with patch.object(builtins, "open", m):
        writer = csv.writer(m())
        writer.writerow(["Faixa de Preço", "Volume"])
        writer.writerows(profile)

    m().write.assert_called()  # Verifica se algo foi escrito
