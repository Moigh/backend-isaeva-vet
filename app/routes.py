import base64
import bcrypt
from models import db, Pet, Visit, User
from flask import jsonify, request
from datetime import datetime
from sqlalchemy import func

def validate(data):
    if not data:
        return {"error": "data is required", "field": None}
    if not isinstance(data, dict):
        return {"error": "invalid json", "field": None}
    return None

def validate_fields(data, partial, visit=False):
    error = validate(data)
    if not error == None:
        return error 
    # name обязательное(не для апдейт), строка, не пустое 
    if not visit:
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
        return None

def validate_user(data):
    error = validate(data)
    if error:
        return error, 400

    login = data.get("login")
    password = data.get("password")

    if not login or not isinstance(login, str):
        return {"error": "login must be a non-empty string", "field": "login"}, 400
    if not password or not isinstance(password, str):
        return {"error": "password must be a non-empty string", "field": "password"}, 400

    if User.query.filter_by(login=login).first():
        return {"error": "login already exists", "field": "login"}, 409

    return None, None
    
def get_current_user():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Basic "):
        return None
    try:
        decoded = base64.b64decode(auth[6:]).decode()
        login, password = decoded.split(":", 1)
    except Exception:
        return None
    user = User.query.filter_by(login=login).first()
    if not user:
        return None
    if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        return None
    return user


def post_pet():
    user = get_current_user()
    if not user:
        return jsonify({"error": "unauthorized", "field": None}), 401
    
    data = request.get_json(silent=True)
    error = validate_fields(data, False)
    if error:
        return jsonify(error), 400
    pet = Pet(
        name=data["name"],
        kind=data.get("kind"),
        age=data.get("age"),
        owner_id=user.id,
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

    q = request.args.get("q")
    if q:
        query = query.filter(Pet.name.ilike(f"%{q}%"))


    for key, value in request.args.items():
        if key in ("name", "kind"):
            query = query.filter(getattr(Pet, key) == value)
        elif key == "age":
            try:
                query = query.filter(Pet.age == int(value))
            except ValueError:
                pass
        elif key == "owner":
            query = query.join(User, Pet.owner_id == User.id).filter(User.login == value)

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
    user = get_current_user()
    if not user:
        return jsonify({"error": "unauthorized", "field": None}), 401

    pet = Pet.query.get(pet_id)
    if not pet:
        return jsonify({"error": "not found", "field": "id"}), 404
    if pet.owner_id != user.id:
        return jsonify({"error": "forbidden", "field": None}), 403
    
    data = request.get_json(silent=True)
    error = validate_fields(data, True)

    if error:
        return jsonify(error), 400
    
    for field in ("name", "kind", "age"):
        if field in data:
            setattr(pet, field, data[field])

    db.session.commit()

    return jsonify(pet.to_dict()), 200

def delete_pet(pet_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "unauthorized", "field": None}), 401
    
    pet = Pet.query.get(pet_id)
    if not pet:
        return jsonify({"error": "not found", "field": None}), 404
    if pet.owner_id != user.id:
        return jsonify({"error": "forbidden", "field": None}), 403

    db.session.delete(pet)
    db.session.commit()

    return "", 204


def get_visits(pet_id):
    pet = Pet.query.get(pet_id)
    if not pet:
        return jsonify({"error": "not found", "field": "id"}), 404
    return jsonify([v.to_dict() for v in pet.visits]), 200

def post_visit(pet_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "unauthorized", "field": None}), 401
    
    data = request.get_json(silent=True)
    
    error = validate_fields(data, True, True)
    if error:
        return jsonify(error), 400

    with db.session.begin():
        pet = Pet.query.get(pet_id)
        if not pet:
            return jsonify({"error": "not found", "field": "id"}), 404

        try:
            visit_date = datetime.fromisoformat(data["date"])
        except (ValueError, TypeError):
            return jsonify({"error": "date must be ISO format", "field": "date"}), 400

        # правило: нельзя два визита на одно время
        existing = Visit.query.filter_by(pet_id=pet_id, date=visit_date).first()
        if existing:
            return jsonify({
                "error": "Pet already has a visit at this time",
                "field": "date"
            }), 409

        visit = Visit(
            pet_id=pet_id,
            date=visit_date,
            reason=data.get("reason"),
            diagnosis=data.get("diagnosis"),
        )
        db.session.add(visit)
    
    return jsonify(visit.to_dict()), 201


def register():
    data = request.get_json(silent=True)
    error, code = validate_user(data)
    if error:
        return jsonify(error), code

    login = data["login"]
    password = data["password"]

    user = User(
        login=login,
        name=data.get("name") or login,
        password_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

def me():
    user = get_current_user()
    if not user:
        return jsonify({"error": "unauthorized", "field": None}), 401
    return jsonify(user.to_dict()), 200


def pets_stats():
    rows = (
        db.session.query(
            func.to_char(Visit.date, 'YYYY-MM').label('month'),
            func.count(Visit.id).label('visits_count')
        )
        .group_by(func.to_char(Visit.date, 'YYYY-MM'))
        .order_by(func.to_char(Visit.date, 'YYYY-MM'))
        .all()
    )
    return jsonify([
        {"month": month, "visits_count": count}
        for month, count in rows
    ]), 200
