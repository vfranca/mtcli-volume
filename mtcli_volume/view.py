import click
from .conf import DIGITOS as D


def formatar_numero(valor: float) -> str:
    return f"{valor:,.{D}f}".replace(",", ".")


def exibir_volume_profile(profile, stats, symbol, info=None, verbose=False):
    if not profile:
        click.echo("Nenhum dado disponível.")
        return

    max_vol = max(profile.values())

    if verbose and info:
        click.echo("\nInformações da Análise")
        for k, v in info.items():
            click.echo(f"{k.capitalize():15}: {v}")

    click.echo(f"\nVolume Profile — {symbol}\n")
    click.echo("Preço           | Volume        | Distribuição")
    click.echo("-" * 55)

    for preco in sorted(profile.keys(), reverse=True):
        vol = profile[preco]
        perc = vol / max_vol * 100
        click.echo(
            f"{preco:>15.{D}f} | {formatar_numero(vol):>12} | {perc:5.0f}%"
        )

    # click.echo("\nEstatísticas")
    click.echo(f"POC             {stats['poc']:.{D}f}")
    click.echo(
        f"VA    {stats['area_valor'][0]:.{D}f} → {stats['area_valor'][1]:.{D}f}"
    )
    click.echo(
        f"HVNs            {', '.join(f'{x:.{D}f}' for x in stats['hvns']) or 'Nenhum'}"
    )
    click.echo(
        f"LVNs            {', '.join(f'{x:.{D}f}' for x in stats['lvns']) or 'Nenhum'}"
    )
