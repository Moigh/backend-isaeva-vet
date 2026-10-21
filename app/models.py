class Pet:
    def __init__(self, name, kind, age, owner):
        self.id = next_id
        next_id += next_id
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