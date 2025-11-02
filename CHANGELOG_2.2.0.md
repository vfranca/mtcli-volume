# Relatório de Revisão — mtcli-volume v2.2.0

**Data da revisão:** 1º de novembro de 2025  
**Revisor:** ChatGPT (GPT-5)  
**Autor:** Valmir França  
**Módulo:** `mtcli-volume`  
**Arquitetura:** MVC (Model–View–Controller)  
**Compatibilidade:** Python ≥ 3.9

---

## 🆕 Principais mudanças da versão 2.2.0

| Categoria | Descrição |
|------------|------------|
|  **Timezone corrigido** | Conversão de timestamps UTC para horário local (ex.: `America/Sao_Paulo`) utilizando `zoneinfo`. Elimina o atraso de 3 horas relatado nas versões anteriores. |
| **Modelo robusto de dados** | `volume_model.py` agora aceita múltiplos formatos de candles (`dict`, `numpy.void`, objetos, tuplas/listas`). Isso amplia a compatibilidade com corretoras e simuladores. |
| **Cálculo aprimorado de estatísticas** | Mantém POC, Área de Valor (70%), HVNs e LVNs, agora com melhor precisão e legibilidade. |
| **Acessibilidade aprimorada** | Saída no terminal mais organizada e legível por leitores de tela (NVDA, JAWS), com tabelas textuais simples e modo `--verbose` opcional. |
| **Logging mais detalhado** | Mensagens de erro e debug mais específicas em todas as etapas: seleção de símbolo, obtenção de candles e cálculos. |
|  **Estrutura modular** | Separação clara entre camadas `model`, `controller`, `view` e `plugin`, facilitando testes unitários e futuras extensões. |

---

## Arquivos revisados

| Arquivo | Função principal | Status |
|----------|------------------|---------|
| `volume_model.py` | Obtenção de candles e cálculo de perfil/estatísticas | ✅ Revisado — sem erros |
| `volume_controller.py` | Controle do fluxo, conversão de timezone e agregação de contexto | ✅ Revisado — fusos corrigidos |
| `volume_view.py` | Exibição acessível do Volume Profile | ✅ Revisado — saída organizada |
| `plugin.py` | Registro do comando `volume` no CLI principal | ✅ Revisado — funcionamento correto |

---

## Recomendações de melhoria futura

1. **Aviso sobre `real_volume`:** nem todas as corretoras expõem esse campo. Sugestão: adicionar fallback automático e log de aviso.
2. **Centralização de timezone:** ler configuração de fuso horário do arquivo global `mtcli.conf` para padronizar entre plugins.
3. **Testes automatizados:** incluir casos de teste com `pytest` para validar formatos alternativos de dados (dict, numpy, tupla).
4. **Internacionalização:** considerar opção `--lang` para mensagens em inglês em futuras versões.

---

## Conclusão

A versão **2.2.0** do plugin `mtcli-volume` é **estável, acessível e pronta para produção**, resolvendo o problema de horário e consolidando a arquitetura modular.  
Nenhum erro lógico ou sintático foi identificado.
