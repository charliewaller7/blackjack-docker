""" History class to record history of a single hand based on the players hand and dealers hand """


class HandOutcome:

	def __init__(self, player_hand, dealer_hand):
		self.player_hand = player_hand
		self.dealer_hand = dealer_hand
		self.status = self._get_status()
		self.hand_value = self._get_hand_value()

	def _get_status(self):
		""" Returns the status of the hand, returning won, lost, blackjack or push"""
		status_list = []
		for hand in self.player_hand:
			if hand.value > 21:
				status_list.append('lost')
			elif hand.value == 21 \
					and len(hand.cards) == 2 \
					and not(self.dealer_hand[0].value == 21 and len(self.dealer_hand[0].cards) == 2):
				status_list.append('blackjack')
			elif self.dealer_hand[0].value > 21:
				status_list.append('won')
			elif hand.value > self.dealer_hand[0].value:
				status_list.append('won')
			elif hand.value == self.dealer_hand[0].value:
				status_list.append('push')
			else:
				status_list.append('lost')
		return status_list

	def _get_hand_value(self):
		""" Gets the financial value of the hand """
		value_list = []
		for index, hand in enumerate(self.player_hand):
			if self.status[index] == 'won':
				value_list.append(hand.bet)
			elif self.status[index] == 'blackjack':
				value_list.append(hand.bet * 1.5)
			elif self.status[index] == 'push':
				value_list.append(0)
			else:
				value_list.append(0-hand.bet)
		return value_list