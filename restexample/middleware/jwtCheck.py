import jwt
from rest_framework.response import Response

from apiApp.models import User

class jwtCheck:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        token = request.headers.get('Authorization')
        
        if token == None:
            return Response({ 'success': False, 'message': 'Please provide a token'}, status=401)
        
        try:
            token = token.split(' ')[1]
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            
            request.user = payload
            
            return None
        except jwt.DecodeError:
            return Response({ 'success': False, 'message': 'Token is invalid'}, status=401)
        except jwt.ExpiredSignatureError:
            return Response({ 'success': False, 'message': 'Token has expired'}, status=401)
        except jwt.InvalidTokenError:
            return Response({ 'success': False, 'message': 'Invalid token'}, status=401)
        except User.DoesNotExist:
            return Response({ 'success': False, 'message': 'User does not exists'}, status=401)