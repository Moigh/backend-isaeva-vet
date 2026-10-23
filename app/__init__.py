from flask import Flask, request, g
from . import routes
import time
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.json.ensure_ascii = False


# Swagger UI
SWAGGER_URL = "/docs"
API_URL = "/openapi.json"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Ветклиника API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route("/openapi.json")
def serve_openapi():
    with open("openapi.json", "r", encoding="utf-8") as f:
        return f.read(), 200, {"Content-Type": "application/json"}


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