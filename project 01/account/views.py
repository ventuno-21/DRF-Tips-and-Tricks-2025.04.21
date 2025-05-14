from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Person
from .serializers import PersonSerilizer
from api.models import User
from .models import Person

# Create your views here.


class PersonRegister(APIView):
    def post(self, request):
        s_data = PersonSerilizer(data=request.data)
        if s_data.is_valid():
            Person.objects.create(
                name=s_data.validated_data["name"],
                email=s_data.validated_data["email"],
                password=s_data.validated_data["password"],
            )
            # Because we mention write_only for password filed in PersonSerlizer, it would not show password in Response.data
            return Response(s_data.data)

        return Response(s_data.errors)
