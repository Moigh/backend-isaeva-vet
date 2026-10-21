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

def health():
    return jsonify({"status": "ok"}), 200

def get_pets():
    return jsonify([p.to_dict() for p in pets]), 200

def get_pet(pet_id):
    pet = next((p for p in pets if p["id"] == pet_id), None)
    if pet:
        return jsonify(pet.to_dict()), 200
    return jsonify({'error': 'comic not found'}), 404

def update_pet(pet_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "invalid json"}), 400

    pet = next((p for p in pets if p["id"] == pet_id), None)
    if not pet:
        return jsonify({"error": "not found"}), 404

    for field in ("name", "species", "age", "owner"):
        if field in data:
            pet[field] = data[field]

    return jsonify(pet), 200

def delete_pet(pet_id):
    pet = next((p for p in pets if p["id"] == pet_id), None)

    if not pet:
        return jsonify({"error": "not found"}), 404

    pets.remove(pet)

    return "", 204