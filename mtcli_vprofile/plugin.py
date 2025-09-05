import click
import MetaTrader5 as mt5
import csv
from mtcli.conecta import conectar, shutdown
from mtcli.logger import setup_logger
from . import conf
from .volume_profile import calcular_volume_profile

log = setup_logger()

@click.command()
@click.version_option(package_name="mtcli-vprofile")
@click.option("--symbol", "-s", default="WINV25", help="Símbolo do ativo.")
@click.option("--periods", "-p", default=500, help="Número de candles.")
@click.option("--step", "-e", default=5, help="Tamanho do agrupamento de preços.")
@click.option("--csv", is_flag=True, help="Exportar para CSV.")
def volume(symbol, periods, step, csv):
    """Exibe o Volume Profile agrupando volumes por faixa de preço com POC e Área de Valor."""
    conectar()
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, periods)

    if rates is None or len(rates) == 0:
        click.echo("❌ Não foi possível obter os dados.")
        shutdown()
        return

    dados_ordenados, poc, av_min, av_max = calcular_volume_profile(rates, step)

    if csv:
        nome_arquivo = f"volume_profile_{symbol}.csv"
        with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Faixa de Preço", "Volume", "POC", "Área de Valor"])
            for preco, vol in dados_ordenados:
                is_poc = "✅" if preco == poc else ""
                in_value_area = "✅" if av_min <= preco <= av_max else ""
                writer.writerow([preco, vol, is_poc, in_value_area])
        click.echo(f"✅ Exportado para {nome_arquivo}")
        log.info(f"Exportado para {nome_arquivo}")
    else:
        click.echo(f"\nVolume Profile {symbol}\n")
        max_vol = max(v for _, v in dados_ordenados)
        for preco, vol in dados_ordenados:
            barra = "█" * (vol // max(1, max_vol // 50))
            label = ""
            if preco == poc:
                label += " <-- POC"
            elif av_min <= preco <= av_max:
                label += " [Área de Valor]"
            click.echo(f"{preco:>8.{conf.digitos}f} | {vol:>6} {barra}{label}")

    shutdown()
