import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, f'{BASE_DIR}')

from datetime import datetime

import pytz
from flask import Flask, jsonify, make_response, request, render_template, redirect

from BuyingModule.celery_task import receive_task
from DaoModule.Dao import Dao

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        try:
            login = request.form['login']
            password = request.form['password']
            to_name = request.form['to_name']
            drops_str = request.form['description'].strip().split(",")
            drops = [int(x) for x in drops_str]
            print(login, password, drops)
            send_to_celery(login, password, drops, to_name)
            return render_template('success.html')
        except Exception as err:
            return render_template('error.html', error=err)
    return render_template('main.html')

@app.route('/historical-data/', methods=['GET', 'POST'])
def get_historical_data():
    if request.method == "POST":
        drop_id = request.form['drop_id']
        if int(drop_id) < 0:
            return render_template('error.html', error='Drop ID should be bigger than zero')
        return redirect(f"/historical-data/{drop_id}", code=302)
    return render_template('historical.html')

@app.route('/historical-data/<int:drop_id>', methods=['GET'])
def get_historical_data_id(drop_id):
    labels, values = Dao.get_clean_historical_data(drop_id)
    return render_template('graph.html', labels=labels, values=values, drop_id=drop_id)


def send_to_celery(login, password, drops, to_name):
    receive_task.apply_async(eta=datetime.now(pytz.utc),
                        kwargs={
                            "login": login,
                            "password": password,
                            "drops": drops,
                            "to_name": to_name,
                        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run(host='0.0.0.0', port=8080, use_reloader=False)