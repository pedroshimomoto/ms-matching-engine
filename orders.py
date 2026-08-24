seq = 0
while True:
    user_input = input(f'>>>')
    seq += 1
    if 'limit' in user_input: #fun limit/market
        splitted = user_input.split()
        order = splitted[0] #da pra usar POO aqui
        side = splitted[1]
        price = splitted[2]
        qty = splitted[3]
        id = 'identificator_' + str(seq) #tem que ficar dentro, se der print book, vai contar como id
        print(f'id: {id}')
        
    if 'market' in user_input:
        splitted = user_input.split()
        order = splitted[0]
        side = splitted[1] # a primeiro momento não dar id pra market, pois assume-se que ela morre no instante do input
        qty = splitted[2] #isso q muda do market pro limit
        
    print(f'order: {order}, side: {side}, qty: {qty}')
