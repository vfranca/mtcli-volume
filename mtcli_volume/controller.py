"""
Controller do plugin mtcli-volume.
"""

from datetime import datetime, timedelta, timezone
import zoneinfo
import numpy as np

from mtcli.logger import setup_logger
from .model import calcular_profile, calcular_estatisticas, obter_rates

log = setup_logger()


def resolver_inicio_ancorado(anchor: str, tz):
    """
    Resolve a data-base da ancoragem (sem forçar horário fixo).
    """
    agora = datetime.now(tz)

    if anchor == "day":
        return agora.replace(hour=0, minute=0, second=0, microsecond=0)

    if anchor == "week":
        inicio_semana = agora - timedelta(days=agora.weekday())
        return inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)

    if anchor == "month":
        return agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    return None


def calcular_volume_profile(
    symbol,
    period,
    limit,
    step,
    volume,
    inicio=None,
    fim=None,
    anchor="day",
    verbose=False,
    timezone_str="America/Sao_Paulo",
    criterio_hvn="media",
):
    volume = volume.lower().strip()
    if volume not in ("tick", "real"):
        raise ValueError("Tipo de volume inválido. Use 'tick' ou 'real'.")

    try:
        fuso = zoneinfo.ZoneInfo(timezone_str)
    except Exception:
        fuso = timezone(timedelta(hours=-3))

    # Resolve ancoragem se --inicio não foi informado
    if inicio is None:
        inicio = resolver_inicio_ancorado(anchor, fuso)

    rates = None
    tentativas = 0
    max_tentativas = 7

    while tentativas < max_tentativas:
        rates = obter_rates(symbol, period, limit, inicio, fim)
        if rates is not None and isinstance(rates, np.ndarray) and len(rates) > 0:
            break

        inicio -= timedelta(days=1)
        tentativas += 1

    if rates is None or len(rates) == 0:
        log.error("Nenhum dado retornado após fallback de ancoragem.")
        return {}, {}, {}

    profile = calcular_profile(rates, step, volume)
    stats = calcular_estatisticas(profile, criterio=criterio_hvn)

    try:
        inicio_real = datetime.utcfromtimestamp(
            float(rates[0]["time"])
        ).astimezone(fuso)

        fim_real = datetime.utcfromtimestamp(
            float(rates[-1]["time"])
        ).astimezone(fuso)

    except Exception:
        inicio_real = fim_real = "?"

    info = {
        "symbol": symbol,
        "period": period,
        "candles": len(rates),
        "inicio": str(inicio_real),
        "fim": str(fim_real),
        "timezone": timezone_str,
        "anchor": anchor,
        "fallback_days": tentativas,
    }

    return profile, stats, info
