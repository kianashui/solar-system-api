from app import db
from app.models.planets import Planet
from flask import Blueprint, jsonify, abort, make_response, request

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

def validate_planet_id(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        abort(make_response({"error": f"{planet_id} is an invalid planet ID"}, 400))
    planets = Planet.query.all()
    for planet in planets:
        if planet.id == planet_id:
            return planet
    abort(make_response({"error": f"planet {planet_id} not found"}, 404))

@planets_bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()

    new_planet = Planet(
        name=request_body["name"],
        description=request_body["description"],
        num_moons=request_body["num_moons"]
    )

    db.session.add(new_planet)
    db.session.commit()

    #return {"id": f"Planet {new_planet.id} successfully created"}, 201
    # an alternative to the above return statement
    return make_response(f"Planet {new_planet.id} successfully created", 201)

@planets_bp.route("", methods=["GET"])
def show_planets():
    response = []
    planets = Planet.query.all()
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
    planet = validate_planet_id(planet_id)
    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "num_moons": planet.num_moons
        }