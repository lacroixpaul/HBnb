from flask_restx import Namespace, Resource, fields
from app.services import facade
import uuid

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        try:
            if not amenity_data.get("name") or not amenity_data["name"].strip():
                return {'error': 'Name must be a non-empty string.'}, 400

            existing_amenity = next((a for a in facade.get_all_amenities()
                                    if a.name.lower() == amenity_data['name'].lower()), None)
            if existing_amenity:
                return {'error': 'Amenity already exists.'}, 400

            new_amenity = facade.create_amenity(amenity_data)

            return {'id': new_amenity.id, 'name': new_amenity.name}, 201

        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': a.id, 'name': a.name} for a in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid amenity ID format')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            uuid.UUID(amenity_id)
        except ValueError:
            return {'error': 'Invalid amenity ID format'}, 400

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload
        try:
            uuid.UUID(amenity_id)
        except ValueError:
            return {'error': 'Invalid amenity ID format'}, 400

        if not amenity_data.get("name") or not amenity_data["name"].strip():
            return {'error': 'Name must be a non-empty string.'}, 400

        updated_amenity = facade.update_amenity(amenity_id, amenity_data)

        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404

        return {'message': 'Amenity updated successfully', 'id': updated_amenity.id, 'name': updated_amenity.name}, 200
