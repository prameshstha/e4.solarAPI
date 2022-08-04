from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from accounts.models import InstallerUser
from company.models import Company


class InstallerUserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = InstallerUser
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'city']

    def get_role(self, instance):
        # print('is_admin', instance, self.context.get('view').kwargs.get('company_id'))
        company_id = self.context.get('view').kwargs.get('company_id')
        company = Company.objects.get(id=company_id)
        if instance in company.company_admin.all():
            return 'Admin'
        else:
            return 'User'


class RegistrationInstallerUserSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = InstallerUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        password = self.validated_data['password']
        account = InstallerUser(email=self.validated_data['email'], first_name=self.validated_data['first_name'],
                                last_name=self.validated_data['last_name'],
                                street=self.validated_data['street'], city=self.validated_data['city'],
                                postcode=self.validated_data['postcode'],
                                state=self.validated_data['state'], country=self.validated_data['country'],
                                phone=self.validated_data['phone'])

        # account = User(email=self.validated_data['email'],
        account.set_password(password)
        account.save()
        return account


class ChangePasswordSerializer(serializers.Serializer):
    model = InstallerUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class InstallerEmailSerializer(serializers.Serializer):
    """
       Reset Password Email Request Serializer.
       """
    email = serializers.EmailField()

    class Meta:
        fields = ("email",)


class ResetPasswordSerializer(serializers.Serializer):
    """
    Reset Password Serializer.
    """

    password = serializers.CharField(
        write_only=True,
        min_length=1,
    )
    token = serializers.CharField(
        write_only=True,
        min_length=1,
    )
    pk = serializers.CharField(
        write_only=True,
        min_length=1,
    )

    class Meta:
        field = ["password", "token", 'pk']

    def validate(self, data):
        """
        Verify token and encoded_pk and then set new password.
        """
        password = data.get("password")
        token = data.get("token")
        encoded_pk = data.get("pk")

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data.")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = InstallerUser.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")

        user.set_password(password)
        user.save()
        return data
