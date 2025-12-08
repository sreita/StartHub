// js/startup_form.js
export class StartupFormPage {
    constructor() {
        this.API_BASE_URL = 'http://localhost:8000/api/v1';
        this.startupId = this.getStartupIdFromURL();
        this.isEditMode = !!this.startupId;
        this.currentUser = null;
        this.categories = [];
        this.init();
    }

    init() {
        console.log('Inicializando StartupFormPage...');
        this.checkAuthStatus();
        this.loadCategories();
        this.setupForm();
        this.setupNightMode();
        this.setupDropdown();

        if (this.isEditMode) {
            this.loadStartupData();
        }
    }

    getStartupIdFromURL() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('id');
    }

    checkAuthStatus() {
        const token = localStorage.getItem('authToken');
        const user = localStorage.getItem('user');

        if (token && user) {
            this.currentUser = JSON.parse(user);
            console.log('Usuario completo desde localStorage:', this.currentUser);

            // SOLUCIÓN: Buscar el ID del usuario en diferentes propiedades posibles
            this.currentUser.user_id = this.findUserId(this.currentUser);

            if (!this.currentUser.user_id) {
                console.error('No se pudo encontrar el ID del usuario en:', this.currentUser);
                this.showError('Error de autenticación: no se pudo identificar al usuario');
                return;
            }

            console.log('Usuario autenticado con ID:', this.currentUser.user_id);
        } else {
            alert('Debes iniciar sesión para crear o editar una startup');
            window.location.href = './login.html';
        }
    }

    // Método para encontrar el ID del usuario en diferentes formatos
    findUserId(userObj) {
        // Probar diferentes nombres de campo comunes
        const possibleIdFields = [
            'user_id', 'id', 'userId', 'ID', 'Id',
            'usuario_id', 'usuarioId', 'USER_ID'
        ];

        for (const field of possibleIdFields) {
            if (userObj[field] !== undefined && userObj[field] !== null) {
                console.log(`ID encontrado en campo: ${field}`, userObj[field]);
                return parseInt(userObj[field]);
            }
        }

        // Si no se encuentra en campos comunes, buscar en toda la estructura
        console.log('Buscando ID recursivamente...');
        return this.findUserIdRecursive(userObj);
    }

    findUserIdRecursive(obj, depth = 0) {
        if (depth > 3) return null; // Límite de profundidad para evitar bucles infinitos

        if (typeof obj === 'object' && obj !== null) {
            for (const key in obj) {
                const value = obj[key];

                // Si la clave sugiere que es un ID y el valor es un número
                if ((key.toLowerCase().includes('id') || key.toLowerCase().includes('_id')) &&
                    (typeof value === 'number' || (typeof value === 'string' && !isNaN(value)))) {
                    console.log(`ID potencial encontrado en ${key}:`, value);
                    return parseInt(value);
                }

                // Buscar recursivamente en objetos y arrays
                if (typeof value === 'object' && value !== null) {
                    const found = this.findUserIdRecursive(value, depth + 1);
                    if (found) return found;
                }
            }
        }

        return null;
    }

    async loadCategories() {
        try {
            console.log('Cargando categorías desde /categories/');
            const response = await fetch(`${this.API_BASE_URL}/categories/`);

            if (response.ok) {
                this.categories = await response.json();
                console.log('Categorías cargadas:', this.categories);
                this.renderCategories();
            } else {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
        } catch (error) {
            console.log('Error cargando categorías:', error.message);
            this.loadFallbackCategories();
        }
    }

    loadFallbackCategories() {
        console.log('Cargando categorías de respaldo...');
        this.categories = [
            { category_id: 1, name: "Tecnología" },
            { category_id: 2, name: "Salud" },
            { category_id: 3, name: "Educación" },
            { category_id: 4, name: "Finanzas" },
            { category_id: 5, name: "Medio Ambiente" },
            { category_id: 6, name: "Comercio" }
        ];
        this.renderCategories();
    }

    renderCategories() {
        const select = document.getElementById('category_id');
        if (select) {
            select.innerHTML = '<option value="">Selecciona una categoría</option>' +
                this.categories.map(cat =>
                    `<option value="${cat.category_id}">${cat.name}</option>`
                ).join('');
        }
    }

    async loadStartupData() {
        try {
            const token = localStorage.getItem('authToken');
            console.log('Cargando startup con ID:', this.startupId);

            const response = await fetch(`${this.API_BASE_URL}/startups/${this.startupId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            console.log('Respuesta de startup:', response.status, response.statusText);

            if (response.ok) {
                const startup = await response.json();
                console.log('Startup cargada:', startup);
                this.populateForm(startup);
                this.updateUIForEditMode();

                // Verificar que el usuario es el propietario
                if (startup.owner_user_id !== this.currentUser.user_id && !this.currentUser.is_admin) {
                    this.showError('No tienes permisos para editar esta startup');
                    window.location.href = './home.html';
                }
            } else {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
        } catch (error) {
            console.error('Error loading startup data:', error);
            this.showError('Error al cargar los datos de la startup: ' + error.message);
        }
    }

    populateForm(startup) {
        document.getElementById('name').value = startup.name || '';
        document.getElementById('description').value = startup.description || '';
        document.getElementById('category_id').value = startup.category_id || '';
        document.getElementById('email').value = startup.email || '';
        document.getElementById('website').value = startup.website || '';
        document.getElementById('social_media').value = startup.social_media || '';
    }

    updateUIForEditMode() {
        document.getElementById('form-title').textContent = 'Editar Startup';
        document.getElementById('submit-text').textContent = 'Actualizar Startup';
    }

    setupForm() {
        const form = document.getElementById('startup-form');
        if (form) {
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }
    }

    async handleFormSubmit(e) {
        e.preventDefault();

        if (!this.validateForm()) {
            return;
        }

        const submitButton = document.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = 'Guardando...';
        submitButton.disabled = true;

        try {
            let result;
            if (this.isEditMode) {
                result = await this.updateStartup();
            } else {
                result = await this.createStartup();
            }

            if (result.success) {
                this.showSuccess(result.message);
                setTimeout(() => {
                    window.location.href = './home.html';
                }, 1500);
            } else {
                this.showError(result.message);
            }

        } catch (error) {
            console.error('Error saving startup:', error);
            this.showError('Error al guardar la startup: ' + error.message);
        } finally {
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }
    }

    validateForm() {
        const name = document.getElementById('name').value.trim();
        const description = document.getElementById('description').value.trim();
        const categoryId = document.getElementById('category_id').value;

        if (!name) {
            this.showError('El nombre de la startup es requerido');
            return false;
        }

        if (!description) {
            this.showError('La descripción es requerida');
            return false;
        }

        if (!categoryId) {
            this.showError('La categoría es requerida');
            return false;
        }

        return true;
    }

    getFormData() {
        const formData = {
            name: document.getElementById('name').value.trim(),
            description: document.getElementById('description').value.trim(),
            category_id: parseInt(document.getElementById('category_id').value),
            email: document.getElementById('email').value.trim() || null,
            website: document.getElementById('website').value.trim() || null,
            social_media: document.getElementById('social_media').value.trim() || null
        };

        // Para creación, agregar owner_user_id al body
        if (!this.isEditMode) {
            formData.owner_user_id = this.currentUser.user_id;
        }

        return formData;
    }

    async createStartup() {
        const token = localStorage.getItem('authToken');
        const formData = this.getFormData();

        console.log('Enviando datos de creación:', formData);
        console.log('URL:', `${this.API_BASE_URL}/startups/`);

        const response = await fetch(`${this.API_BASE_URL}/startups/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(formData)
        });

        console.log('Respuesta de creación:', response.status, response.statusText);

        if (response.ok) {
            const data = await response.json();
            console.log('Startup creada exitosamente:', data);
            return {
                success: true,
                message: 'Startup creada exitosamente',
                data: data
            };
        } else {
            let errorMessage = `Error ${response.status}: ${response.statusText}`;
            try {
                const errorData = await response.json();
                console.log('Error detallado del servidor:', errorData);

                // Manejar diferentes formatos de error de FastAPI
                if (errorData.detail) {
                    if (Array.isArray(errorData.detail)) {
                        // Si es un array de errores de validación
                        errorMessage = errorData.detail.map(err =>
                            `${err.loc ? err.loc.join('.') : ''}: ${err.msg}`
                        ).join(', ');
                    } else {
                        // Si es un string simple
                        errorMessage = errorData.detail;
                    }
                } else if (errorData.message) {
                    errorMessage = errorData.message;
                }
            } catch (e) {
                console.log('No se pudo parsear la respuesta de error:', e);
            }
            throw new Error(errorMessage);
        }
    }

    async updateStartup() {
        const token = localStorage.getItem('authToken');
        const formData = this.getFormData();

        console.log('Enviando datos de actualización:', formData);

        // Para actualización, el user_id va como query parameter
        const queryParams = new URLSearchParams({
            user_id: this.currentUser.user_id
        });

        const response = await fetch(`${this.API_BASE_URL}/startups/${this.startupId}?${queryParams}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(formData)
        });

        console.log('Respuesta de actualización:', response.status, response.statusText);

        if (response.ok) {
            const data = await response.json();
            return {
                success: true,
                message: 'Startup actualizada exitosamente',
                data: data
            };
        } else {
            let errorMessage = `Error ${response.status}: ${response.statusText}`;
            try {
                const errorData = await response.json();
                console.log('Error detallado del servidor:', errorData);

                if (errorData.detail) {
                    if (Array.isArray(errorData.detail)) {
                        errorMessage = errorData.detail.map(err =>
                            `${err.loc ? err.loc.join('.') : ''}: ${err.msg}`
                        ).join(', ');
                    } else {
                        errorMessage = errorData.detail;
                    }
                } else if (errorData.message) {
                    errorMessage = errorData.message;
                }
            } catch (e) {
                console.log('No se pudo parsear la respuesta de error:', e);
            }
            throw new Error(errorMessage);
        }
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg border-2 border-black font-bold z-50 ${
            type === 'success' ? 'bg-green-400' : 'bg-red-400'
        }`;
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    setupNightMode() {
        const nightModeToggle = document.getElementById('night-mode-toggle');
        if (nightModeToggle) {
            nightModeToggle.addEventListener('click', (e) => {
                e.preventDefault();
                document.body.classList.toggle('night-mode-active');
                localStorage.setItem('nightMode', document.body.classList.contains('night-mode-active'));
            });

            const savedNightMode = localStorage.getItem('nightMode') === 'true';
            if (savedNightMode) {
                document.body.classList.add('night-mode-active');
            }
        }
    }

    setupDropdown() {
        const dropdownBtn = document.getElementById('dropdown-btn');
        const dropdownMenu = document.getElementById('dropdown-menu');

        if (dropdownBtn && dropdownMenu) {
            dropdownBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                dropdownMenu.classList.toggle('hidden');
            });

            document.addEventListener('click', () => {
                dropdownMenu.classList.add('hidden');
            });
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new StartupFormPage();
});