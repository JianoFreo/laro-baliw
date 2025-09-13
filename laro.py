import random 

choice = input('Press enter to pick a card (q to quit)')

while choice.lower() != 'q':
    cardvalue = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 'A', 'J', 'Q', 'K'])
    cardclass = random.choice(['spades', 'clubs', 'hearts', 'diamond'])
    print(cardvalue, cardclass)
    choice = input('Press enter to pick a card (q to quit)')
print('bye')