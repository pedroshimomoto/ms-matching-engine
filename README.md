## Exercício programa de uma Matching Machine 
### Objetivo: Cruzar dados em uma Exchange
- Ordens possíveis: limit -> ordem passiva (preço fixo), market -> ordem preenchida com o melhor preço disponível
- Não é necessário armazenamento perene
- Não é necessário pensar em escalabilidade de hardware, nuvem ou elasticidade
- Interface de input e cancelamento (buy, sell, cancel)
- Interface de display de book (2 sides: buy | sell)
- Ordem de preço prevalece (melhor preço de buy: maior preço; melhor preço de sell: menor preço)
- Ordem de chegada (desempate)
- Pegged: 'prego' -> fixa o preço de acordo com o melhor de compra/venda (bid: melhor de buy e offer: melhor de sell)


### Decisões de desing:
