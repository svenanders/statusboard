import json
import requests

from flask import Flask
from flask import render_template

app = Flask(__name__)
config = {}


def shell_handler(command, **kwargs):
    return json.dumps(False)


def http_handler(address, **kwargs):
    try:
        r = requests.get(address)
    except requests.exceptions.RequestException:
        return json.dumps(False)
    return json.dumps(r.status_code == 200)


get_handler = {
    'http': http_handler,
    'shell': shell_handler,
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<task_id>')
def status(task_id):
    try:
        task = filter(lambda t: t['id'] == task_id, config['tasks'])[0]
    except IndexError:
        return 'This task does not exist', 404
    return get_handler[task['type']](**task)


if __name__ == '__main__':
    with open('example.json') as f:
        config = json.loads(f.read())
    app.run(debug=True, host='0.0.0.0')