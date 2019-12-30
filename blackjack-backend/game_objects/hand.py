""" Hand class """
from refs.functions import *


class Hand:

	def __init__(self, bet):
		self.cards = list()
		self.value = self.get_value()
		self.bet = bet
		self.card_values = get_card_values()
		self.is_bust = False
		self.is_stood = False

	def get_value(self):
		values = [self.card_values[card] for card in self.cards]
		return sum(values)

	def show_hand(self):
		for num, card in enumerate(self.cards):
			card_values = get_card_values()
			print(f'Card {num+1}) {card}  ({card_values[card]})')

	def add_card(self, card):
		if card not in get_card_values().keys():
			raise Exception("Card not valid, ensure that all cards are in the format 'card-suit', e.g. '9-S'.")

		self.cards.append(card)
		self.value = self.get_value()
		return self.cards

	def ace_to_one(self, reverse=False,first_only=False):
		""" changes an aces value from 11 to 1 (and vice versa) called when player bust """

		val = 11 if reverse else 1
		for c in self.cards:
			if 'A' in c:
				self.card_values[c] = val
				self.value = self.get_value()
				if first_only:
					return
		return