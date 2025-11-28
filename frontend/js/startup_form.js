// js/startup_form.js
export class StartupFormPage {
    constructor() {
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
        } else {
            // Redirigir al login si no está autenticado
            alert('Debes iniciar sesión para crear o editar una startup');
            window.location.href = './login.html';
        }
    }

    async loadCategories() {
        try {
            this.categories = await this.fetchCategories();
            this.renderCategories();
        } catch (error) {
            console.error('Error loading categories:', error);
        }
    }

    async fetchCategories() {
        // Simulación - reemplazar con llamada real a la API
        return [
            { category_id: 1, name: "Tecnología", description: "Startups tecnológicas e innovadoras" },
            { category_id: 2, name: "Salud", description: "Innovación en el sector salud" },
            { category_id: 3, name: "Educación", description: "EdTech y soluciones educativas" },
            { category_id: 4, name: "Finanzas", description: "FinTech y servicios financieros" },
            { category_id: 5, name: "Medio Ambiente", description: "Soluciones sostenibles y ecológicas" },
            { category_id: 6, name: "Comercio", description: "E-commerce y retail" }
        ];
    }

    renderCategories() {
        const select = document.getElementById('category_id');
        select.innerHTML = '<option value="">Selecciona una categoría</option>' +
            this.categories.map(cat =>
                `<option value="${cat.category_id}">${cat.name}</option>`
            ).join('');
    }

    async loadStartupData() {
        try {
            const startup = await this.fetchStartupById(this.startupId);
            this.populateForm(startup);
            this.updateUIForEditMode();
        } catch (error) {
            console.error('Error loading startup data:', error);
            this.showError('Error al cargar los datos de la startup');
        }
    }

    async fetchStartupById(startupId) {
        // Simulación - reemplazar con llamada real a la API
        return {
            startup_id: startupId,
            name: "TechInnovate",
            description: "Una startup dedicada a la innovación tecnológica",
            email: "contact@techinnovate.com",
            website: "https://techinnovate.com",
            social_media: "@techinnovate",
            category_id: 1
        };
    }

    populateForm(startup) {
        document.getElementById('name').value = startup.name;
        document.getElementById('description').value = startup.description;
        document.getElementById('category_id').value = startup.category_id;
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
        form.addEventListener('submit', (e) => this.handleFormSubmit(e));
    }

    async handleFormSubmit(e) {
        e.preventDefault();

        if (!this.validateForm()) {
            return;
        }

        const formData = this.getFormData();

        try {
            if (this.isEditMode) {
                await this.updateStartup(formData);
            } else {
                await this.createStartup(formData);
            }

            this.showSuccess('Startup guardada exitosamente');
            setTimeout(() => {
                window.location.href = './home.html';
            }, 1500);

        } catch (error) {
            console.error('Error saving startup:', error);
            this.showError('Error al guardar la startup');
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
        return {
            name: document.getElementById('name').value.trim(),
            description: document.getElementById('description').value.trim(),
            category_id: parseInt(document.getElementById('category_id').value),
            email: document.getElementById('email').value.trim() || null,
            website: document.getElementById('website').value.trim() || null,
            social_media: document.getElementById('social_media').value.trim() || null,
            owner_user_id: this.currentUser.user_id
        };
    }

    async createStartup(formData) {
        // Simulación - reemplazar con llamada real a la API
        console.log('Creando startup:', formData);
        return new Promise(resolve => setTimeout(resolve, 1000));
    }

    async updateStartup(formData) {
        // Simulación - reemplazar con llamada real a la API
        console.log('Actualizando startup:', formData);
        return new Promise(resolve => setTimeout(resolve, 1000));
    }

    showSuccess(message) {
        // Implementar notificación de éxito
        alert(message);
    }

    showError(message) {
        // Implementar notificación de error
        alert(message);
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

// Inicializar la página
new StartupFormPage();