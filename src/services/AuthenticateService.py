from src.repositories.ConfigTokenRepository import set_token
from src.utils.Security import verify_password
from flask_jwt_extended import create_access_token

from src.repositories.ConfigUserRepository import get_user
from src.utils.Security import verify_password
import datetime

class AuthenticateService:
    @classmethod
    def generate_token(self, username,password):
        user = get_user(username)
        hashed_password= user[1]
        user_id= user[0]

        if not hashed_password or not verify_password(hashed_password,password):
            return {"message": "Credenciales inválidas", 'success': False}
        
        payload = {
            "user_id": str(user_id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=3),
        }
        token = create_access_token(identity=username, additional_claims=payload)

        set_token(user_id,token)
        
        return {"token": token, 'success': True}