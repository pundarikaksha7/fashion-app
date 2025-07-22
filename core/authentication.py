from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from firebase_admin import auth
from django.contrib.auth.models import User

class IsFirebaseAuthenticated(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            token_type, id_token = auth_header.split(' ')
            if token_type.lower() != 'bearer':
                raise AuthenticationFailed('Invalid token type')

            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token.get('uid')
            email = decoded_token.get('email')

            user, _ = User.objects.get_or_create(email=email, defaults={
                'username': email.split('@')[0]
            })
            return (user, None)

        except Exception as e:
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')