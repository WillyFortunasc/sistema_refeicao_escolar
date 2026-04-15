from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Usuario, Estudante


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer de leitura — nunca expõe senha."""
    class Meta:
        model  = Usuario
        fields = ["id", "nome", "email", "papel", "ativo", "ultimo_acesso", "google_id"]
        read_only_fields = ["id", "ultimo_acesso", "google_id"]


class RegistroSerializer(serializers.ModelSerializer):
    """Criação de usuário por um admin (login tradicional)."""
    senha           = serializers.CharField(write_only=True, required=True,
                                            validators=[validate_password])
    confirmar_senha = serializers.CharField(write_only=True, required=True)

    class Meta:
        model  = Usuario
        fields = ["nome", "email", "senha", "confirmar_senha", "papel"]

    def validate(self, attrs):
        if attrs["senha"] != attrs.pop("confirmar_senha"):
            raise serializers.ValidationError({"senha": "As senhas não conferem."})
        return attrs

    def create(self, validated_data):
        senha = validated_data.pop("senha")
        user  = Usuario(**validated_data)
        user.set_password(senha)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True)


# =========================
# NOVO SERIALIZER - ESTUDANTE
# =========================

class EstudanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = "__all__"
