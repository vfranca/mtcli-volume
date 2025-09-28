from collections import defaultdict
from ..conf import DIGITOS


def calcular_volume_profile(rates, step, volume="tick"):
    profile = defaultdict(int)
    for r in rates:
        preco = r["close"]
        faixa = round(round(preco / step) * step, DIGITOS)
        profile[faixa] += r["tick_volume"] if volume == "tick" else r["real_volume"]
    return dict(profile)


def calcular_estatisticas(profile):
    if not profile:
        return {
            "poc": None,
            "area_valor": (None, None),
            "hvns": [],
            "lvns": [],
        }

    total_volume = sum(profile.values())
    dados = sorted(profile.items(), key=lambda x: x[0])
    volumes_ordenados = sorted(profile.items(), key=lambda x: x[1], reverse=True)

    poc = volumes_ordenados[0][0]

    acumulado = 0
    area_valor = []
    for faixa, vol in volumes_ordenados:
        acumulado += vol
        area_valor.append(faixa)
        if acumulado / total_volume >= 0.7:
            break

    media = total_volume / len(profile)
    hvns = [faixa for faixa, vol in profile.items() if vol >= media * 1.5]
    lvns = [faixa for faixa, vol in profile.items() if vol <= media * 0.5]

    return {
        "poc": poc,
        "area_valor": (min(area_valor), max(area_valor)),
        "hvns": sorted(hvns),
        "lvns": sorted(lvns),
    }
