import { useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            const res = await api.post("login/", {
                username,
                password,
            });

            localStorage.setItem("pre_auth_token", res.data.pre_auth_token);
            navigate("/otp");
        } catch (err) {
            console.error(err.response?.data);

            alert(
                err.response?.data?.error ||
                "Login failed"
            );
        }

    };

    return (
        <form onSubmit={handleLogin}>
            <h2>Login</h2>

            <input
                name="username"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />

            <input
                name="password"
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />

            <button type="submit">Login</button>
        </form>
    );
}
