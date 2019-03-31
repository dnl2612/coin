from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
import coin

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        try:
            make_proof = request.form['make_proof']
        except Exception:
            make_proof = False
        
        coin.write_coin(make_proof)

@app.route('/check', methods=['POST'])
def integrity():
    results = coin.check_coins_integrity()
    
    return results

@app.route('/mining', methods=['POST'])
def mining():
    if request.method == 'POST':
        max_index = int(coin.get_next_coin())

        for i in range(2, max_index):
            coin.proof_of_work(i)

if __name__ == '__main__':
    app.run(debug = True)
