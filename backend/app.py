from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/http-call")
def http_call():
    """return JSON with string data as the value"""
    data = {'data': 'this is data'}
    return jsonify(data)

@socketio.on('connect')
def connected():
    print(request.sid)
    print("Client is connected")
    emit("connect", {
        "data": f"id:{request.sid} is connected"
    })

@socketio.on('disconnect')
def disconnected():
    print("User disconnected")
    emit("disconnect", f"user {request.sid} has been disconnected", broadcast=True)

@socketio.on('data')
def handle_message(data):
    print('Data from the front end:', str(data))
    emit("data", {'data': data, 'id': request.sid}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5001)
