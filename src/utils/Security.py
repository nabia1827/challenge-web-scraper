from decouple import config
import hashlib
import base64
import hmac

SALT_SIZE = int(config('SALT_SIZE'))
KEY_SIZE = int(config('KEY_SIZE'))
ITERATIONS = int(config('ITERATIONS'))
HASH_ALGORITHM = config('HASH_ALGORITHM')
DELIMITER = config('DELIMITER')



def verify_password(hashed_password: str, provided_password: str) -> bool:
    try:
        salt_b64, hash_b64 = hashed_password.split(DELIMITER)
        salt = base64.b64decode(salt_b64)  
        stored_hash = base64.b64decode(hash_b64)

        new_hash = hashlib.pbkdf2_hmac(HASH_ALGORITHM, provided_password.encode("utf-8"), salt, ITERATIONS, KEY_SIZE)
        return hmac.compare_digest(stored_hash, new_hash)

    except Exception as ex:
        return False