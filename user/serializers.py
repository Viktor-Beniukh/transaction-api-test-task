import string
import random

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext as _

from rest_framework import serializers

from transactions.serializers import TransactionListSerializer


class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
        )
        read_only_fields = ("id", "is_staff", "is_superuser",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        user = get_user_model().objects.create_user(
            **validated_data,
            is_staff=True,
            is_superuser=True,
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update the user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    transactions = TransactionListSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "transactions",
        )

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        password = self.generate_password()
        validated_data["password"] = make_password(password)
        user = get_user_model().objects.create_user(**validated_data)
        return user

    @staticmethod
    def generate_password(length=12):
        """Generate a random password"""
        characters = string.ascii_letters + string.digits + string.punctuation
        return "".join(random.choice(characters) for i in range(length))

    def update(self, instance, validated_data):
        """Update a user, but don't allow updating password"""
        validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        return user


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"), write_only=True, min_length=5, max_length=255)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"), username=username, password=password
            )

            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _("Must include 'username' and 'password'.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user

        return attrs
