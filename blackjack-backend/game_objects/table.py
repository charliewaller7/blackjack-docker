""" Table object """

from refs.functions import *
from game_objects.deck import *
from game_objects.player import *
from game_objects.hand_outcome import *
import random


class Table:

	def __init__(self, max_players=1, no_of_decks=1, shuffle_rules='every_hand', dealer_stick=17, bet_limit=None, peak_for_bj=True):

		# input validation
		if not isinstance(max_players, int) and max_players <= 0:
			raise Exception("Maximum number of players must be a positive integer")

		if not isinstance(no_of_decks, int) and no_of_decks <= 0:
			raise Exception("Number of decks must be a positive integer")

		if not isinstance(dealer_stick, int) and dealer_stick <= 0:
			raise Exception("Dealer stick value must be a positive integer (16 or 17)")

		if shuffle_rules not in get_shuffle_rules():
			raise Exception(
				f"shuffle rule must be listed in get_shuffle_rules reference {(', '.join(get_shuffle_rules()))}")

		if bet_limit is not None and not isinstance(bet_limit, int):
			raise Exception("Bet limit must be EITHER a positive integer or None")

		self.max_players = max_players
		self.no_of_decks = no_of_decks
		self.shuffle_rules = shuffle_rules
		self.dealer_stick = dealer_stick
		self.bet_limit = bet_limit
		self.deck = self._create_deck()
		self.table_balance = 1000000
		self.players = list()
		self.dealer = self.create_dealer()
		self.card_count = 0


	def _create_deck(self):
		""" Creates the deck for that table. """
		return Deck(no_of_decks=self.no_of_decks)

	def create_dealer(self):
		""" Method to create dealer using player object """
		dealer = Player(name='DEALER', budget=self.table_balance)
		return dealer

	def add_player(self, player):
		""" Adds a player to the table. Takes in a player object as input"""
		if player.name not in [player.name for player in self.players]:
			self.players.append(player)
		else:
			print(f"There is already a player with the name {player.name}.")
			return

		return f"Player '{player.name}' added."

	def get_count(self):
		# TODO - Add all to strategy
		# Count
		full_deck = self._create_deck().cards
		played_cards = [card for card in full_deck if card not in self.deck.cards]
		card_values = get_card_values()
		values = [card_values[card] for card in played_cards]
		count = sum([1 if x <= 6 else -1 if x >= 10 else 0 for x in values])

		# Remaining decks
		error_rate = 15
		error = random.randint(-error_rate, error_rate)
		remaining_cards = len(self.deck.cards) + error
		decks_remaining = round((remaining_cards/52) * 2) / 2

		true_count = count / decks_remaining

		return count, true_count

	def _deal_one(self, player):
		""" deals one card to a specified player."""
		player.hit(self.deck.draw_card())
		return

	def deal_round(self):
		""" deal a round a cards. Two to each player, hiding one dealer card.  """

		# Clear previous cards
		for player in (self.players + [self.dealer]):
			if player.card_counting:
				count, true_count = self.get_count()
				betting_unit = player.balance / 100
				bet = min((true_count-1) * betting_unit, player.balance/4)
			else:
				bet = player.balance / 100

			player.hands = [player.create_hand(bet=bet)]

		for player in (self.players + [self.dealer]) * 2:
			self._deal_one(player)
		return

	def _one_turn(self, player, hand_num=0):
		""" Applies a single decision for a player based on the card """
		decision = player.player_decision(dealer_hand=self.dealer.hands[0], hand_num=hand_num)

		if decision == 'p':
			player.split(card_1=self.deck.draw_card(), card_2=self.deck.draw_card(), hand_num=hand_num)
			return 'split'
		elif decision == 's':
			player.stand(hand_num=hand_num)
		elif decision == 'h':
			player.hit(card=self.deck.draw_card(), hand_num=hand_num)
		elif decision == 'dh':
			card = self.deck.draw_card()
			player.double_down(card, hand_num=hand_num)
			if not player.hands[hand_num].is_stood:
				player.hit(card=card, hand_num=hand_num)
		elif decision == 'ds':
			card = self.deck.draw_card()
			player.double_down(card, hand_num=hand_num)
			if not player.hands[hand_num].is_stood:
				player.stand(hand_num=hand_num)
		return

	def player_turn(self, player):
		""" Applies all decisions for player (multiple splits etc.) """
		if (len(player.hands) > 1) or (len(player.hands[0].cards) != 2):
			print(f"player_turn can only be applied to a player after dealing hand, not half way through. \n"
				  f"The player must have 2 cards and cannot have split")

		for hand_num, hand in enumerate(player.hands):
			while not hand.is_stood and not hand.is_bust:
				self._one_turn(player=player, hand_num=hand_num)
		return

	def dealer_turn(self):
		""" Applies dealer moves TODO - make dynamic based on table settings """
		while self.dealer.hands[0].value < self.dealer_stick:
			self.dealer.hit(self.deck.draw_card())

		self.dealer.stand()
		return

	def all_turns(self):
		""" Applies all turns to all players"""
		for player in self.players:
			self.player_turn(player)

		self.dealer_turn()
		return

	def _clear_one(self, player):
		""" Clears players cards, adding them to the deck, and recording the hand history """
		# Add players cards into the deck
		for h in player.hands:
			for c in h.cards:
				self.deck.add_card(c)

		hand_outcome = HandOutcome(player_hand=player.hands, dealer_hand=self.dealer.hands)
		for value in hand_outcome.hand_value:
			player.update_budget(value)
			self.table_balance += (0 - value)

		player.record_and_reset(self.dealer.hands)

		return

	def clear_round(self):
		""" Clear all players cards and record history. Also clear dealer cards """
		if any([True for player in self.players if len(player.hands[0].cards) < 2]):
			print(f"Players with no cards at the table, deal a round first.")
			return

		for p in self.players:
			if len(p.hands[0].cards) < 2:
				print(f"{p.name} not in this round, skipping...")
				continue
			self._clear_one(p)

		# Add dealers cards into the deck
		for c in self.dealer.hands[0].cards:
			self.deck.add_card(c)

		self.dealer = self.create_dealer()
		return

	def player_summary(self):
		""" prints out a summary of the players, their current hand and their cash balances """
		for num, player in enumerate(self.players):
			print(f"Player {num+1}: {player.name}")
			print(f"Player hand:")
			for hand in player.hands:
				print(f"cards: {hand.cards} value:{hand.value}  Stood:{hand.is_stood}")
			print(f"Dealer hand: {self.dealer.hands[0].cards} ({self.dealer.hands[0].value})")

			diff = player.balance - player.start_budget
			if diff > 0:
				budget_status = f"£{diff} up"
			elif diff < 0:
				budget_status = f"£{diff} down"
			else:
				budget_status = "no change"

			print(f"Balance: £{player.balance} ({budget_status})")
			print("------------------------")
		return