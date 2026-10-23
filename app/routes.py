from.models import pets, Pet
from flask import jsonify, request

def validate_fields(data, partial):
    if not data:
        return {"error": "data is required", "field": None}
    if not isinstance(data, dict):
        return {"error": "invalid json", "field": None}
    # name обязательное(не для апдейт), строка, не пустое 
    if not partial or "name" in data:
        if not data.get("name") or not isinstance(data["name"], str):
            return {"error": "name must be a non-empty string", "field": "name"}
    # kind строка
    if "kind" in data:
        if not isinstance(data["kind"], str):
            return {"error": "kind must be a string", "field": "kind"}
    # age положительное число
    if "age" in data:
        if not isinstance(data["age"], int) or data["age"] < 0:
            return {"error": "age must be a non-negative integer", "field": "age"}
    # owner строка
    if "owner" in data:
        if not isinstance(data["owner"], str):
            return {"error": "owner must be a string", "field": "owner"}
    return None

def post_pet():
    data = request.get_json(silent=True)
    error = validate_fields(data, False)
    if error:
        return jsonify(error), 400
    pet = Pet(
        data["name"],
        data.get("kind"),
        data.get("age"),
        data.get("owner")
    )
    pets.append(pet)
    return jsonify(pet.to_dict()), 201

def health():
    return jsonify({"status": "ok"}), 200

def get_pets():
    return jsonify([p.to_dict() for p in pets]), 200

def get_pet(pet_id):
    pet = next((p for p in pets if p.id == pet_id), None)
    if pet:
        return jsonify(pet.to_dict()), 200
    return jsonify({'error': 'not found', "field": None}), 404

def update_pet(pet_id):
    data = request.get_json(silent=True)

    error = validate_fields(data, True)

    if error:
        return jsonify(error), 400

    pet = next((p for p in pets if p.id == pet_id), None)
    if not pet:
        return jsonify({"error": "not found", "field": None}), 404

    for field in ("name", "kind", "age", "owner"):
        if field in data:
            setattr(pet, field, data[field])

    return jsonify(pet.to_dict()), 200

def delete_pet(pet_id):
    pet = next((p for p in pets if p.id == pet_id), None)

    if not pet:
        return jsonify({"error": "not found", "field": None}), 404

    pets.remove(pet)

    return "", 204


