
from flask_cors import CORS
from flask import Flask, request, jsonify
from generate import output_lyrics  # Import your lyrics generation function

app = Flask(__name__)
CORS(app)
@app.route('/generate-lyrics', methods=['POST'])  # Use POST method
def generate_lyrics_endpoint():
    lyrics = output_lyrics()  # Call your lyrics generation function with appropriate params
    return jsonify({'lyrics': lyrics})

if __name__ == '__main__':
    app.run()
