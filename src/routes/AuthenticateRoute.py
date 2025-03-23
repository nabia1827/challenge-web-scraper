from flask import Blueprint, request, jsonify
from src.services.AuthenticateService import AuthenticateService

main = Blueprint('authenticate_blueprint', __name__)

@main.route('/authenticate', methods=['POST'])
def authenticate():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        service = AuthenticateService()
        response = service.generate_token(username,password)

        if response['success'] == False:
            return jsonify(response), 404

        return jsonify(response)
        
    except Exception as ex:
        return jsonify({'message': ex, 'success': False})
