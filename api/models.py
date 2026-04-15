from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


# =========================
# USUÁRIO
# =========================

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, senha=None, **extra_fields):
        if not email:
            raise ValueError("Usuário precisa de um email")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            nome=nome,
            **extra_fields
        )

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

    # ⚠️ não use campo senha manual em AbstractBaseUser
    # o Django já gerencia isso com set_password
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


# =========================
# ESTUDANTE
# =========================

class Estudante(models.Model):
    nome_completo = models.CharField(max_length=255)
    matricula = models.CharField(max_length=50, unique=True)
    data_nascimento = models.DateField()
    curso = models.CharField(max_length=100)
    turma = models.CharField(max_length=50)

    foto = models.ImageField(upload_to='fotos/', null=True, blank=True)
    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome_completo


# =========================
# DIGITAL (BIOMETRIA)
# =========================

class Digital(models.Model):
    estudante = models.ForeignKey(
        Estudante,
        on_delete=models.CASCADE,
        related_name="digitais"
    )

    codigo_hex = models.CharField(max_length=255, unique=True)
    dedo = models.CharField(max_length=50, blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudante.nome_completo} - {self.codigo_hex}"
