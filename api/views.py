from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.http import JsonResponse
import jwt
from django.conf import settings

from .models import Usuario, Estudante, Digital
from .serializers import UsuarioSerializer, EstudanteSerializer, DigitalSerializer


def health_check(request):
    return JsonResponse({"status": "ok"})


class RegistroView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        senha = request.data.get("senha")

        user = authenticate(request, email=email, password=senha)

        if user is not None and user.ativo:
            payload = {
                "id": user.id,
                "email": user.email,
                "papel": user.papel
            }

            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

            return Response({
                "token": token,
                "papel": user.papel
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "Credenciais inválidas"},
            status=status.HTTP_401_UNAUTHORIZED
        )


# =========================
# ESTUDANTE
# =========================

class EstudanteViewSet(viewsets.ModelViewSet):
    queryset = Estudante.objects.all().order_by("-criado_em")
    serializer_class = EstudanteSerializer
    permission_classes = [AllowAny]


# =========================
# DIGITAL
# =========================

class DigitalViewSet(viewsets.ModelViewSet):
    queryset = Digital.objects.all()
    serializer_class = DigitalSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        estudante_id = self.request.query_params.get("estudante_id")
        if estudante_id:
            return self.queryset.filter(estudante_id=estudante_id)
        return self.queryset
