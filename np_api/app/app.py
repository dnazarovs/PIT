from flask import Flask

from service.DataService import get_schedule_data

app = Flask(__name__)


@app.route('/schedule/<period>')
def get_schedule(period):
    schedule = get_schedule_data(period)
    return schedule


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
