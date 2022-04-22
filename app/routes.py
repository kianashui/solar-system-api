from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, num_moons):
        self.id = id
        self.name = name
        self.description = description
        self.num_moons = num_moons

planets = [
    Planet(1, "Mercury", "first planet from sun", 0),
    Planet(2, "Venus", "second planet from sun", 0),
    Planet(3, "Earth", "third planet from sun", 1)
]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["GET"])
def show_planets():
    response = []
    for planet in planets:
        response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "num_moons": planet.num_moons
            }
        )
    return jsonify(response)

@planets_bp.route("/<planet_id>", methods=["GET"])
def show_requested_planet(planet_id):
    planet_id = int(planet_id)
    
    for planet in planets:
        if planet.id == planet_id:
            response = {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "num_moons": planet.num_moons
                }
            return jsonify(response)
    
    not_found_response_body = {"error": "planet not found"}
    return jsonify(not_found_response_body), 404

