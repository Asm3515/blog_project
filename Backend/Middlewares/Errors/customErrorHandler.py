from flask import Flask, jsonify

class CustomError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

app = Flask(__name__)

@app.errorhandler(CustomError)
def handle_custom_error(error):
    response = {
        'success': False,
        'error': error.message
    }
    return jsonify(response), error.status_code

@app.errorhandler(404)
def handle_not_found_error(error):
    response = {
        'success': False,
        'error': 'Not Found'
    }
    return jsonify(response), 404

@app.errorhandler(500)
def handle_internal_server_error(error):
    response = {
        'success': False,
        'error': 'Internal Server Error'
    }
    return jsonify(response), 500

@app.route('/example')
def example_route():
    # Simulate a CustomError
    raise CustomError('Example CustomError', 404)

if __name__ == '__main__':
    app.run(debug=True)
