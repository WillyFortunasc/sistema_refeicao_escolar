from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, senha=None, **extra_fields):
        if not email:
            raise ValueError("Usuário precisa de um email")
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, **extra_fields)
        user.set_password(senha)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, senha=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, nome, senha, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128, blank=True, null=True)
    google_id = models.CharField(max_length=255, blank=True, null=True)
    papel = models.CharField(
        max_length=20,
        choices=[
            ("operador", "Operador"),
            ("empresa", "Empresa"),
            ("fiscal", "Fiscal"),
            ("gestor", "Gestor"),
            ("admin", "Admin"),
        ]
    )
    ativo = models.BooleanField(default=True)
    ultimo_acesso = models.DateTimeField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome"]

    objects = UsuarioManager()

    def __str__(self):
        return self.email
