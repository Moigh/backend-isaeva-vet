next_id = 1
pets = []
class Pet:
    def __init__(self, name, kind, age, owner):
        global next_id
        self.id = next_id
        next_id += 1
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
