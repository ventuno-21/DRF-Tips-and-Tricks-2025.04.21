from rest_framework import serializers


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
        Object Level Validation
        """
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords should match")
        return data
