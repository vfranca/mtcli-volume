from collections import defaultdict

def calcular_volume_profile(rates, step):
    profile = defaultdict(int)
    for r in rates:
        preco = r["close"]
        faixa = round(preco / step) * step
        profile[faixa] += r["tick_volume"]

    dados_ordenados = sorted(profile.items())
    total_volume = sum(v for _, v in dados_ordenados)
    poc = max(dados_ordenados, key=lambda x: x[1])[0]

    # Calcular Área de Valor (70%)
    sorted_by_vol = sorted(dados_ordenados, key=lambda x: x[1], reverse=True)
    acumulado = 0
    area_valor = []
    for faixa, vol in sorted_by_vol:
        acumulado += vol
        area_valor.append(faixa)
        if acumulado >= total_volume * 0.7:
            break
    area_valor_min = min(area_valor)
    area_valor_max = max(area_valor)

    return dados_ordenados, poc, area_valor_min, area_valor_max
