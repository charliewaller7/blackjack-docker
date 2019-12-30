from flask import Flask, request, render_template, redirect
import pandas as pd
from functions.functions import *
import requests
import json

app = Flask(__name__)

# index
@app.route('/')
def index():
    return render_template(r'index.html')

# /me    
@app.route("/results", methods=["GET", "POST"])
def results():

	if request.method == 'POST':

		number_of_players = request.form.get('number_of_players')
		number_of_hands = request.form.get('number_of_hands')

		payload = json.dumps({'number_of_players': int(number_of_players), 'number_of_hands': int(number_of_hands)})
		result = requests.post(url='http://backend:5001/run', data=payload)

		df = pd.DataFrame(result.json()['result'])
		df.index = df.index.map(int)
		df.sort_index(inplace=True)
		graph_html = get_html(df)

		return render_template(r'results.html', graph_html=graph_html, number_of_players=number_of_players, number_of_hands=number_of_hands)

	return redirect('/')


if __name__ == "__main__":
    app.run(port=5002, host='0.0.0.0')
