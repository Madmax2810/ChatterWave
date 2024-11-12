from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
from vosk import Model, KaldiRecognizer
import wave
import subprocess
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'
socketio = SocketIO(app)

# Store sessions and users
users = {}

# Global variable for Vosk model
model = None

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')


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


### Speech-to-Text functionality ###

@app.route('/initialize', methods=['POST'])
def initialize():
    global model
    if model is None:
        model = Model(r"D:\Codes\SEM5project-Learn\eng-v8")  # Your Vosk model path
    return jsonify({'status': 'initialized'})

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part provided'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Ensure the 'uploads' directory exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    # Save the uploaded file
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    print(f"Audio file saved at {file_path}")

    # Convert WebM to WAV format using ffmpeg
    wav_path = file_path.replace('.webm', '.wav')
    try:
        subprocess.run(['ffmpeg', '-i', file_path, wav_path], check=True)
        print(f"Audio file converted to WAV: {wav_path}")
    except Exception as e:
        print(f"Error converting file: {e}")
        return jsonify({'error': 'Failed to convert audio file'}), 500

        # Initialize transcription result
    transcription_text = ""

    try:
        # Open the WAV file for reading and transcribe it
        with wave.open(wav_path, "rb") as wf:
            # Initialize KaldiRecognizer for each new transcription
            rec = KaldiRecognizer(model, wf.getframerate())
            rec.Reset()  # Reset the recognizer

            print("Starting transcription...")
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    result_dict = json.loads(result)
                    print(f"Intermediate result: {result_dict}")

            # Get the final transcription result
            final_result = rec.FinalResult()
            final_result_dict = json.loads(final_result)
            print(final_result_dict)
            transcription_text = final_result_dict.get('text', '').strip()
            print(f"Final transcription: {transcription_text}")

    except Exception as e:
        print(f"Error transcribing audio file: {e}")
        return jsonify({'error': 'Transcription failed'}), 500


    # Clean up: remove the audio files after transcription
    try:
        os.remove(r"D:\Codes\Chatapp-1\uploads\audio.wav")
        os.remove(r"D:\Codes\Chatapp-1\uploads\audio.webm")
        print(f"Deleted original and converted audio files: {file_path}, {wav_path}")
    except Exception as e:
        print(f"Error deleting files: {e}")

    # Return the transcription text to the frontend
    return jsonify({'text': transcription_text})

if __name__ == '__main__':
    app.run(debug=True)
