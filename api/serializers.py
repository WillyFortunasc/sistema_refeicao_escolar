from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Usuario, Estudante, Digital


# =========================
# USUÁRIO
# =========================

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "nome", "email", "papel", "ativo", "ultimo_acesso", "google_id"]
        read_only_fields = ["id", "ultimo_acesso", "google_id"]


class RegistroSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirmar_senha = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = ["nome", "email", "senha", "confirmar_senha", "papel"]

    def validate(self, attrs):
        if attrs["senha"] != attrs.pop("confirmar_senha"):
            raise serializers.ValidationError({"senha": "As senhas não conferem."})
        return attrs

    def create(self, validated_data):
        senha = validated_data.pop("senha")
        user = Usuario(**validated_data)
        user.set_password(senha)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True)


# =========================
# ESTUDANTE
# =========================

class EstudanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = "__all__"


# =========================
# DIGITAL
# =========================

class DigitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Digital
        fields = "__all__"

    def validate_codigo_hex(self, value):
        if not value.startswith("0x"):
            raise serializers.ValidationError("Código deve começar com 0x")

        # impede duplicidade global
        if Digital.objects.filter(codigo_hex=value).exists():
            raise serializers.ValidationError("Este código já está cadastrado.")

        return value

    def validate(self, data):
        estudante = data.get("estudante")

        if estudante:
            total = Digital.objects.filter(estudante=estudante).count()
            if total >= 3:
                raise serializers.ValidationError(
                    "Este aluno já possui 3 digitais cadastradas."
                )

        return data
