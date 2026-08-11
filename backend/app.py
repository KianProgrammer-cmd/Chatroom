from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit, join_room
from database import init_db, save_message, get_messages
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "chatroom-secret-key"
)

socketio = SocketIO(
    app,
    cors_allowed_origins="*"
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:filename>")
def frontend(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@socketio.on("connect")
def handle_connect():
    print("Client connected:", request.sid)


@socketio.on("join")
def handle_join(data):
    username = data.get("username", "کاربر")
    room = data.get("room", "main")

    join_room(room)

    print(f"{username} joined room: {room}")

    messages = get_messages(room)

    for message in messages:
        emit(
            "message",
            {
                "username": message["username"],
                "message": message["message"]
            },
            to=request.sid
        )


@socketio.on("send_message")
def handle_message(data):
    username = data.get("username", "کاربر")
    message = data.get("message", "").strip()
    room = data.get("room", "main")

    if not message:
        return

    print(f"MESSAGE | {username} | {room} | {message}")

    save_message(username, message, room)

    socketio.emit(
        "message",
        {
            "username": username,
            "message": message
        },
        to=room
    )


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected:", request.sid)


init_db()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    socketio.run(
        app,
        host="0.0.0.0",
        port=port,
        debug=False
    )