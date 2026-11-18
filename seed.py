from app import app
from app.models import db, Pet, Visit
from datetime import datetime

with app.app_context():
    Pet.query.delete()
    db.session.commit()

    pets_data = [
        {"name": "Барсик", "kind": "кот", "age": 3, "owner": "Иван"},
        {"name": "Мурка", "kind": "кошка", "age": 2, "owner": "Пётр"},
        {"name": "Шарик", "kind": "собака", "age": 5, "owner": "Анна"},
        {"name": "Рекс", "kind": "собака", "age": 1, "owner": "Иван"},
        {"name": "Снежок", "kind": "кот", "age": 4, "owner": "Мария"},
    ]
    pets = [Pet(**data) for data in pets_data]
    db.session.add_all(pets)
    db.session.commit()  

    visits_data = [
        {"pet_id": pets[0].id, "date": datetime(2026, 9, 10, 10, 0), "reason": "Осмотр", "diagnosis": "Здоров"},
        {"pet_id": pets[0].id, "date": datetime(2026, 10, 5, 14, 30), "reason": "Прививка", "diagnosis": "Вакцинирован"},
        {"pet_id": pets[0].id, "date": datetime(2026, 11, 12, 9, 0), "reason": "Повторный осмотр", "diagnosis": "Здоров"},

        {"pet_id": pets[1].id, "date": datetime(2026, 9, 15, 11, 0), "reason": "Стерилизация", "diagnosis": "Послеоперационный уход"},
        {"pet_id": pets[1].id, "date": datetime(2026, 10, 20, 16, 0), "reason": "Проверка швов", "diagnosis": "Заживает"},

        {"pet_id": pets[2].id, "date": datetime(2026, 10, 1, 10, 0), "reason": "Травма лапы", "diagnosis": "Перелом"},
        {"pet_id": pets[2].id, "date": datetime(2026, 11, 5, 13, 0), "reason": "Рентген", "diagnosis": "Срастается"},

        {"pet_id": pets[3].id, "date": datetime(2026, 9, 25, 9, 30), "reason": "Вакцинация", "diagnosis": "Здоров"},
        {"pet_id": pets[3].id, "date": datetime(2026, 12, 1, 15, 0), "reason": "Осмотр", "diagnosis": "Здоров"},

        {"pet_id": pets[4].id, "date": datetime(2026, 8, 15, 12, 0), "reason": "Кастрация", "diagnosis": "Послеоперационный уход"},
        {"pet_id": pets[4].id, "date": datetime(2026, 10, 10, 10, 0), "reason": "Проверка", "diagnosis": "Здоров"},
        {"pet_id": pets[4].id, "date": datetime(2026, 11, 20, 17, 0), "reason": "Прививка", "diagnosis": "Вакцинирован"},
    ]
    visits = [Visit(**data) for data in visits_data]
    db.session.add_all(visits)
    db.session.commit()