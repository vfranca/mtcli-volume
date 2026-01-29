from datetime import datetime, timedelta, timezone
import zoneinfo
import numpy as np

from mtcli.logger import setup_logger
from .model import (
    calcular_profile,
    calcular_estatisticas,
    obter_rates,
)

log = setup_logger()


def calcular_volume_profile(
    symbol,
    period,
    limit,
    step,
    volume,
    inicio=None,
    fim=None,
    verbose=False,
    timezone_str="America/Sao_Paulo",
    criterio_hvn="media",
):
    """
    Controla o fluxo de cálculo do Volume Profile.

    - Obtém candles via MT5
    - Calcula Volume Profile por faixa High–Low
    - Calcula estatísticas (POC, VA, HVN, LVN)
    """

    volume = volume.lower().strip()
    if volume not in ("tick", "real"):
        raise ValueError("Tipo de volume inválido. Use 'tick' ou 'real'.")

    rates = obter_rates(symbol, period, limit, inicio, fim)

    # ✅ Correção crítica: validação correta para numpy.ndarray
    if rates is None or not isinstance(rates, np.ndarray) or len(rates) == 0:
        log.error("Nenhum dado retornado para o cálculo do Volume Profile.")
        return {}, {}, {}

    profile = calcular_profile(
        rates=rates,
        step=step,
        volume_tipo=volume,
    )

    stats = calcular_estatisticas(
        profile=profile,
        criterio=criterio_hvn,
    )

    info = {}
    try:
        fuso = zoneinfo.ZoneInfo(timezone_str)
    except Exception:
        log.warning(
            f"Fuso horário '{timezone_str}' inválido. Usando UTC−3 (Brasília)."
        )
        fuso = timezone(timedelta(hours=-3))

    try:
        inicio_real = (
            datetime.utcfromtimestamp(float(rates[0]["time"]))
            .astimezone(fuso)
            .strftime("%Y-%m-%d %H:%M:%S")
        )
        fim_real = (
            datetime.utcfromtimestamp(float(rates[-1]["time"]))
            .astimezone(fuso)
            .strftime("%Y-%m-%d %H:%M:%S")
        )
    except Exception as e:
        log.error(f"Erro ao converter datas: {e}")
        inicio_real = fim_real = "?"

    info = {
        "symbol": symbol,
        "period": period,
        "candles": len(rates),
        "inicio": inicio_real,
        "fim": fim_real,
        "timezone": timezone_str,
    }

    return profile, stats, info
