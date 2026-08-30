# Matching Engine
Implementação de uma matching engine, usando um único ativo, com as ordens limit, market, pegged, cancelamento e visualização de um livro de ordens de compras e vendas
O código não possui dependências externas, toda memória em estado volátil

## Como Executar

``` bash
python orders.py
```

Rodando isso, o programa abre um prompt interativo (>>>) que lê o comando digitado, pode ser encerrado com `Ctrl + C`

Os exemplos do enunciado (sequência principal, requisito 4 e requisito 5) foram verificados manualmente e reproduzem a saída esperada, com a ressalva descrita nas limitações.

## Comandos

| Comando | Sintaxe | Descrição |
|---|---|---|
| Limit | `limit <buy\|sell> <price> <qty>` | Ordem com preço fixo |
| Market | `market <buy\|sell> <qty>` | Ordem executada ao melhor preço disponível |
| Pegged | `peg <bid\|offer> <buy\|sell> <qty>` | Ordem ancorada no melhor preço do book |
| Cancelar | `cancel order <id>` | Remove a ordem do livro |
| Alterar | `edit order <id> [price <valor>] [qty <valor>]` | Altera preço, quantidade ou ambos |
| Livro | `print book` | Exibe o livro de ofertas |

Exemplo:

```
>>> limit buy 10 100
Order created: buy 100 @ 10 id: 1
>>> limit sell 20 100
Order created: sell 100 @ 20 id: 2
>>> market buy 150
Trade, price: 20, qty: 100
>>> print book
Ordens de Compra    | Ordens de Venda
--------------------|--------------------
100 @ 10            |
```

## Regras de prioridade

O book segue o **price-time priority**:

1. **Preço** - sempre decide primeiro, independente. Na compra, o maior preço é o melhor, na venda o menor preço é o melhor
2. **Tempo** - só é aplicado em caso de desempate de preços. Quem chegou antes executa antes

Ordem de chegada nunca supera o preço. Uma ordem que acabou de entrar no book com preço melhor passa na frente de todas as outras

No script isso acontece na função `compare_price`, que usa uma comparação ('>' / '<'), no empate de preço ela devolve False e o loop continua, assim a nova ordem ficará atrás das que já existiam

## Decisões técnicas

### Preços com `Decimal`, não `float`

O `float` é binário e possui imprecisões em valores como `9.99`. Essa aplicação depende diretamente da igualdade entre preços. Ou seja, um erro de arredondamento causaria comportamentos indesejados.
Por isso optei por utilizar o `Decimal`, pois ele representa valores em base decimal; construído a partir de string, o valor é exato.

### Limit orders que cruzam são preenchidas

Optei por **preencher**, principalmente pelo seguinte motivo:
- É o comportamento de uma exchange real. Uma limit define o preço máximo, não que necessariamente precise esperar. Se ignorasse, o book poderia ficar com um bid acima de um ask, que é inconsistente.

Uma limit pode ser passiva e agressiva numa mesma execução: a parte que cruza e o restante que fica esperando no livro

### Trade é feito no preço da ordem passiva

Quando uma orfem agressiva acontece, o preço do trade é o da que estava esperando no livro. Uma `limit buy 25` contra um offer de 20, negocia a 20.

### Market orders descartam a quantidade não executada

Como uma market order não tem preço, ela é uma ordem instantânea que não fica no livro.
Esse comportamento é confirmado no exemplo do enunciado (passo 5). Uma `market buy 200` executa 150 e sobram 50. No passo 6, a market sell 200 tem um trade com os `100 @ 10`. Se os 50 tivessem ficado no livro, o passo 6 teria um output diferente

### Trades não são agregados por nível de preço

Quando uma ordem consome várias já no livro, é emitido um trade por ordem consumida, não um trade agregado

O exemplo do enunciado mostra `Trade, price: 20, qty: 150` para uma execução de duas ordens distintas (100 e 50) no mesmo preço. Optei por mostrar os dois trades, pois agregar perderia informações

### Regras de prioridade na alteração

| Alteração | Prioridade |
|---|---|
| Preço muda | **Perde** — vai para o fim da fila do novo nível |
| Quantidade aumenta | **Perde** |
| Quantidade diminui | **Preserva** |

Aumentar a quantidade piora a situação de quem está atrás na fila: essa ordem passa a esperar que uma ordem maior consuma a liquidez antes dela. Já diminuir beneficia quem está atrás, por isso não há razão para punir quem fez a edição.


### Sintaxe do comando de alteração

O enunciado descreve o comportamento da edição, mas não a sintaxe. Usei a seguinte forma: `edit order <id> [price <valor>] [qty <valor>]`

### Identificadores

Ids são inteiros que nunca serão reutilizados, mesmo depois de cancelamento ou trade. Reutilizá-los traria ambiguidade no decorrer da sessão.
O contador aumenta para toda ordem válida, inclusive as rejeitadas (ex: peg sem âncora de preço)
O enunciado usa `identificador_1` como ilustrativo, interpretei como indicação de que existe um identificador, não como formato exigido

### Ordens pegged

Uma ordem pegged fixa seu preço automaticamente com o melhor de uma referência (`bid` ou `offer`), sendo ela reprecificada sempre que essa referência muda

### Combinações pegged rejeitadas

`peg bid sell` e `peg offer buy` ancorariam a ordem no lado oposto, gerando trade na criação e contradizendo a natureza passiva do instrumento. São aceitas apenas `peg bid buy` e `peg offer sell`.

### Âncora ignora outras pegged

O cálculo do melhor preço de referência pula as orders pegged, evitando que uma se ancore na outra

### Pegged sem âncora

Se o book de referência estiver vazio, não há preço a seguir e a ordem não é criada

### Reprecificação preserva preço da âncora

Alterar o preço de uma order pegged usando `edit` não tem efeito, pois a reprecificação automática restaura o preço da âncora.

## Complexidade
 
| Operação | Complexidade | Observação |
|---|---|---|
| `parse` | O(1) | Não depende do tamanho do livro |
| `matches` / `compare_price` | O(1) | Comparação simples |
| `insert_book` | O(log n) | O(1) amortizado, O(log n) ao criar um novo nível de preço|
| `cancel_order` | O(n) | Localização em O(1) pelo índice; `remove` do deque é O(n) |
| `edit_order` | O(n) | `remove` + `insert` |
| `best_order` | O(n) no pior caso | Típico O(1): para na primeira ordem não-pegged |
| `trades` | O(k) | k = ordens consumidas; `popleft()` em `deque` é O(1) |
| `reprice_peg` | O(P · n) | P = ordens pegged ativas |
| `print_book` | O(n) | Percorre ambos os lados |

Os dois lados do book usam `collections.deque` em vez de `list`. Isso faz diferença na remoção do top no matching: `list.pop(0)` muda (desloca) todos os elementos seguintes (O(n)), já o `deque.popleft()` é O(1)

O índice `orders_by_id` permite localizar qualquer ordem em O(1), essencial para cancelamento e alteração. O que aumenta a complexidade vem da estrutura do leque (remove, insert), pois esses comandos deslocam todos os elementos seguintes

**Onde isso ultrapassa O(n):** apenas `reprice_peg`, que executa uma operação O(n)
(`remove` + `insert`) dentro de um laço que roda P vezes. No caso típico P é pequeno
(poucas pegged ativas), mas o pior caso é quadrático.

### Possíveis otimizações

- `dict` de `preço → nível de preço` — acesso ao nível em O(1)
- lista duplamente ligada dentro de cada nível — remoção arbitrária em O(1), pois basta religar os vizinhos, sem deslocar nada
- heap dos preços ativos — melhor preço em O(1), inserção de novo nível em O(log n)
- `dict` de `id → nó` — cancelamento e alteração em O(1) reais

Fazendo isso, `insert_book`, `cancel_order` e `edit_order` cairiam para O(1), e `reprice_peg` para O(P)

## Estrutura do código

Arquivo único, `orders.py`, dividido em blocos comentados que mapeiam os requisitos:

- **Estado global** — os dois lados do livro, o índice por id e a lista de pegged ativas
- **Parsing e validação** (`qty_parse`, `price_parse`, `side_parse`, `parse`) — traduzem o texto em estrutura e validam a sintaxe dos comandos
- **Núcleo do matching** (`matches`, `compare_price`, `insert_book`, `trades`) — requisitos 1 e 2
- **Cancelamento** (`cancel_order`) — requisito 3
- **Alteração** (`edit_order`) — requisito 4
- **Ordens pegged** (`best_order`, `reprice_peg`) — requisito 5
- **Visualização** (`print_book`) — requisito adicional 1
- **Loop principal** (`main`) — lê comandos e despacha

A função `trades` retorna a lista de negócios em vez de imprimi-los; a impressão fica a cargo do `main`.

O enunciado permite implementação estrutural ou orientada a objetos. Optei pela estrutural. A conversão natural para POO agruparia o estado compartilhado: `bids`, `offers` e `orders_by_id` formariam um `OrderBook`; o contador de ids e a lógica de matching formariam uma `MatchingEngine`; os dicionários de ordem virariam uma classe `Order`, com `PeggedOrder` como especialização, por ter estado próprio (a referência) e comportamtento próprio (a reprecificação). As funções de parsing permaneceriam funções, por não terem estado.

## Limitações conhecidas

1. **Alteração que cruza não gera trade.** Se um `edit` leva uma ordem a um preço que cruza no outro book, ela é reinserida sem passar pelo matching. A correção exigiria casar a ordem enquanto está fora do livro
2. **Reprecificação de pegged não dispara matching.** A função `reprice_peg` apenas reposiciona a ordem no livro. Uma pegged reprecificada para um preço que cruze, permanece no livro sem ter o trade
3. **Prioridade da pegged reprecificada.** No exemplo do requisito 5, a ordem peg aparece na frente da limit que causou a mudança de preço, preservando sua prioridade original. Aqui ela é removida e reinserida, então entra no fim do novo nível de preço. O comportamente funcional (seguir a referência) está correto, apenas a posição relativa dentro do nível que muda
4. **Inserção e remoção no meio do livro O(n)**, conforme detalhado na seção de complexidade 