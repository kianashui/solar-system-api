from attr import validate
from app import db
from app.models.planets import Planet
from flask import Blueprint, jsonify, abort, make_response, request

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

def validate_planet_id(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        abort(make_response({"error": f"{planet_id} is an invalid planet ID"}, 400))
    
    planet = Planet.query.get(planet_id)

    if not planet:
        abort(make_response({"error": f"planet {planet_id} not found"}, 404))
    
    return planet

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
    name_query = request.args.get("name")
    
    if name_query:
        planets = Planet.query.filter_by(name=name_query)
    else:
        planets = Planet.query.all()

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
    planet = validate_planet_id(planet_id)
    
    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "num_moons": planet.num_moons
        }

@planets_bp.route("/<planet_id>", methods=["PUT"])
def replace_planet(planet_id):
    planet = validate_planet_id(planet_id)

    request_body = request.get_json()

    if "name" not in request_body or \
        "description" not in request_body or \
        "num_moons" not in request_body:
        return jsonify({'error': f'Request must include name, description, and num_moons.'}), 400

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.num_moons = request_body["num_moons"]

    db.session.commit()

    return jsonify({'msg': f"Successfully replaced planet with id {planet_id}"})


@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_planet_id(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return jsonify({'msg': f'Successfully deleted planet with id {planet_id}'})