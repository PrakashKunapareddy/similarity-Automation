from urllib import request
from flask import jsonify

import json

from ChatGPT4omini import analyze_nli_with_4omini

# Flask setup
app = Flask(__name__)


@app.route('/analyze_nli', methods=['POST'])
def analyze_nli():
    # Get JSON data from the request
    data = request.get_json()

    # Check if both 'expected' and 'actual' are present
    if 'expected' not in data or 'actual' not in data:
        return jsonify({"error": "Both 'expected' and 'actual' fields are required."}), 400

    expected = data['expected']
    actual = data['actual']

    # Call the analyze function
    result = analyze_nli_with_4omini(expected, actual)

    if "error" in result:
        return jsonify(result), 500

    # Return the result as JSON
    return jsonify(result), 200


# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)