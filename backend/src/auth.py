from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

import json

AUTH0_DOMAIN = 'dev-REPLACEME.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'com.auth0tutorial.exams'

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def requires_role(required_role):
    def decorator(f):
        def wrapper(**args):
            token = get_token_auth_header()
            unverified_claims = jwt.get_unverified_claims(token)
            
            if unverified_claims.get('https://online-exams.com/roles'):
                roles = unverified_claims['https://online-exams.com/roles']
                for role in roles:
                    if role == required_role:
                        return f(**args)
                        
            raise AuthError({
                'code': 'insuficient_roles',
                'description': 'You do now have the roles needed to preform this operation.'
            }, 401)
     
        return wrapper
        
    return decorator    
    
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)
        
    parts = auth.split()
    
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)
        
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)
        
    token = parts[1]
    
    return token
    
def requires_auth(f):
    
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e'],
                }
        if rsa_key:
            print(token)
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer='https://' + AUTH0_DOMAIN + '/'
                )
            except jwt.JWTClaimsError:
                raise AuthError({
                    'code': 'invalid_claims',
                    'description': 'Incorrect claims. Please check the audience and issuer.'
                }, 401)
            except Exception:
                raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token.'
                }, 400)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
            
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.'
        }, 400)
        
        
    return decorated













