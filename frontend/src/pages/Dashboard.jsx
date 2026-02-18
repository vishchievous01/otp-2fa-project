import { useEffect, useState } from "react";
import api from "../services/api";

export default function Dashboard() {
    const [message, setMessage] = useState("");

    useEffect(() => {
        api
            .get("dashboard/", {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                },
            })
            .then((res) => setMessage(res.data.message))
            .catch(() => setMessage("Unauthorized"));
    }, []);

    return <h2>{message}</h2>
}