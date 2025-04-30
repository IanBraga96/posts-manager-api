from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth
from functools import wraps

def firebase_auth_middleware(view_func):
    @wraps(view_func)
    def wrapped_view(view_instance, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response(
                {"detail": "No token provided"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        token = auth_header.split(' ')[1]
        
        try:
            decoded_token = auth.verify_id_token(token)
            request.user_id = decoded_token['uid']
            
            user = auth.get_user(request.user_id)
            request.user = user
            
            return view_func(view_instance, request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"detail": "Invalid or expired token"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
    return wrapped_view