from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.generics import get_object_or_404

from car.models import Car
from .models import User, Job, JobTitle


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "phone", "email"]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super(MyTokenObtainPairSerializer, self).__init__(*args, **kwargs)
        self.fields['userinput'] = serializers.CharField(required=False)
        self.fields['username'] = serializers.CharField(read_only=True, required=False)

    def auth_validate(self, attrs):
        # print(attrs)
        user_input = attrs.get('userinput')
        # print(user_input)
        authentication_kwargs = {
            self.username_field: user_input,
            'password': attrs['password']
        }
        print(authentication_kwargs)
        user = authenticate(**authentication_kwargs)
        if user is not None:
            self.user = user
        else:
            raise ValidationError(
                {"password": "Sorry, login or password you entered is incorrect. Please check and try again."}
            )

    def validate(self, attrs):
        self.auth_validate(attrs)
        data = self.user.tokens()
        return data

    def get_user(self, **kwargs):
        users = User.objects.filter(**kwargs)
        if not users.exists():
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                "no_active_account",
            )
        return users.first()


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance['user_id']
        user = get_object_or_404(User, id=user_id)
        update_last_login(None, user)
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", 'phone', "password"]

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_password(self, value):
        try:
            validate_password(value, self.instance)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))

        return value

    def validate(self, attrs):
        super(UserSerializer, self).validate(attrs)

        if attrs['username'].lower() == attrs['password'].lower():
            raise serializers.ValidationError("Username va parol bir xil bo'lmasligi kerak")

        if not any(char in "!@#$%^&*()_-+=<>?/[]{}|" for char in attrs['password']):
            raise serializers.ValidationError("Belgi iborat bo'lishi kerak")

        if not any(char.islower() for char in attrs['password']):
            raise serializers.ValidationError("Kichik harfdan iborat bo'lishi kerak")

        if sum(1 for char in attrs['password'] if char.isupper()) < 2:
            raise serializers.ValidationError("Parol kamida 2 ta katta harf bo'lishi kerak")

        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)


class JObSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["user", "company", 'job_title']

    def validate(self, attrs):
        user = attrs.get("user")
        compony = attrs.get("company")
        job_title = attrs.get("job_title")
        job = Job.objects.filter(user=user, company=compony, job_title=JobTitle.DIRECTOR.value)
        jobs = Job.objects.filter(user=user).first()
        car = Car.objects.filter(user=user)
        if job and job_title == JobTitle.DIRECTOR.value:
            raise ValidationError({"success": False, "message": "Bitta kompaniyaga bitta drektor bo'lishi kerak"})
        elif not car and job_title == JobTitle.DRIVER.value:
            raise ValidationError({"success": False, "message": "Sizda mashina mavjud emas!!"})
        elif jobs:
            if jobs.company != compony and jobs.job_title == JobTitle.DIRECTOR.value and JobTitle.GUARD.value == job_title:
                raise ValidationError({"success": False, "message": "Bitta kompaniyaga bitta drektor bo'lishi kerak"})
            else:
                return attrs
        else:
            return attrs
