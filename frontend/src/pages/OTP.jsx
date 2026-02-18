import { useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

export default function OTP() {
    const [otp, setOtp] = useState("");
    const navigate = useNavigate();

    const handleVerify = async (e) => {
        e.preventDefault();

        try {
            const res = await api.post("verify-otp/", {
                pre_auth_token: localStorage.getItem("pre_auth_token"),
                otp,
            });

            localStorage.setItem("access_token", res.data.access_token);
            localStorage.setItem("refresh_token", res.data.refresh_token);

            navigate("/dashboard");
        } catch {
            alert("Invalid OTP");
        }
    };

    return (
        <form onSubmit={handleVerify}>
            <h2>OTP Verification</h2>

            <input
                placeholder="Enter OTP"
                onChange={(e) => setOtp(e.target.value)}
            />

            <button type="submit">Verify OTP</button>
        </form>
    );
}