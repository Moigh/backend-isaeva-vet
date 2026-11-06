from.models import db, Pet, Visit
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
        name=data["name"],
        kind=data.get("kind"),
        age=data.get("age"),
        owner=data.get("owner")
    )
    db.session.add(pet)
    db.session.commit()
    return jsonify(pet.to_dict()), 201

def health():
    return jsonify({"status": "ok"}), 200

def get_pets():
    limit = request.args.get("limit", type=int)
    offset = request.args.get("offset", default=0, type=int)

    query = Pet.query

    for key, value in request.args.items():
        if key in ("name", "kind", "owner"):
            query = query.filter(getattr(Pet, key) == value)
        elif key == "age":
            try:
                query = query.filter(Pet.age == int(value))
            except ValueError:
                pass

    if offset:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)

    pets = query.all()
    return jsonify([p.to_dict() for p in pets]), 200

def get_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet:
        return jsonify(pet.to_dict()), 200
    return jsonify({'error': 'not found', "field": "id"}), 404

def update_pet(pet_id):
    data = request.get_json(silent=True)

    error = validate_fields(data, True)

    if error:
        return jsonify(error), 400

    pet = Pet.query.get(pet_id)
    if not pet:
        return jsonify({"error": "not found", "field": "id"}), 404

    for field in ("name", "kind", "age", "owner"):
        if field in data:
            setattr(pet, field, data[field])

    db.session.commit()

    return jsonify(pet.to_dict()), 200

def delete_pet(pet_id):
    pet = Pet.query.get(pet_id)

    if not pet:
        return jsonify({"error": "not found", "field": None}), 404

    db.session.delete(pet)
    db.session.commit()

    return "", 204


