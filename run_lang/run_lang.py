from flask import Flask, request, jsonify, Blueprint
from run_lang.services.execute import execute, InvalidCode
from run_lang.services.describe import get_ubuntu
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define log message format
    datefmt='%Y-%m-%d %H:%M:%S'  # Define date/time format
)
logger = logging.getLogger(__name__)

bp = Blueprint("rce", __name__)

@bp.route('/run', methods=['POST'])
def playground():
    json_data = request.get_json()
    if not json_data:
        return {"message": "Data must be JSON"}, 400
    try:
        lang = json_data["lang"]
        code = json_data["code"]
        tests = json_data["tests"]
        func_name = json_data["func_name"]
    except KeyError:
        return {"status": "failed", "test_results": [], "message": "Key \"lang\" or \"code\" or \"tests\" are not present"}, 400

    try:
        result = execute(lang, code, func_name, tests)
        return jsonify(result), 200
    except InvalidCode as inv:
        return jsonify({
            "status": "failed",
            "message": "Could not run tests due to errors in the code"
        }), 200
    except Exception as e:
        logger.error(f'Error occured: {e}')
        return jsonify({"status": "failed", "test_results": [], "message": "Internal server error"}), 500



def create_app(*args, **kwargs):
    app = Flask(__name__)
    app.register_blueprint(bp)

    return app
