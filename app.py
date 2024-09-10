from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.secret_key = 'supersecretkey'
socketio = SocketIO(app)

# Store sessions and users
users = {}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/chat', methods=['POST'])
def chat():
    username = request.form['username']
    session_key = request.form['session_key']

    if username and session_key:
        session['username'] = username
        session['session_key'] = session_key
        return render_template('chat.html', username=username, session_key=session_key)
    else:
        return redirect(url_for('login'))

@socketio.on('join')
def on_join(data):
    username = data['username']
    session_key = data['session_key']
    join_room(session_key)
    emit('message', {'msg': f"{username} has joined the chat"}, room=session_key)

@socketio.on('message')
def handle_message(data):
    session_key = data['session_key']
    message = data['msg']
    emit('message', {'msg': f"{session['username']}: {message}"}, room=session_key)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    session_key = data['session_key']
    leave_room(session_key)
    emit('message', {'msg': f"{username} has left the chat"}, room=session_key)


if __name__ == '__main__':
    socketio.run(app, debug=True)
