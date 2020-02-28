import json
from bson import json_util
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from src.models.spot import Spot
from src.common.database import Database

app = Flask(__name__)
app.config.from_object('src.config')
socketio = SocketIO(app, async_mode=None, cors_allowed_origins='*')
Database.initialize()


@app.route('/')
def hello_world():
    return render_template('home.jinja2')


@app.route('/data')
def get_data():
    return render_template('web_data.jinja2')


@app.route('/web_data', methods=['POST'])
def receive_data():
    """
    restful api for uploading data from web,
    once msg received,
        1. save spots to mongodb
        2. switch thread stop event to False
    :return:
    """
    spots_str = request.form['data']
    spots_list = json.loads(spots_str)

    for spot in list(spots_list):
        lng, lat = spot[0], spot[1]
        spot = Spot(loc=[lng, lat])
        spot.save_to_mongo()
    socketio.emit("updates", "data needs updates", namespace='/map')

    return render_template('web_data.jinja2')


@app.route('/clear', methods=['POST'])
def clear_db():
    print('removing data')
    Database.remove('spots', {})
    socketio.emit("clear_map", "clear all data", namespace='/map')
    return render_template('web_data.jinja2')


@socketio.on('get_spots', namespace='/map')
def get_posts(msg):
    result = json.loads(msg)
    ne = [result['He'], result['Vd']]
    sw = [result['Le'], result['Xd']]
    spots = Database.find_range(sw, ne)

    results_json = json.dumps(list(spots), default=json_util.default)
    socketio.emit('get_spots', results_json, namespace='/map')
    print('{}:{}'.format(ne, sw))
    print('spots: {}'.format(spots))
