import json
from threading import Thread, Event

from bson import json_util
from flask import Flask, render_template, request
from flask_socketio import SocketIO

from src.models.spot import Spot
from src.common.database import Database

app = Flask(__name__)
app.config.from_object('src.config')
# socketio = SocketIO(app, async_mode=None, logger=True)
socketio = SocketIO(app, async_mode=None, logger=True,cors_allowed_origins='*')

Database.initialize()

changed = True
thread = Thread()
thread_stop_event = Event()


# ne = [114.221011, 22.693566]
# sw = [114.215621, 22.691066]


# @app.before_first_request
# def init_db():
#     Database.initialize()
#     print("database initializing...")


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


# @socketio.on('clear', namespace='/data')
# def clear_db(msg):
#     print('removing data')
#     Database.remove('spots', {})
#     socketio.sleep(2)
#     socketio.emit("clear_map", "clear all data", namespace='/map')


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

# @socketio.on('bounds', namespace="/test")
# def get_bounds(msg):
#     result = json.loads(msg)
#     global ne, sw
#     ne = [result['He'], result['Vd']]
#     sw = [result['Le'], result['Xd']]

# def spots_to_client():
#     """
#     Generate a random number every 1 second and emit to a socketio instance (broadcast)
#     Ideally to be run in a separate thread?
#     """
#     # infinite loop of magical random numbers
#     print("Sending spots to client")
#     global changed
#     while True:
#         if not thread_stop_event.isSet() and changed:
#             socketio.emit('bounds', namespace="/test")
#             global ne, sw
#             print("{}:{}".format(ne, sw))
#             spots = Database.find_range(sw, ne)
#             # results_json = json.dumps(list(spots), default=json_util.default)
#
#             # socketio.emit('json', results_json, namespace='/test')
#             for spot in spots:
#                 print(spot)
#             changed = False
#
#
# @socketio.on('connect', namespace='/test')
# def test_connect():
#     # need visibility of the global thread object
#     global thread, changed
#     changed = True
#     print('Client connected')
#
#     # Start the random number generator thread only if the thread has not been started before.
#     if not thread.isAlive():
#         print("Starting Thread")
#         thread = socketio.start_background_task(spots_to_client())
