import datetime
import jwt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.decorators import decorator_from_middleware
from restexample.middleware.jwtCheck import jwtCheck

from . models import User
from.serializer import UserSerializer
    
@api_view(['POST'])
def register_user(request):
    data = request.data
    # check if data is empty
    if data.get('name') == None or data.get('email') == None or data.get('password') == None:
        message = { 'success': False, 'message': 'Please provide all the fields'}
        return Response(message, status=400)
    
    # get user with the same email
    user_isExits = User.objects.filter(email=data['email']).exists()
    if (user_isExits):
        return Response({ 'success': False, 'message': 'User already exists'}, status=400)
    
    if data.get('is_admin') != None:
        data.pop('is_admin')
        
    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    # create token
    payload = {
        'id': serializer.data['id'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow()
    }
    
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    
    response = Response()
    response.data = {
        'success': True,
        'data': {
            'id': serializer.data['id'],
            'name': serializer.data['name'],
            'email': serializer.data['email'],
            'token': f'Bearer {token}'
        }
    }
    
    return response


@api_view(['POST'])
def login(request):
    data = request.data
    if data.get('email') == None or data.get('password') == None:
        message = { 'success': False, 'message': 'Please provide all the fields'}
        return Response(message, status=400)
    
    user = User.objects.filter(email=data['email'])
    if (not user.exists()):
        return Response({ 'success': False, 'message': 'User does not exists'}, status=400)
    
    user = user.first()
    if not user.check_password(data['password']):
        return Response({ 'success': False, 'message': 'Invalid credentials'}, status=400)
    
    payload = {
        'id': user.id,
        'is_admin': user.is_admin,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow()
    }   
    
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    
    response = Response(status=200)
    response.data = {
        'success': True,
        'data': {
            'id': user.id,
            'token': f'Bearer {token}'
        }
    }
    
    return response


@api_view(['GET'])
@decorator_from_middleware(jwtCheck)
def get_all_users(request):
    if not request.user['is_admin']:
        return Response({ 'success': False, 'message': 'You are not admin!'}, status=400)
        
    users = User.objects.all().values('id', 'name', 'email', 'is_admin')
        
    response = Response(status=200)
    response.data = {
        'success': True,
        'data': users
    }

    return response
    
@api_view(['POST'])
@decorator_from_middleware(jwtCheck)
def create_user(request):
    if not request.user['is_admin']:
        return Response({ 'success': False, 'message': 'You are not admin!'}, status=400)
    
    data = request.data
    if data.get('name') == None or data.get('email') == None or data.get('password') == None or data.get('is_admin') == None:
        message = { 'success': False, 'message': 'Please provide all the fields'}
        return Response(message, status=400)
    
    user_isExits = User.objects.filter(email=data['email']).exists()
    if user_isExits:
        return Response({ 'success': False, 'message': 'User already exists'}, status=400)
        
    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    response = Response(status=200)
    response.data = {
        'success': True,
        'message': 'User created successfully',
        'data': {
            'id': serializer.data['id'],
            'name': serializer.data['name'],
            'email': serializer.data['email'],
            'is_admin': serializer.data['is_admin']
        }
    }

    return response

@api_view(['GET', 'PUT', 'DELETE'])
@decorator_from_middleware(jwtCheck)
def user_management(request, id):
    if not request.user['is_admin']:
        return Response({ 'success': False, 'message': 'You are not admin'}, status=400)
    
    if not id:
        return Response({ 'success': False, 'message': 'Please provide user id'}, status=400)
    
    user = User.objects.filter(id=id)
    if not user.exists():
        return Response({ 'success': False, 'message': 'User does not exists'}, status=400)
    
    if request.method == 'GET':
        user = user.values('id', 'name', 'email', 'is_admin').first()
    
        response = Response(status=200)
        response.data = {
            'success': True,
            'data': user
        }
        
        return response
    elif request.method == 'PUT':
        data = request.data
        searilizer = UserSerializer(user.first(), data=data)
        searilizer.is_valid(raise_exception=True)
        searilizer.update(user.first(), data)

        response = Response(status=200)
        response.data = {
            'success': True,
            'message': 'User updated successfully',
            'data': searilizer.data
        }
        
        return response
    elif request.method == 'DELETE':
        user.delete()
        
        response = Response(status=200)
        response.data = {
            'success': True,
            'message': 'User deleted successfully'
        }
        return response
    