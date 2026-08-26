from decimal import Decimal, InvalidOperation
seq = 0
bids = [] #nova abordagem, não será lista única
offers = [] # uma lista para cada lado

# funções auxiliares para tratamento dos textos
def qty_parse(texto):
    try:
        qty = int(texto)
    except ValueError:
        raise ValueError(f'Quantidade inválida: {texto}')
    if qty <= 0:
        raise ValueError(f'Quantidade deve ser positiva')
    return qty

def price_parse(texto):
    try:
        price = Decimal(texto)
    except InvalidOperation:
        raise ValueError(f'Preço Inválido: {texto}')
    if price <= 0:
        raise ValueError('O preço deve ser positivo')  #tratando hipótese de apenas posicoes long
    return price

def side_parse(texto):
    side = texto.lower()
    if side not in ('buy', 'sell'):
        raise ValueError(f'Side inválido: {texto}')
    return side

#função principal do parse

def parse(input):
    splitted = input.split()
    if not splitted:
        return None

    order = splitted[0].lower()

    if order == 'limit':
        if len(splitted) != 4:
            print(f'Argumentos faltando')
            return None
        return {
            'Ordem': order,
            'Lado': side_parse(splitted[1]),
            'Preço': price_parse(splitted[2]),
            'Quantidade': qty_parse(splitted[3]),
        }

    elif order == 'market':
        if len(splitted) != 3:
            print(f'Argumentos faltando')
            return None
        return {
            'Ordem': order,
            'Lado': side_parse(splitted[1]),
            'Quantidade': qty_parse(splitted[2]),          
        }
    else:
        print(f'Comando desconhecido')
        return None

def trades(order): #Vazio por enquanto,
    return []

#antes de fazer toda a lógica da função trades: vou escrever a função insert_book e compara_price, pois a função trades depende dessa

def compare_price(order, book_order):
    if order['Lado'] == 'buy': #lógica: melhor preço de buy: maior; melhor preço de sell: menor
        return order['Preço'] > book_order['Preço'] #lógica booleana, vai devolver True ou false, comparando a order nova com a order do book
    else:
        return order['Preço'] < book_order['Preço']

def insert_book(order):
    book = bids if order['Lado'] == 'buy' else offers
    i = 0
    while i < len(book) and not compare_price(order, book[i]): # loop continua enquanto o price da order não for melhor que a order do book
        i += 1 #vai contanndo os indices
    book.insert(i, order) # coloca a order no book no indice i e empurra todos os outros pra trás (se tiver)

id = 0

def main():
    global id
    while True:
        user_input = input(f'>>>')
        try:
            order = parse(user_input)
        except ValueError as e:
            print(f'Erro: {e}')
            continue
        if order is None:
            continue

        id += 1
        order['id'] = id #deixar o id como int por enquanto, str creio que será dificil de tratar depois

        if order['Ordem'] == 'limit':
            insert_book(order)

        print('BIDS:', [(str(o['Preço']), o['Quantidade']) for o in bids])
        print('OFFERS:', [(str(o['Preço']), o['Quantidade']) for o in offers])
        
        for trade in trades(order):
            print(f'Trade, price: {trade['price']}, qty: {trade['qty']}')

if __name__ == '__main__':
    main()
        

