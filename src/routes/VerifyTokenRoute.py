from flask import Blueprint, request, jsonify
from src.services.VerifyTokenService import VerifyTokenService

main = Blueprint('verify-token_blueprint', __name__)

@main.route('/verify-token', methods=['POST'])
def verify_token():
    try:
        data = request.get_json()
        user_id = data.get('userId')
        token = data.get('token')

        service = VerifyTokenService()
        response = service.verify_token(user_id, token)

        if response['success'] == False:
            return jsonify(response), 401

        return jsonify(response)
        
    except Exception as ex:
        return jsonify({'message': ex, 'success': False})
