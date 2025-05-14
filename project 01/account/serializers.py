from rest_framework import serializers


class PersonSerilizer(serializers.Serializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    # Because we mention write_only for password filed in PersonSerlizer, it would not show password in Response.data
    password = serializers.CharField(required=True, write_only=True)
