from rest_framework import serializers
from .models import Person


def clean_email(value):
    """
    We can use this function as a validator
    """
    if "admin" in value:
        raise serializers.ValidationError("admin can not be in your email")


class PersonSerilizer(serializers.Serializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, validators=[clean_email])
    # Because we mention write_only for password filed in PersonSerlizer, it would not show password in Response.data
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_name(self, value):
        """
        Field Level Validation
        """
        if value == "admin":
            raise serializers.ValidationError("Username cannot be admin")
        return value

    def validate(self, data):
        """
        Object Level Validation,
        First field validation will be executed, and if there was no error,
        then object-level validation will be executes
        """
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords should match")
        return data


class PersonModelSerilizer(serializers.ModelSerializer):
    """
    1) You can mention below line for password field, so it will not show
    password because of property of write_only in it:

         password = serializers.CharField(required=True, write_only=True)

    2) or you can mention it like below in class Meta:
        class Meta:
            model = Person
            fields = ("name", "email", "password", "password2")

            extra_kwargs = {
                # "password": {"write_only": True},
            }
    """

    # password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Person
        fields = ("name", "email", "password", "password2")
        """
        Please keep in mind that, if the field has already been explicitly 
        declared on the serializer class, then the extra_kwargs option will be ignored.
        """
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"validators": [clean_email]},
        }
        # fields = "__all__"

    def validate_name(self, value):
        """
        Field Level Validation
        """
        if value == "admin":
            raise serializers.ValidationError("Username cannot be admin")
        return value

    def validate(self, data):
        """
        Object Level Validation,
        First field validation will be executed, and if there was no error,
        then object-level validation will be executes
        """
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords should match")
        return data
