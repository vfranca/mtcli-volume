"""Plugin para exibir o Volume Profile do ativo."""

import click
import MetaTrader5 as mt5
import csv
from collections import defaultdict
from mtcli.conecta import conectar, shutdown
from mtcli.logger import setup_logger
from . import conf

log = setup_logger()

@click.command()
@click.version_option(package_name="mtcli-vprofile")
@click.option("--symbol", "-s", default="WINV25", help="Símbolo do ativo.")
@click.option("--periods", "-p", default=500, help="Número de candles.")
@click.option("--step", "-e", default=5, help="Tamanho do agrupamento de preços.")
@click.option("--csv", is_flag=True, help="Exportar para CSV.")
def volume(symbol, periods, step, csv):
    """Exibe o Volume Profile agrupando volumes por faixa de preço."""
    conectar()
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, periods)

    if rates is None or len(rates) == 0:
        click.echo("❌ Não foi possível obter os dados.")
        shutdown()
        return

    profile = defaultdict(int)

    for r in rates:
        preco = r["close"]
        faixa = round(preco / step) * step
        profile[faixa] += r["tick_volume"]

    dados_ordenados = sorted(profile.items())

    if csv:
        nome_arquivo = f"volume_profile_{symbol}.csv"
        with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Faixa de Preço", "Volume"])
            writer.writerows(dados_ordenados)
        click.echo(f"✅ Exportado para {nome_arquivo}")
        log.info(f"Exportado para {nome_arquivo}")
    else:
        click.echo(f"\nVolume Profile {symbol}\n")
        max_vol = max(profile.values())
        for preco, vol in dados_ordenados:
            barra = "█" * (vol // max(1, max_vol // 50))
            click.echo(f"{preco:>8.{conf.digitos}f} | {vol:>6} {barra}")

    shutdown()

