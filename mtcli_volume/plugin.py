from mtcli_volume.commands.volume import volume


def register(cli):
    cli.add_command(volume)
