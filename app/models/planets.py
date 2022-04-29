from app import db

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    num_moons = db.Column(db.Integer)



# class Planet:
#     def __init__(self, id, name, description, num_moons):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.num_moons = num_moons

# planets = [
#     Planet(1, "Mercury", "first planet from sun", 0),
#     Planet(2, "Venus", "second planet from sun", 0),
#     Planet(3, "Earth", "third planet from sun", 1)
# ]