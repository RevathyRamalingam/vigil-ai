const API_BASE_URL = "/api";

export const api = {
    async scan() {
        const response = await fetch(`${API_BASE_URL}/scan`, { method: "POST" });
        if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
    },

    async getCameras() {
        const response = await fetch(`${API_BASE_URL}/cameras`);
        if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
    },

    async getAlerts() {
        const response = await fetch(`${API_BASE_URL}/alerts`);
        if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
    },

    async updateAlert(id: string, status: string) {
        const response = await fetch(`${API_BASE_URL}/alerts/${id}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status }),
        });
        if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
    }
};
