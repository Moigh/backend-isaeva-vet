from flask import Flask
from . import routes

app = Flask(__name__)

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