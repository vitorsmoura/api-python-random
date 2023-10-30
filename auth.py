from flask import abort

def authenticate(token, users):
    # Verifique se o token corresponde a um token armazenado na memória
    valid_tokens = [user['access_token'] for user in users.values() if 'access_token' in user]
    if token not in valid_tokens:
        abort(401, description="Token inválido")
