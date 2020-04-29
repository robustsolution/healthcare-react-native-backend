from flask import Flask, jsonify
from mobile_api.mobile_api import mobile_api
from user_api.user_api import user_api
from photos.photos_api import photos_api
from admin_api.admin_api import admin_api
from web_errors import WebError
from config import FLASK_DEBUG, FLASK_DEBUG_PORT
import startup_tasks


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(mobile_api)
app.register_blueprint(user_api)
app.register_blueprint(photos_api)
app.register_blueprint(admin_api)


@app.route('/')
def hello_world():
    return jsonify({'message': 'Welcome to the Hikma Health backend.',
                    'status': 'OK'})


@app.errorhandler(WebError)
def handle_web_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(404)
def page_not_found(_err):
    response = jsonify({'message': 'Endpoint not found.'})
    response.status_code = 404
    return response


@app.errorhandler(405)
def method_not_found(_err):
    response = jsonify({'message': 'Method not found.'})
    response.status_code = 405
    return response


@app.errorhandler(500)
def internal_server_error(_err):
    response = jsonify({'message': 'Internal Server Error'})
    response.status_code = 500
    return response


if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=str(FLASK_DEBUG_PORT))
