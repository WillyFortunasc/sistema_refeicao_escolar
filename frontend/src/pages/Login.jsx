import { useState } from "react";
import axios from "axios";

export default function Login() {
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

      // salva o token
      localStorage.setItem("token", token);

      setMsg("Login realizado com sucesso 🚀");

      console.log("TOKEN:", token);

    } catch (error) {
      setMsg("Erro ao fazer login ❌");
      console.error(error);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Login</h2>

      <form onSubmit={handleLogin}>
        <div>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div>
          <input
            type="password"
            placeholder="Senha"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
          />
        </div>

        <button type="submit">Entrar</button>
      </form>

      <p>{msg}</p>
    </div>
  );
}
