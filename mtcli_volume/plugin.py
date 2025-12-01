from .cli import volume


def register(cli):
    cli.add_command(volume, name="vp")
