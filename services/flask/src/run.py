from src.common.database import Database
from src.app import app, socketio

if __name__ == '__main__':
    Database.initialize()
    socketio.run(app, debug=app.config['DEBUG'], port=app.config['PORT'])
