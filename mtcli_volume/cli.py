from datetime import datetime

import click

from .conf import (
    FIM,
    INICIO,
    LIMIT,
    PERIOD,
    RANGE,
    SYMBOL,
    TIMEZONE,
    VOLUME,
)
from .controller import calcular_volume_profile
from .view import exibir_volume_profile


@click.command(
    help=(
        "Exibe o Volume Profile distribuindo o volume dos candles "
        "uniformemente entre as faixas de preço entre LOW e HIGH."
    )
)
@click.version_option(package_name="mtcli-volume")
@click.option(
    "--symbol",
    "-s",
    default=SYMBOL,
    show_default=True,
    help="Símbolo do ativo.",
)
@click.option(
    "--period",
    "-p",
    default=PERIOD,
    show_default=True,
    help="Timeframe utilizado no cálculo.",
)
@click.option(
    "--limit",
    "-l",
    default=LIMIT,
    show_default=True,
    help="Quantidade de candles usados no cálculo.",
)
@click.option(
    "--range",
    "-r",
    type=float,
    default=RANGE,
    show_default=True,
    help="Tamanho da faixa de preço do Volume Profile.",
)
@click.option(
    "--volume",
    "-v",
    type=click.Choice(["tick", "real"], case_sensitive=False),
    default=VOLUME,
    show_default=True,
    help="Tipo de volume utilizado no cálculo.",
)
@click.option(
    "--inicio",
    "-i",
    default=INICIO,
    show_default=True,
    help="Data/hora inicial (YYYY-MM-DD HH:MM).",
)
@click.option(
    "--fim",
    "-f",
    default=FIM,
    show_default=True,
    help="Data/hora final (YYYY-MM-DD HH:MM).",
)
@click.option(
    "--timezone",
    "-tz",
    type=str,
    default=TIMEZONE,
    show_default=True,
    help="Fuso horário para exibição das datas.",
)
@click.option(
    "--hvn-criterio",
    type=click.Choice(["media", "percentil"], case_sensitive=False),
    default="percentil",
    show_default=True,
    help="Critério para identificação de HVNs e LVNs.",
)
@click.option(
    "--verbose",
    "-vv",
    is_flag=True,
    help="Exibe informações detalhadas da análise.",
)
def volume(
    symbol,
    period,
    limit,
    range,
    volume,
    inicio,
    fim,
    timezone,
    hvn_criterio,
    verbose,
):
    """
    Exibe o Volume Profile agrupando volumes por faixa de preço.

    O volume de cada candle é distribuído igualmente entre todas
    as faixas de preço tocadas entre o LOW e o HIGH do candle,
    resultando em uma representação mais precisa da distribuição
    de volume.
    """
    inicio_dt = (
        datetime.strptime(inicio, "%Y-%m-%d %H:%M") if inicio else None
    )
    fim_dt = datetime.strptime(fim, "%Y-%m-%d %H:%M") if fim else None

    profile, stats, info = calcular_volume_profile(
        symbol=symbol,
        period=period,
        limit=limit,
        step=range,
        volume=volume,
        inicio=inicio_dt,
        fim=fim_dt,
        verbose=verbose,
        timezone_str=timezone,
        criterio_hvn=hvn_criterio.lower(),
    )

    exibir_volume_profile(
        profile=profile,
        stats=stats,
        symbol=symbol,
        info=info,
        verbose=verbose,
    )
