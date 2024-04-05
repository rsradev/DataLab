def get_current_price(coin):
    print(f'Getting current price of {coin}')

    if coin == 'bitcoin':
        return 1000
    elif coin == 'etherum':
        return 1000
    elif coin == 'solana':
        return 100
    else:
        return -1