import json
import requests
import subprocess

from flask import Flask
from flask import render_template

app = Flask(__name__)
with open('config.json') as f:
    config = json.loads(f.read())


def shell_handler(command, **kwargs):
    return_code = subprocess.call(command, shell=True)
    return json.dumps(return_code == 0)


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
    data = {
        'tasks': config['tasks'],
        'title': config['title'],
    }
    return render_template('index.html', **data)


@app.route('/<task_id>')
def status(task_id):
    try:
        task = filter(lambda t: t['id'] == task_id, config['tasks'])[0]
    except IndexError:
        return 'This task does not exist', 404
    return get_handler[task['type']](**task)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
