import datetime
from flask_jwt_extended import create_access_token
from src.repositories.ConfigTokenRepository import get_status_token, set_token

class VerifyTokenService:

    def verify_token(self, user_id, token):

        status = get_status_token(user_id, token)

        if status == 0:
            return {'message': "Error: Token is not registered. Unauthorized", 'success': False}
        
        elif status == 1:
            payload = {
                "user_id": str(user_id),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=3),
            }
            token = create_access_token(identity=str(user_id), additional_claims=payload)
            set_token(user_id,token)
            return {'token': token, 'success': True}
        
        elif status == 2:
            return {'token': token, 'success': True}
        
        else:
            return {'message': "Error: Token is not registered. Unauthorized", 'success': False}