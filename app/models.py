class Pet:
    def __init__(self, id, name, kind, age, owner):
        self.id = id
        self.name = name
        self.kind = kind
        self.age = age
        self.owner = owner

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "kind": self.kind,
            "age": self.age,
            "owner": self.owner,
        }

pets = []
next_id = 1