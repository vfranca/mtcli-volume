# Como usar o plugin
  
```bash
mt volume \[OPTIONS]
```
  
## Opções disponíveis
  
| Opção          | Descrição                                      |
|----------------|-----------------------------------------------|
| --symbol     | Ativo a ser analisado (ex: WINV25)            |
| --periods    | Número de candles (padrão: 500)               |
| --step       | Tamanho da faixa de preço (ex: 5 pontos)      |
| --exporta-csv| Exporta os dados para arquivo CSV             |
  
## Exemplo de uso
  
```bash
mt volume -s WINV25 -p 500 -e 10 --exporta-csv
```
  
Isso irá gerar um CSV chamado volume\_profile\_WINV25\_2025-09-05.csv com os dados do volume profile.
