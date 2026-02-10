import jwt
import datetime

SECRET_KEY = "your-jwt-secret"


def generate_token(email, role):
    """
    Generate a JWT token for the logged-in user

    """
    payload = {
        "email": email,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token):
    """
    Decode JWT token,return user's info if valid

    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token expiré. Veuillez vous reconnecter.")
    except jwt.InvalidTokenError:
        print("Token invalide.")
    return None


def load_token():
    """
       Load the saved authentication token from the .token file.

    Returns
    -------
    dict or None
        The decoded token payload if the .token file exists and the token
        can be decoded, otherwise None if no token file is found.

    """
    try:
        with open(".token", "r") as f:
            token = f.read()
            return decode_token(token)
    except FileNotFoundError:
        print("Aucun utilisateur connecté.")
        return None
