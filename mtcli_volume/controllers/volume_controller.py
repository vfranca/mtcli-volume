from mtcli_volume.models.volume_model import (
    calcular_volume_profile,
    calcular_estatisticas,
)


def processar_volume(rates, step, volume="tick"):
    profile = calcular_volume_profile(rates, step, volume)
    estatisticas = calcular_estatisticas(profile)
    return profile, estatisticas
