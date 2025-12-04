import tkinter as tk
from tkinter import messagebox

from laro import create_deck, shuffle_deck, deal_card, hand_value, is_blackjack


class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        root.title('Blackjack')

        self.deck = []
        self.player_hand = []
        self.dealer_hand = []

        # Dealer frame
        self.dealer_frame = tk.LabelFrame(root, text='Dealer', padx=10, pady=10)
        self.dealer_frame.grid(row=0, column=0, padx=10, pady=5, sticky='ew')
        self.dealer_cards_label = tk.Label(self.dealer_frame, text='')
        self.dealer_cards_label.pack()
        self.dealer_value_label = tk.Label(self.dealer_frame, text='Value:')
        self.dealer_value_label.pack()

        # Player frame
        self.player_frame = tk.LabelFrame(root, text='Player', padx=10, pady=10)
        self.player_frame.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
        self.player_cards_label = tk.Label(self.player_frame, text='')
        self.player_cards_label.pack()
        self.player_value_label = tk.Label(self.player_frame, text='Value:')
        self.player_value_label.pack()

        # Buttons
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.grid(row=2, column=0, pady=10)
        self.hit_button = tk.Button(self.buttons_frame, text='Hit', width=10, command=self.player_hit, state='disabled')
        self.hit_button.grid(row=0, column=0, padx=5)
        self.stand_button = tk.Button(self.buttons_frame, text='Stand', width=10, command=self.player_stand, state='disabled')
        self.stand_button.grid(row=0, column=1, padx=5)
        self.new_button = tk.Button(self.buttons_frame, text='New Game', width=10, command=self.new_game)
        self.new_button.grid(row=0, column=2, padx=5)
        self.quit_button = tk.Button(self.buttons_frame, text='Quit', width=10, command=root.quit)
        self.quit_button.grid(row=0, column=3, padx=5)

        # Start
        self.new_game()

    def format_hand(self, hand, hide_first=False):
        if hide_first and hand:
            return ['??'] + [f"{r}{s}" for r, s in hand[1:]]
        return [f"{r}{s}" for r, s in hand]

    def update_display(self, hide_dealer=True):
        dealer_cards = ' '.join(self.format_hand(self.dealer_hand, hide_first=hide_dealer))
        self.dealer_cards_label.config(text=dealer_cards)
        self.dealer_value_label.config(text=f"Value: {'?' if hide_dealer else hand_value(self.dealer_hand)}")

        player_cards = ' '.join(self.format_hand(self.player_hand))
        self.player_cards_label.config(text=player_cards)
        self.player_value_label.config(text=f"Value: {hand_value(self.player_hand)}")

    def new_game(self):
        self.deck = create_deck()
        shuffle_deck(self.deck)
        self.player_hand = [deal_card(self.deck), deal_card(self.deck)]
        self.dealer_hand = [deal_card(self.deck), deal_card(self.deck)]

        self.hit_button.config(state='normal')
        self.stand_button.config(state='normal')

        self.update_display(hide_dealer=True)

        # Check for blackjack
        if is_blackjack(self.player_hand) or is_blackjack(self.dealer_hand):
            self.update_display(hide_dealer=False)
            if is_blackjack(self.player_hand) and is_blackjack(self.dealer_hand):
                messagebox.showinfo('Result', 'Both have Blackjack: Push')
            elif is_blackjack(self.player_hand):
                messagebox.showinfo('Result', 'Player has Blackjack! You win.')
            else:
                messagebox.showinfo('Result', 'Dealer has Blackjack. You lose.')
            self.hit_button.config(state='disabled')
            self.stand_button.config(state='disabled')

    def player_hit(self):
        self.player_hand.append(deal_card(self.deck))
        self.update_display(hide_dealer=True)
        if hand_value(self.player_hand) > 21:
            self.update_display(hide_dealer=False)
            messagebox.showinfo('Result', 'You busted!')
            self.hit_button.config(state='disabled')
            self.stand_button.config(state='disabled')

    def player_stand(self):
        self.hit_button.config(state='disabled')
        self.stand_button.config(state='disabled')
        # Reveal dealer and play
        self.update_display(hide_dealer=False)
        self.dealer_play()

    def dealer_play(self):
        while hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(deal_card(self.deck))
            self.update_display(hide_dealer=False)

        # Compare
        pval = hand_value(self.player_hand)
        dval = hand_value(self.dealer_hand)
        if dval > 21:
            message = f'Dealer busted ({dval}). You win!'
        elif pval > dval:
            message = f'You win! ({pval} vs {dval})'
        elif pval < dval:
            message = f'You lose. ({pval} vs {dval})'
        else:
            message = f'Push (tie) ({pval} vs {dval})'

        messagebox.showinfo('Result', message)


def run_gui():
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()


if __name__ == '__main__':
    run_gui()
