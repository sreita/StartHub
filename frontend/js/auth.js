// js/auth.js
export class AuthService {
    static BASE_URL = 'http://localhost:8080/api/v1';

    static async login(email, password) {
        try {
            const response = await fetch(`${this.BASE_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText || 'Login failed');
            }

            const data = await response.json();
            return {
                success: true,
                token: data.token,
                user: data.user
            };
        } catch (error) {
            console.error('Error en AuthService.login:', error);
            throw error;
        }
    }

    static async register(userData) {
        try {
            const response = await fetch(`${this.BASE_URL}/registration`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText || 'Registration failed');
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

    static async recoverPassword(email) {
    try {
        const response = await fetch(`${this.BASE_URL}/auth/recover-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email })
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || 'Error en la recuperación de contraseña');
        }

        return { success: true };
    } catch (error) {
        console.error('Error en AuthService.recoverPassword:', error);
        throw error;
    }
}

    static async resetPassword(token, newPassword) {
        try {
            console.log('🔍 Enviando reset password con token:', token);

            const response = await fetch(`${this.BASE_URL}/auth/reset-password`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ token, newPassword })
            });

            console.log('📡 Respuesta del servidor:', response.status);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('❌ Error del servidor:', errorText);
                throw new Error(errorText || 'Error al restablecer la contraseña');
            }

            console.log('✅ Contraseña restablecida exitosamente');
            return { success: true }; // Este return está dentro de una función, es válido
        } catch (error) {
            console.error('💥 Error en AuthService.resetPassword:', error);
            throw error;
        }
    }

    static async getUserProfile(userId) {
        try {
            const response = await this.makeAuthenticatedRequest(`/users/${userId}`);
            return await response.json();
        } catch (error) {
            console.error('Error en AuthService.getUserProfile:', error);
            throw error;
        }
    }

    static async updateUserProfile(userId, userData) {
        try {
            const response = await this.makeAuthenticatedRequest(`/users/${userId}`, {
                method: 'PUT',
                body: JSON.stringify(userData)
            });
            return await response.json();
        } catch (error) {
            console.error('Error en AuthService.updateUserProfile:', error);
            throw error;
        }
    }

    static async deleteUser(userId) {
        try {
            const response = await this.makeAuthenticatedRequest(`/users/${userId}`, {
                method: 'DELETE'
            });
            return { success: true };
        } catch (error) {
            console.error('Error en AuthService.deleteUser:', error);
            throw error;
        }
    }

    static logout() {
        // Opcional: llamar al endpoint de logout del servidor
        fetch(`${this.BASE_URL}/auth/logout`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.getToken()}`
            }
        }).catch(console.error);

        // Limpiar localStorage y redirigir
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        window.location.href = './home.html';
    }

    static getCurrentUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    }

    static isAuthenticated() {
        return !!localStorage.getItem('authToken');
    }

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

        if (response.status === 401 || response.status === 403) {
            this.logout();
            throw new Error('Authentication failed');
        }

        return response;
    }

    static getToken() {
        return localStorage.getItem('authToken');
    }
}