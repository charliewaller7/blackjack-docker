""" reference objects for the game (e.g. card values) """


def get_card_values():
    values = dict()
    for suit in ['H', 'D', 'C', 'S']:
        for card in [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']:
            value = card if isinstance(card, int) else 10
            if card == 'A':
                value = 11
            values[f'{card}-{suit}'] = value

    return values


def get_shuffle_rules():
    rules = ['every_hand', 'blackjack_only']
    return rules


def check_history(table, hand_index, player=0):
    """ function to summarise history from specified hand """
    hist = table.players[player].history[hand_index]
    print(f"Status: {', '.join([str(x) for x in hist.status])}")
    print(f"Value: {', '.join([str(x) for x in hist.hand_value])}")
    print(f"Player cards: ")
    for h in hist.player_hand:
        print(f"cards: {h.cards}   value: {h.value}")
    print(f"Dealer cards: {hist.dealer_hand[0].cards}  value: {hist.dealer_hand[0].value}")
    print("------------------------------------------------\n")