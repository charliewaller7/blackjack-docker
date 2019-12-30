""" Deck object """

from refs.functions import *
import random


class Deck:

	def __init__(self, no_of_decks=1):

		self.no_of_decks = no_of_decks
		self.cards = self._create_deck()

	def _create_deck(self):
		""" Creates the deck for that table. """
		cards = list(get_card_values().keys()) * self.no_of_decks
		return cards

	def shuffle(self):
		""" Shuffle current deck """
		random.shuffle(self.cards)
		return

	def add_card(self, card):
		if self.cards.count(card) >= self.no_of_decks:
			raise Exception(f"There is already {self.no_of_decks} of {card} in the deck.")

		self.cards.append(card)
		return

	def draw_card(self, card=None):
		if len(self.cards) < 1:
			return "Deck is empty"
		if card is None:
			return self.cards.pop(0)
		elif card not in self.cards:
			raise Exception(f"Invalid card, {card} not in deck.")
		else:
			self.cards.remove(card)
			return card