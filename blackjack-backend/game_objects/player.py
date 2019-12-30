""" Player class """
# TODO - add in budget restraints

from game_objects.table import *
from game_objects.hand import *
from game_objects.hand_outcome import *
from refs.strategy_tables import *


class Player:

	def __init__(self, name, budget, strategy='basic_strategy', card_counting=True):
		self.name = name
		self.start_budget = budget
		self.balance = budget
		self.hands = [self.create_hand(bet=100)]
		self.history = list()
		self.is_split = False
		self.strategy = strategy
		self.card_counting = card_counting

	def create_hand(self, bet):
		""" Instantiate player hand """
		# TODO - make bet_value dynamic
		hand = Hand(bet=bet)
		return hand

	def hit(self, card, hand_num=0):
		""" draw new card for player. Hand_num for managing split hands (zero indexed) """

		if self.hands[hand_num].is_stood:
			print(f"{self.name} cannot hit as already stood")
			return

		if self.hands[hand_num].is_bust:
			print(f"{self.name} is bust and cannot hit")
			return

		self.hands[hand_num].add_card(card)

		# reduce ace values 1 by 1 to check if bust
		for i in [c for c in self.hands[hand_num].cards if 'A' in c]:
			if self.hands[hand_num].value > 21:
				self.hands[hand_num].ace_to_one(first_only=True)
				continue

		# Bust if value greater than 21
		if self.hands[hand_num].value > 21:
			self.hands[hand_num].is_bust = True

		return

	def stand(self, hand_num=0):
		""" Stand, no more cards can be drawn """
		self.hands[hand_num].is_stood = True
		return

	def double_down(self, card, hand_num=0):
		""" Double bet value for one more card only"""
		if self.name == 'DEALER':
			print(f"Dealer cannot double down")
			return

		if len(self.hands[hand_num].cards) != 2:
			return f"You can only double-down on your first new card. Current cards are {self.hands[hand_num].cards}."

		self.hands[hand_num].bet = self.hands[hand_num].bet * 2
		self.hit(card, hand_num=hand_num)
		self.hands[hand_num].is_stood = True
		return

	def split(self, card_1, card_2, hand_num=0):
		""" Where both cards are the same number/face, split cards into two hands """
		if self.name == 'DEALER':
			print(f"Dealer cannot split")

		if len(self.hands[hand_num].cards) != 2:
			print(f"You can only split on your first new card. Current cards are {self.hands[hand_num].cards}.")
			return 'na'

		if self.hands[hand_num].cards[0][0] != self.hands[hand_num].cards[1][0]:
			print("You can only split on cards with the same number/picture.")
			return 'na'

		# Create new hand using previous cards
		split_hand = self.create_hand(bet=self.hands[hand_num].bet)
		split_hand.add_card(card=self.hands[hand_num].cards.pop())

		# add one new card to each hand
		self.hands[hand_num].add_card(card_1)
		split_hand.add_card(card_2)

		# Reverse ace values to 11
		self.hands[hand_num].ace_to_one(reverse=True)
		split_hand.ace_to_one(reverse=True)

		self.hands.append(split_hand)
		self.is_split = True
		return

	def player_decision(self, dealer_hand, hand_num=0):
		""" Method to return a player decision (hit, stick, double etc.) based on the strategy and current cards """
		strategy = basic_strategy
		hand = self.hands[hand_num]
		dealer_card = dealer_hand.cards[0].split('-')[0]

		if hand.is_bust:
			print(f"{self.name} already bust")
			return

		if (len(hand.cards) == 2) and (hand.cards[0].split('-')[0] == hand.cards[1].split('-')[0]):
			hand_type = 'pair'
			card = hand.cards[0].split('-')[0]
		elif (any([True for c in hand.cards if 'A' in c])) and (len(hand.cards) == 2):
			hand_type = 'soft'
			card = str(hand.value)
		else:
			hand_type = 'hard'
			card = str(hand.value)

		return strategy[hand_type][dealer_card][card]

	def update_budget(self, value):
		""" Function to update budget """
		self.balance = self.balance + value
		return

	def record_and_reset(self, dealer_hand):
		""" records hand in history and reset hand """
		hand_outcome = HandOutcome(player_hand=self.hands, dealer_hand=dealer_hand)
		self.history.append(hand_outcome)
		self.hands = [self.create_hand(bet=100)]
		self.is_split = False
		return