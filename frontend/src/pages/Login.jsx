import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [msg, setMsg] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/login/", {
        email,
        senha,
      });

      const token = response.data.token;

      // salva token
      localStorage.setItem("token", token);

      setMsg("Login realizado com sucesso 🚀");

      // 🚀 AQUI ESTÁ O QUE FALTAVA
      setTimeout(() => {
        navigate("/home");
      }, 500);

    } catch (error) {
      console.error(error);
      setMsg("Erro ao fazer login ❌");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-500 to-indigo-600">
      <div className="bg-white p-8 rounded-2xl shadow-lg w-96">
        <h2 className="text-2xl font-bold mb-6 text-center text-gray-700">
          Sistema Escolar
        </h2>

        <form onSubmit={handleLogin} className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            className="w-full p-2 border rounded-lg"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Senha"
            className="w-full p-2 border rounded-lg"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
          />

          <button
            type="submit"
            className="w-full bg-blue-500 text-white p-2 rounded-lg"
          >
            Entrar
          </button>
        </form>

        {msg && <p className="mt-4 text-center">{msg}</p>}
      </div>
    </div>
  );
}
