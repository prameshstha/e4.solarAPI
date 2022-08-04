# to override the model of custom Token table
from rest_framework.authentication import TokenAuthentication, BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from accounts.models import InstallerToken, InstallerUser
from django.utils.translation import gettext_lazy as _


class InstallerTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # secret_token = request.META.get('HTTP_AUTHORIZATION')
        auth = get_authorization_header(request).split()
        modal = InstallerToken
        # print('auth', auth, not auth, auth[0].lower(), self.keyword.lower().encode())
        # print(self.keyword.lower())

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            msg = 'Authentication credentials were not provided.'
            raise AuthenticationFailed(msg)
            # return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
            t1 = auth[0].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(token, t1)

    def authenticate_credentials(self, key, t1):
        model = InstallerToken
        # if t1 != 'pramesh':
        #     print('not equal pramesh')
        #     raise AuthenticationFailed('Invalid token type')
        # print('key', key)
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted.')

        return token.user, token

    def authenticate_header(self, request):
        return self.keyword

        # if not secret_token:
        #     raise AuthenticationFailed('Unauthorized')
        # else:
        #     print(secret_token.length())
        #     key = secret_token.split()[1]
        #     print(key)
        #
        # try:
        #     ua = InstallerToken.objects.get(key=key)
        #     print(ua)
        # except InstallerToken.DoesNotExist:
        #     raise AuthenticationFailed('Unauthorized')
        #
        # return (ua, None)
    # model = InstallerToken
