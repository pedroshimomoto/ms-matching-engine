from decimal import Decimal, InvalidOperation
seq = 0
orders_list = []

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
        for trade in trades(order):
            print(f'Trade, price: {trade['price']}, qty: {trade['qty']}')

if __name__ == '__main__':
    main()
        

