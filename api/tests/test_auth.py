"""
Testes automatizados — autenticação e controle de papéis.
Execute: python manage.py test api.tests
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Usuario


def _criar_usuario(email, nome, papel, senha=None):
    return Usuario.objects.create_user(email=email, nome=nome, papel=papel, senha=senha)


def _token(client, email, senha):
    resp = client.post(
        reverse("login"),
        {"email": email, "senha": senha},
        format="json",
    )
    return resp.data.get("access", "")


class ModelUsuarioTest(TestCase):
    """Testa o model e o manager."""

    def test_criar_usuario_com_senha(self):
        u = _criar_usuario("op@test.com", "Operador", "operador", "Senha@123")
        self.assertEqual(u.email, "op@test.com")
        self.assertEqual(u.papel, "operador")
        self.assertTrue(u.check_password("Senha@123"))

    def test_senha_armazenada_com_hash(self):
        u = _criar_usuario("op2@test.com", "Op2", "operador", "Senha@123")
        # A senha salva nunca deve ser igual ao texto puro
        self.assertNotEqual(u.password, "Senha@123")

    def test_criar_usuario_sem_senha_nao_tem_senha_utilizavel(self):
        u = _criar_usuario("fiscal@test.com", "Fiscal", "fiscal", None)
        self.assertFalse(u.has_usable_password())

    def test_criar_superusuario(self):
        su = Usuario.objects.create_superuser(
            email="su@test.com", nome="Super", senha="Super@123"
        )
        self.assertTrue(su.is_staff)
        self.assertTrue(su.is_superuser)
        self.assertEqual(su.papel, "admin")

    def test_registrar_acesso_atualiza_ultimo_acesso(self):
        u = _criar_usuario("ac@test.com", "Acesso", "gestor", "Pass@123")
        self.assertIsNone(u.ultimo_acesso)
        u.registrar_acesso()
        u.refresh_from_db()
        self.assertIsNotNone(u.ultimo_acesso)


class LoginViewTest(TestCase):
    """Testa POST /api/auth/login/"""

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("login")
        self.user = _criar_usuario("login@test.com", "Login", "operador", "Login@123")

    def test_login_correto_retorna_tokens(self):
        resp = self.client.post(
            self.url, {"email": "login@test.com", "senha": "Login@123"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)
        self.assertIn("usuario", resp.data)
        self.assertEqual(resp.data["usuario"]["papel"], "operador")

    def test_login_senha_errada_retorna_401(self):
        resp = self.client.post(
            self.url, {"email": "login@test.com", "senha": "Errada@123"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_email_inexistente_retorna_401(self):
        resp = self.client.post(
            self.url, {"email": "nao@existe.com", "senha": "Qualquer@1"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_conta_inativa_retorna_403(self):
        self.user.ativo = False
        self.user.save()
        resp = self.client.post(
            self.url, {"email": "login@test.com", "senha": "Login@123"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_atualiza_ultimo_acesso(self):
        self.client.post(
            self.url, {"email": "login@test.com", "senha": "Login@123"}, format="json"
        )
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.ultimo_acesso)

    def test_login_sem_campos_retorna_400(self):
        resp = self.client.post(self.url, {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class MeViewTest(TestCase):
    """Testa GET /api/auth/me/"""

    def setUp(self):
        self.client = APIClient()
        self.user = _criar_usuario("me@test.com", "Me", "gestor", "Me@12345")
        self.token = _token(self.client, "me@test.com", "Me@12345")

    def test_me_autenticado_retorna_dados(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        resp = self.client.get(reverse("me"))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["email"], "me@test.com")
        self.assertEqual(resp.data["papel"], "gestor")

    def test_me_sem_token_retorna_401(self):
        resp = self.client.get(reverse("me"))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class RegistroViewTest(TestCase):
    """Testa POST /api/auth/registro/ — apenas admin pode registrar."""

    def setUp(self):
        self.client = APIClient()
        self.admin = _criar_usuario("adm@test.com", "Admin", "admin", "Adm@12345")
        self.operador = _criar_usuario("op@test.com", "Op", "operador", "Op@12345")
        self.admin_token = _token(self.client, "adm@test.com", "Adm@12345")
        self.op_token = _token(self.client, "op@test.com", "Op@12345")
        self.url = reverse("registro")
        self.payload = {
            "nome": "Novo Fiscal",
            "email": "novo@test.com",
            "papel": "fiscal",
            "senha": "Fiscal@123",
            "confirmar_senha": "Fiscal@123",
        }

    def test_admin_pode_registrar(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        resp = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Usuario.objects.filter(email="novo@test.com").exists())

    def test_nao_admin_nao_pode_registrar(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.op_token}")
        resp = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_sem_autenticacao_nao_pode_registrar(self):
        resp = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_senhas_diferentes_retorna_400(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        payload = {**self.payload, "confirmar_senha": "Diferente@123"}
        resp = self.client.post(self.url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_duplicado_retorna_400(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        self.client.post(self.url, self.payload, format="json")
        resp = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_senha_fraca_retorna_400(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        payload = {**self.payload, "email": "fraco@test.com", "senha": "123", "confirmar_senha": "123"}
        resp = self.client.post(self.url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class UsuariosListViewTest(TestCase):
    """Testa GET /api/usuarios/ — apenas admin."""

    def setUp(self):
        self.client = APIClient()
        self.admin = _criar_usuario("adm2@test.com", "Admin2", "admin", "Adm@12345")
        self.fiscal = _criar_usuario("fis@test.com", "Fiscal", "fiscal", "Fis@12345")
        self.admin_token = _token(self.client, "adm2@test.com", "Adm@12345")
        self.fiscal_token = _token(self.client, "fis@test.com", "Fis@12345")

    def test_admin_lista_todos(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        resp = self.client.get(reverse("usuarios_list"))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.data), 2)

    def test_nao_admin_nao_lista(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.fiscal_token}")
        resp = self.client.get(reverse("usuarios_list"))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class UsuarioDetailViewTest(TestCase):
    """Testa GET/PATCH/DELETE /api/usuarios/<id>/"""

    def setUp(self):
        self.client = APIClient()
        self.admin = _criar_usuario("adm3@test.com", "Admin3", "admin", "Adm@12345")
        self.alvo = _criar_usuario("alvo@test.com", "Alvo", "operador", "Alvo@123")
        self.admin_token = _token(self.client, "adm3@test.com", "Adm@12345")

    def test_admin_ve_detalhe(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        resp = self.client.get(reverse("usuario_detail", args=[self.alvo.pk]))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["email"], "alvo@test.com")

    def test_admin_altera_papel(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        resp = self.client.patch(
            reverse("usuario_detail", args=[self.alvo.pk]),
            {"papel": "gestor"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.alvo.refresh_from_db()
        self.assertEqual(self.alvo.papel, "gestor")

    def test_admin_desativa_usuario(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        resp = self.client.patch(
            reverse("usuario_detail", args=[self.alvo.pk]),
            {"ativo": False},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.alvo.refresh_from_db()
        self.assertFalse(self.alvo.ativo)

    def test_admin_deleta_usuario(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        resp = self.client.delete(reverse("usuario_detail", args=[self.alvo.pk]))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Usuario.objects.filter(pk=self.alvo.pk).exists())

    def test_id_inexistente_retorna_404(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        resp = self.client.get(reverse("usuario_detail", args=[99999]))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


class TokenRefreshTest(TestCase):
    """Testa POST /api/auth/refresh/"""

    def setUp(self):
        self.client = APIClient()
        _criar_usuario("ref@test.com", "Ref", "operador", "Ref@12345")

    def test_refresh_retorna_novo_access(self):
        resp = self.client.post(
            reverse("login"),
            {"email": "ref@test.com", "senha": "Ref@12345"},
            format="json",
        )
        refresh = resp.data["refresh"]
        resp2 = self.client.post(
            reverse("token_refresh"), {"refresh": refresh}, format="json"
        )
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp2.data)

    def test_refresh_invalido_retorna_401(self):
        resp = self.client.post(
            reverse("token_refresh"), {"refresh": "token.invalido.aqui"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PermissoesPapelTest(TestCase):
    """Garante que cada papel só acessa o que deve."""

    def setUp(self):
        self.client = APIClient()
        papeis = ["operador", "empresa", "fiscal", "gestor"]
        self.tokens = {}
        for p in papeis:
            u = _criar_usuario(f"{p}@test.com", p.capitalize(), p, f"Pass@{p}1")
            resp = self.client.post(
                reverse("login"),
                {"email": f"{p}@test.com", "senha": f"Pass@{p}1"},
                format="json",
            )
            self.tokens[p] = resp.data.get("access", "")

    def test_nenhum_papel_comum_acessa_registro(self):
        for papel, token in self.tokens.items():
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
            resp = self.client.post(
                reverse("registro"),
                {
                    "nome": "X", "email": "x@x.com", "papel": "operador",
                    "senha": "Senha@123", "confirmar_senha": "Senha@123",
                },
                format="json",
            )
            self.assertEqual(
                resp.status_code, status.HTTP_403_FORBIDDEN,
                msg=f"Papel '{papel}' deveria ser 403 em /registro/",
            )

    def test_nenhum_papel_comum_lista_usuarios(self):
        for papel, token in self.tokens.items():
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
            resp = self.client.get(reverse("usuarios_list"))
            self.assertEqual(
                resp.status_code, status.HTTP_403_FORBIDDEN,
                msg=f"Papel '{papel}' deveria ser 403 em /usuarios/",
            )
