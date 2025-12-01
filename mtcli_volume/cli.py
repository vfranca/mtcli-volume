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
    help="Exibe o Volume Profile, agrupando volumes por faixa de preço no histórico recente."
)
@click.version_option(package_name="mtcli-volume")
@click.option(
    "--symbol", "-s", default=SYMBOL, show_default=True, help="Símbolo do ativo."
)
@click.option(
    "--period",
    "-p",
    default=PERIOD,
    show_default=True,
    help="Timeframe usado no calculo.",
)
@click.option(
    "--limit",
    "-l",
    default=LIMIT,
    show_default=True,
    help="Quantidade de timeframes usados no calculo.",
)
@click.option(
    "--range",
    "-r",
    type=float,
    default=RANGE,
    show_default=True,
    help="Tamanho da faixa da distribuicao.",
)
@click.option(
    "--volume",
    "-v",
    type=click.Choice(["tick", "real"], case_sensitive=False),
    default=VOLUME,
    show_default=True,
    help="Tipo do volume .",
)
@click.option(
    "--format",
    "-fo",
    type=click.Choice(["none", "k", "m", "auto"], case_sensitive=False),
    default="k",
    show_default=True,
    help="Formatacao do volume.",
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
    "--verbose",
    "-vv",
    is_flag=True,
    help="Mostra informações detalhadas sobre a análise.",
)
@click.option(
    "--timezone",
    "-tz",
    type=str,
    default=TIMEZONE,
    show_default=True,
    help="Fuso horário para exibição das datas (ex: 'UTC', 'America/Sao_Paulo').",
)
def volume(
    symbol, period, limit, range, volume, format, inicio, fim, timezone, verbose
):
    """Exibe o Volume Profile agrupando volumes por faixa de preço."""
    inicio = datetime.strptime(inicio, "%Y-%m-%d %H:%M") if inicio else None
    fim = datetime.strptime(fim, "%Y-%m-%d %H:%M") if fim else None

    profile, stats, info = calcular_volume_profile(
        symbol, period, limit, range, volume, inicio, fim, verbose, timezone
    )
    exibir_volume_profile(profile, stats, symbol, info, verbose, format)
