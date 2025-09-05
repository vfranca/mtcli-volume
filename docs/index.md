# mtcli-volume
  
`mtcli-volume` é um plugin para o projeto [mtcli](https://github.com/vfranca/mtcli) que exibe o *Volume Profile* de um ativo utilizando dados do MetaTrader 5.
  

Este plugin permite visualizar textualmente via terminal a distribuição de volume por faixa de preço, além de identificar o POC (Point of Control), Área de Valor, High Volume Nodes e Low Volume Nodes.

  

---

  

## 🔍 O que é Volume Profile?

  

O *Volume Profile* é uma ferramenta gráfica que mostra o volume negociado em diferentes níveis de preço, ao longo de um período. Ele ajuda a identificar:

  

- *POC*: Nível de preço com maior volume.

- *Área de Valor*: Faixa de preço com cerca de 70% do volume total.

- *HVNs*: Níveis de preço com volumes elevados.

- *LVNs*: Níveis de preço com volumes baixos.

  

---

  

## 🧰 Recursos do plugin

  

- Agrupamento de volume por faixa de preço.

- Cálculo e exibição de:

  - *POC*

  - *Área de Valor*

  - *HVNs* e *LVNs*

- Exportação para CSV com data no nome do arquivo.

- Exibição textual com barras proporcionais ao volume.





