from.models import pets, Pet
from flask import jsonify, request

def post_pet():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "data is required"}), 400
    pet = {
        "id": 1,
        "name": data["name"],
        "species": data.get("species"),
        "age": data.get("age"),
        "owner": data.get("owner"),
    }
    pets.append(pet)
    return jsonify(pet), 201