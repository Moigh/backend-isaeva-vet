from app import app
from app.models import db, Pet, Visit, User
from datetime import datetime
import bcrypt


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


with app.app_context():
    # Чистим в правильном порядке (визиты → питомцы → юзеры)
    Visit.query.delete()
    Pet.query.delete()
    User.query.delete()
    db.session.commit()

    # ---------- Юзеры ----------
    users_data = [
        {"login": "ivan",   "name": "Иван",   "password": "pass123"},
        {"login": "petr",   "name": "Пётр",   "password": "pass123"},
        {"login": "anna",   "name": "Анна",   "password": "pass123"},
        {"login": "maria",  "name": "Мария",  "password": "pass123"},
        {"login": "admin", "name": "Admin", "password": "admin", "role": "admin"},
    ]
    users = []
    for u in users_data:
        user = User(
            login=u["login"],
            name=u["name"],
            role=u.get("role", "user"),
            password_hash=hash_password(u["password"]),
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()

    by_login = {u.login: u for u in users}

    # ---------- Питомцы ----------
    pets_data = [
        {"name": "Барсик",  "kind": "кот",    "age": 3, "login": "ivan"},
        {"name": "Мурка",   "kind": "кошка",  "age": 2, "login": "petr"},
        {"name": "Шарик",   "kind": "собака", "age": 5, "login": "anna"},
        {"name": "Рекс",    "kind": "собака", "age": 1, "login": "ivan"},
        {"name": "Снежок",  "kind": "кот",    "age": 4, "login": "maria"},
        {"name": "Бублик",  "kind": "кот",    "age": 6, "login": "anna"},
        {"name": "Тузик",   "kind": "собака", "age": 3, "login": "petr"},
        {"name": "Луна",    "kind": "кошка",  "age": 1, "login": "maria"},
        {"name": "Кеша",    "kind": "попугай","age": 2, "login": "ivan"},
        {"name": "Найда",   "kind": "собака", "age": 7, "login": "anna"},
    ]
    pets = []
    for p in pets_data:
        pet = Pet(
            name=p["name"],
            kind=p["kind"],
            age=p["age"],
            owner_id=by_login[p["login"]].id,
        )
        db.session.add(pet)
        pets.append(pet)
    db.session.commit()

    # ---------- Визиты ----------
    visits_data = [
        {"idx": 0, "date": datetime(2026, 9, 10, 10, 0),  "reason": "Осмотр",            "diagnosis": "Здоров"},
        {"idx": 0, "date": datetime(2026, 10, 5, 14, 30), "reason": "Прививка",          "diagnosis": "Вакцинирован"},
        {"idx": 0, "date": datetime(2026, 11, 12, 9, 0),  "reason": "Повторный осмотр",  "diagnosis": "Здоров"},
        {"idx": 1, "date": datetime(2026, 9, 15, 11, 0),  "reason": "Стерилизация",      "diagnosis": "Послеоперационный уход"},
        {"idx": 1, "date": datetime(2026, 10, 20, 16, 0), "reason": "Проверка швов",     "diagnosis": "Заживает"},
        {"idx": 2, "date": datetime(2026, 10, 1, 10, 0),  "reason": "Травма лапы",       "diagnosis": "Перелом"},
        {"idx": 2, "date": datetime(2026, 11, 5, 13, 0),  "reason": "Рентген",           "diagnosis": "Срастается"},
        {"idx": 3, "date": datetime(2026, 9, 25, 9, 30),  "reason": "Вакцинация",        "diagnosis": "Здоров"},
        {"idx": 3, "date": datetime(2026, 12, 1, 15, 0),  "reason": "Осмотр",            "diagnosis": "Здоров"},
        {"idx": 4, "date": datetime(2026, 8, 15, 12, 0),  "reason": "Кастрация",         "diagnosis": "Послеоперационный уход"},
        {"idx": 4, "date": datetime(2026, 10, 10, 10, 0), "reason": "Проверка",          "diagnosis": "Здоров"},
        {"idx": 4, "date": datetime(2026, 11, 20, 17, 0), "reason": "Прививка",          "diagnosis": "Вакцинирован"},
        {"idx": 5, "date": datetime(2026, 8, 5, 10, 0),   "reason": "Осмотр",            "diagnosis": "Здоров"},
        {"idx": 5, "date": datetime(2026, 9, 18, 12, 30), "reason": "Чистка зубов",      "diagnosis": "Здоров"},
        {"idx": 6, "date": datetime(2026, 9, 2, 9, 0),    "reason": "Аллергия",          "diagnosis": "Дерматит"},
        {"idx": 6, "date": datetime(2026, 10, 14, 11, 0), "reason": "Повторный осмотр",  "diagnosis": "Улучшение"},
        {"idx": 7, "date": datetime(2026, 10, 25, 14, 0), "reason": "Вакцинация",        "diagnosis": "Вакцинирован"},
        {"idx": 8, "date": datetime(2026, 11, 1, 10, 30), "reason": "Проверка клюва",    "diagnosis": "Здоров"},
        {"idx": 9, "date": datetime(2026, 8, 20, 13, 0),  "reason": "Старость",          "diagnosis": "Наблюдение"},
        {"idx": 9, "date": datetime(2026, 11, 15, 16, 0), "reason": "Осмотр",            "diagnosis": "Стабильно"},
    ]
    visits = [
        Visit(
            pet_id=pets[v["idx"]].id,
            date=v["date"],
            reason=v["reason"],
            diagnosis=v["diagnosis"],
        )
        for v in visits_data
    ]
    db.session.add_all(visits)
    db.session.commit()

    print(f"Сид готов: {len(users)} юзеров, {len(pets)} питомцев, {len(visits)} визитов")
    print("Логины: ivan/petr/anna/maria — пароль pass123")