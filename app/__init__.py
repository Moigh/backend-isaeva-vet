from flask import Flask, request, g
from . import routes
import time

app = Flask(__name__)
app.json.ensure_ascii = False


@app.before_request
def start_timer():
    g.start_time = time.perf_counter()

@app.after_request
def log_print(response):
    duration = (time.perf_counter() - g.start_time) * 1000
    print(f"{request.method} {request.path} {response.status_code} {duration:.2f}ms")
    return response

# API
@app.route('/api/pets', methods=['POST'])
def post_pet():
    return routes.post_pet()

@app.route('/health', methods=['GET'])
def health():
    return routes.health()

@app.route('/api/pets', methods=['GET'])
def get_pets():
    return routes.get_pets()

@app.route("/api/pets/<int:pet_id>", methods=["GET"])
def get_pet(pet_id):
    return routes.get_pet(pet_id)

@app.route("/api/pets/<int:pet_id>", methods=["PATCH"])
def update_pet(pet_id):
    return routes.update_pet(pet_id)

@app.route("/api/pets/<int:pet_id>", methods=["DELETE"])
def delete_pet(pet_id):
    return routes.delete_pet(pet_id)