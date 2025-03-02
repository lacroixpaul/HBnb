#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True,
                          description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.Nested(amenity_model),
                             default=[], description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model),
                           default=[], description='List of reviews')
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        try:
            place_data = api.payload
            place = facade.create_place(place_data)
            return place.to_dict(), 201
        except ValueError as e:
            return {"message": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        try:
            places = facade.get_all_places()
            if not places:
                return [], 200
            return [place.to_dict() for place in places], 200
        except Exception as e:
            return {"message": str(e)}, 500


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)
            if not place:
                # Ajout d'une vérification
                return {"message": "Place not found"}, 404
            return place.to_dict(), 200
        except ValueError:
            return {"message": "Place not found"}, 404
        except Exception as e:
            return {"message": str(e)}, 500

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        if 'id' in place_data and place_data['id'] != place_id:
            return {"error": "Place ID cannot be modified"}, 400
        try:
            place = facade.get_place(place_id)
            if not place:
                return {"message": "Place not found"}, 404

            if not place_data:
                return {"message": "No data provided"}, 400

            if 'title' in place_data and not place_data['title'].strip():
                return {"message": "Title is required"}, 400

            updated_place = facade.update_place(place_id, place_data)
            return updated_place.to_dict(), 200
        except ValueError:
            return {"message": "Place not found"}, 404
        except Exception as e:
            return {"message": str(e)}, 400
