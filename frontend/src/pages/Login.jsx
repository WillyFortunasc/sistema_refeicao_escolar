import { useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [msg, setMsg] = useState("");

  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    const sucesso = await login(email, senha);

    if (sucesso) {
      navigate("/home");
    } else {
      setMsg("Credenciais inválidas ❌");
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
            className="w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Senha"
            className="w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
          />

          <button className="w-full bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600 transition">
            Entrar
          </button>
        </form>

        {msg && (
          <p className="mt-4 text-center text-sm text-gray-600">{msg}</p>
        )}
      </div>
    </div>
  );
}
