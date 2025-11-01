from datetime import datetime, timedelta, timezone

import numpy as np

from mtcli.logger import setup_logger
from mtcli_volume.models.volume_model import (
    calcular_estatisticas,
    calcular_profile,
    obter_rates,
)

log = setup_logger()


def calcular_volume_profile(
    symbol, period, bars, step, volume, data_inicio=None, data_fim=None, verbose=False
):
    """Controla o fluxo de cálculo do volume profile, com suporte a exibição detalhada (verbose)."""
    volume = volume.lower().strip()
    if volume not in ["tick", "real"]:
        log.error(f"Tipo de volume inválido: {volume}. Use 'tick' ou 'real'.")
        raise ValueError(f"Tipo de volume inválido: {volume}. Use 'tick' ou 'real'.")

    rates = obter_rates(symbol, period, bars, data_inicio, data_fim)

    # ✅ Checagem segura para arrays NumPy
    if rates is None or len(rates) == 0:
        log.error("Falha ao obter dados de preços para cálculo do volume profile.")
        return {}, {}, {}

    profile = calcular_profile(rates, step, volume)
    stats = calcular_estatisticas(profile)

    # 🔍 Captura de informações de contexto para modo verboso
    info = {}
    if isinstance(rates, np.ndarray) and len(rates) > 0:
        primeiro = rates[0]
        ultimo = rates[-1]
        if "time" in rates.dtype.names:
            try:
                # Converte timestamps UTC do MT5 → horário local de Brasília (UTC−3)
                fuso_brasilia = timezone(timedelta(hours=-3))

                inicio_real = (
                    datetime.utcfromtimestamp(float(primeiro["time"]))
                    .astimezone(fuso_brasilia)
                    .strftime("%Y-%m-%d %H:%M:%S")
                )
                fim_real = (
                    datetime.utcfromtimestamp(float(ultimo["time"]))
                    .astimezone(fuso_brasilia)
                    .strftime("%Y-%m-%d %H:%M:%S")
                )
            except Exception:
                inicio_real = fim_real = "?"
        else:
            inicio_real = fim_real = "?"

        info = {
            "symbol": symbol,
            "period": period,
            "candles": len(rates),
            "inicio": inicio_real,
            "fim": fim_real,
        }

    return profile, stats, info
