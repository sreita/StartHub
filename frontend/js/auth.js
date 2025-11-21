// js/auth.js
export class AuthService {
    static async login(username, password) {
        try {
            // Aquí defines a qué API conectar (Java o Python)
            // Por ejemplo, si el login está en la API de Java:
            const response = await fetch('http://localhost:8080/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });

            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }

            return await response.json();
        } catch (error) {
            console.error('Error en AuthService.login:', error);
            throw error;
        }
    }

    static async register(userData) {
        try {
            // Cambia esta URL por tu endpoint real de registro
            const response = await fetch('http://localhost:8080/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Error en el registro');
            }

            return await response.json();
        } catch (error) {
            console.error('Error en AuthService.register:', error);
            throw error;
        }
    }


    static logout() {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        window.location.href = './login.html';
    }

    static getCurrentUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    }

    static isAuthenticated() {
        return !!localStorage.getItem('authToken');
    }
}