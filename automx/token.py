from datetime import datetime
import jwt
from decouple import config

jwt_secret = config("JWT_SECRET_KEY")
# print(jwt_secret)


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            "iat": datetime.datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, jwt_secret, algorithm="HS256")
    except Exception as e:
        return e


@staticmethod
def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, jwt_secret)
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return "Signature expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."
