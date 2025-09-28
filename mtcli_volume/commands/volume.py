import click
import MetaTrader5 as mt5
from mtcli.conecta import conectar, shutdown
from mtcli.logger import setup_logger
from mtcli_volume.controllers.volume_controller import processar_volume
from mtcli_volume.views.volume_view import exibir_volume
from mtcli_volume.conf import (
    SYMBOL,
    BARS,
    STEP,
    PERIOD,
    VOLUME,
)

log = setup_logger()


@click.command("volume")
@click.option("--symbol", "-s", default=SYMBOL, help="Símbolo do ativo.")
@click.option("--bars", "-b", default=BARS, help="Número de candles.")
@click.option(
    "--step", "-st", default=STEP, type=float, help="Tamanho da faixa de preço."
)
@click.option(
    "--volume",
    "-v",
    default=VOLUME,
    type=click.Choice(["tick", "real"]),
    help="Tipo de volume.",
)
@click.option(
    "--period", "-p", "timeframe", default=PERIOD, help="Timeframe (ex: M1, H1, D1)."
)
def volume(symbol, bars, step, volume, timeframe):
    """Exibe volume profile e estatísticas"""
    conectar()

    tf = getattr(mt5, f"TIMEFRAME_{timeframe.upper()}", None)
    if tf is None:
        click.echo(f"Timeframe inválido: {timeframe}")
        shutdown()
        return

    if not mt5.symbol_select(symbol, True):
        click.echo(f"Erro ao selecionar símbolo {symbol}")
        shutdown()
        return

    rates = mt5.copy_rates_from_pos(symbol, tf, 0, bars)
    if rates is None or len(rates) == 0:
        click.echo("Falha ao obter dados de candles")
        shutdown()
        return

    profile, estatisticas = processar_volume(rates, step, volume)
    exibir_volume(profile, estatisticas)

    shutdown()
