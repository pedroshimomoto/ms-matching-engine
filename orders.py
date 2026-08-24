from decimal import Decimal
seq = 0
orders_list = []

while True:
    user_input = input(f'>>>')
    seq += 1
    splitted = user_input.split()
    
    if not splitted:
        continue

    order = splitted[0].lower() #da pra usar POO aqui
    
    if order == 'limit': #fun limit/market
        if len(splitted) != 4:
            print(f'Argumentos faltando')
            continue

        side = splitted[1]
        price = Decimal(splitted[2])
        qty = int(splitted[3])

    elif order == 'market':
        if len(splitted) != 3:
            print(f'Argumentos faltando')
            continue
        order = splitted[0]
        side = splitted[1] # a primeiro momento não dar id pra market, pois assume-se que ela morre no instante do input
        qty = int(splitted[2]) #isso q muda do market pro limit

    else:
        print(f'Comando desconhecido')
        
    print(f'order: {order}, side: {side}, qty: {qty}')


