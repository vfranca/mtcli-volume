import click


def exibir_volume(profile, estatisticas):
    click.echo("📊 Volume Profile:")
    for faixa, vol in sorted(profile.items()):
        click.echo(f"{faixa:.2f}: {vol}")

    click.echo("\n📈 Estatísticas:")
    click.echo(f"POC: {estatisticas['poc']}")
    click.echo(f"Área de Valor: {estatisticas['area_valor']}")
    click.echo(f"HVNs: {estatisticas['hvns']}")
    click.echo(f"LVNs: {estatisticas['lvns']}")
