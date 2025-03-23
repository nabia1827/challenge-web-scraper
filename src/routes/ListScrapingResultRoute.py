from flask import Blueprint, request, jsonify
from src.services.ListScrapingResultService import ListScrapingResultService
from config import limiter
from flask_jwt_extended import jwt_required

main = Blueprint('list-scrap-result_blueprint', __name__)

@main.route('/list-scrap-result', methods=['GET'])
@jwt_required()
@limiter.limit("20 per minute", error_message="You have reached the limit requests per minute")
def list_scrap_result():
    try:
        input = request.args.get('legal_name', '')
        source_id = request.args.get('source_id', '')
        
        service = ListScrapingResultService(input)
        response = service.get_scrap_from_source(source_id)

        if response['success'] == False:
            return jsonify(response), 404

        return jsonify(response)
        
    except Exception as ex:
        return jsonify({'message': ex, 'success': False})
