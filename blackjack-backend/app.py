from flask import Flask, request, render_template
import requests
import json
from game_objects.table import *
from refs.functions import *
from refs.visualisation import *


app = Flask(__name__)

# index
@app.route('/')
def index():
    return "Blackjack backend endpoint"

# /me    
@app.route("/run", methods=["GET", "POST"])
def run():
	if request.method == "POST":
		r = request.data
		params = json.loads(r.decode('utf-8'))
		number_of_players = params['number_of_players']
		number_of_hands = params['number_of_hands']

		table = Table(dealer_stick=17, no_of_decks=1)

		for player_num in range(number_of_players):
			table.add_player(Player(name=f'Player {player_num+1}', budget=1000, card_counting=False))

		for i in range(number_of_hands):
			table.deck.shuffle()
			table.deal_round()
			table.all_turns()
			table.clear_round()

		result_table = metric_cum_balance_by_player(table)
		params['result'] = result_table.to_dict()

		return json.dumps(params)

	return "No data posted"

if __name__ == "__main__":
    app.run(port=5001, host='0.0.0.0')
