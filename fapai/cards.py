import random

ranks = [i for i in range(2, 15)]
suits = ['Spades', 'Diamonds', 'Clubs', 'Hearts']
cards52 = [(suit, rank) for rank in ranks for suit in suits]
cards54 = cards52 + [('jokers', 100), ('jokers', 200)]


def deal(cardsnum: int, playernum: int, desknum: int, jokersin=True):
    handnum = ((54 if jokersin else 52)*cardsnum-desknum)/playernum
    if handnum != int(handnum):
        raise ValueError('不能这么玩！')
    handnum = int(handnum)
    if jokersin:
        cards = cards54 * cardsnum
    else:
        cards = cards52 * cardsnum
    random.shuffle(cards)
    result = {}
    for i in range(playernum):
        result['player'+str(i+1)] = cards[i*handnum:(i+1)*handnum]
        # result['player'+str(i+1)].sort()
    if desknum != 0:
        result['desk'] = cards[-desknum:]
    return result
