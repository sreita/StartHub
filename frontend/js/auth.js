// js/auth.js
export class AuthService {
    static BASE_URL = 'http://localhost:8080'; // URL de tu backend Spring Boot

    static async login(email, password) {
        try {
            // Conectando con tu backend Spring Boot
            const response = await fetch(`${this.BASE_URL}/api/v1/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText || 'Error en la respuesta del servidor');
            }

            const data = await response.json();
            return {
                success: true,
                token: data.token,
                user: { email: email } // Puedes expandir esto con más datos del usuario
            };
        } catch (error) {
            console.error('Error en AuthService.login:', error);
            throw error;
        }
    }

    static async register(userData) {
        try {
            // Conectando con tu backend Spring Boot
            const response = await fetch(`${this.BASE_URL}/api/v1/registration`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText || 'Error en el registro');
            }

            const result = await response.text();
            return {
                success: true,
                message: result
            };
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

    // Método para hacer peticiones autenticadas
    static async makeAuthenticatedRequest(url, options = {}) {
        const token = this.getToken();

        if (!token) {
            throw new Error('No authentication token found');
        }

        const defaultOptions = {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                ...options.headers
            }
        };

        const mergedOptions = { ...defaultOptions, ...options };

        const response = await fetch(`${this.BASE_URL}${url}`, mergedOptions);

        if (response.status === 403 || response.status === 401) {
            this.logout();
            throw new Error('Authentication failed');
        }

        return response;
    }

    static getToken() {
        return localStorage.getItem('authToken');
    }
}