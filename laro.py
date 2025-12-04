import random
import sys


def create_deck():
    """Create and return a standard 52-card deck as (rank, suit) tuples."""
    ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
    suits = ['♠', '♣', '♥', '♦']
    return [(rank, suit) for rank in ranks for suit in suits]


def shuffle_deck(deck):
    random.shuffle(deck)


def deal_card(deck):
    return deck.pop()


def hand_value(hand):
    """Return the best Blackjack value for a hand (Aces as 1 or 11)."""
    value = 0
    aces = 0
    for rank, _ in hand:
        if isinstance(rank, int):
            value += rank
        elif rank in ('J', 'Q', 'K'):
            value += 10
        elif rank == 'A':
            aces += 1
    # Add aces as 11 when it doesn't bust, otherwise as 1
    for _ in range(aces):
        if value + 11 <= 21 - (aces - 1):
            value += 11
        else:
            value += 1
    return value


def is_blackjack(hand):
    return len(hand) == 2 and hand_value(hand) == 21


def display_hand(hand, who='Player', hide_first=False):
    if hide_first:
        cards = ['??'] + [f"{r}{s}" for r, s in hand[1:]]
    else:
        cards = [f"{r}{s}" for r, s in hand]
    print(f"{who}: {' '.join(cards)}  (value: {'?' if hide_first else hand_value(hand)})")


def player_turn(deck, player_hand):
    while True:
        display_hand(player_hand, 'Player')
        if hand_value(player_hand) > 21:
            print('You busted!')
            return
        choice = input("Hit or Stand? (h/s, q to quit): ").strip().lower()
        if choice == 'q':
            print('Quitting game.')
            sys.exit(0)
        if choice == 'h':
            player_hand.append(deal_card(deck))
            continue
        if choice == 's' or choice == '':
            return
        print("Please enter 'h' to hit, 's' to stand, or 'q' to quit.")


def dealer_turn(deck, dealer_hand):
    # Dealer hits until 17 or higher (soft 17 stands)
    while True:
        value = hand_value(dealer_hand)
        if value < 17:
            dealer_hand.append(deal_card(deck))
            continue
        return


def compare_hands(player_hand, dealer_hand):
    player_val = hand_value(player_hand)
    dealer_val = hand_value(dealer_hand)
    if player_val > 21:
        return 'lose'
    if dealer_val > 21:
        return 'win'
    if player_val > dealer_val:
        return 'win'
    if player_val < dealer_val:
        return 'lose'
    return 'push'


def play_round():
    deck = create_deck()
    shuffle_deck(deck)

    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    print('\n--- New Round ---')
    display_hand(dealer_hand, 'Dealer', hide_first=True)
    display_hand(player_hand, 'Player')

    # Check for immediate blackjack
    player_blackjack = is_blackjack(player_hand)
    dealer_blackjack = is_blackjack(dealer_hand)
    if player_blackjack or dealer_blackjack:
        display_hand(dealer_hand, 'Dealer')
        if player_blackjack and dealer_blackjack:
            print('Both have Blackjack: Push.')
            return 'push'
        if player_blackjack:
            print('Player has Blackjack! You win 1.5x.')
            return 'blackjack'
        print('Dealer has Blackjack. You lose.')
        return 'lose'

    # Player turn
    player_turn(deck, player_hand)

    # Dealer turn (only if player hasn't busted)
    if hand_value(player_hand) <= 21:
        print()
        display_hand(dealer_hand, 'Dealer')
        dealer_turn(deck, dealer_hand)
        display_hand(dealer_hand, 'Dealer')

    result = compare_hands(player_hand, dealer_hand)
    if result == 'win':
        print('You win!')
    elif result == 'lose':
        print('You lose.')
    else:
        print('Push (tie).')
    return result


def main():
    print('Simple Blackjack — type q to quit at any prompt')
    rounds_played = 0
    while True:
        outcome = play_round()
        rounds_played += 1
        again = input("Play another round? (y/n): ").strip().lower()
        if again == 'q' or again == 'n':
            print(f'Goodbye — rounds played: {rounds_played}')
            break


if __name__ == '__main__':
    main()