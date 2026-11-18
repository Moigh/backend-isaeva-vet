from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    kind = db.Column(db.String(50))
    age = db.Column(db.Integer)
    owner = db.Column(db.String(100))

    visits = db.relationship("Visit", backref="pet", lazy=True, cascade='all, delete-orphan', passive_deletes=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "kind": self.kind,
            "age": self.age,
            "owner": self.owner,
        }

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(200))
    diagnosis = db.Column(db.String(200))

    __table_args__ = (
        db.Index('ix_visit_pet_id', 'pet_id'),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "pet_id": self.pet_id,
            "date": self.date.isoformat() if self.date else None,
            "reason": self.reason,
            "diagnosis": self.diagnosis,
        }