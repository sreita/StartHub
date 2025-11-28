// js/navbar.js
import { AuthService } from './auth.js';

export class NavbarManager {
    constructor() {
        this.navbarLoaded = false;
        this.init();
    }

    async init() {
        try {
            await this.loadNavbar();
            this.navbarLoaded = true;

            // Dar tiempo al DOM para renderizar
            setTimeout(() => {
                this.initializeNavbar();
            }, 50);

        } catch (error) {
            console.error('Error initializing navbar:', error);
            this.createFallbackNavbar();
        }
    }

    async loadNavbar() {
        try {
            const response = await fetch('./components/navbar.html');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const navbarHtml = await response.text();

            // Insertar la navbar al inicio del body
            document.body.insertAdjacentHTML('afterbegin', navbarHtml);

            console.log('✅ Navbar loaded successfully');
            return true;
        } catch (error) {
            console.error('❌ Error loading navbar:', error);
            throw error;
        }
    }

    initializeNavbar() {
        if (!this.navbarLoaded) {
            console.error('Navbar not loaded, cannot initialize');
            return;
        }

        console.log('🔄 Initializing navbar components');

        // Verificar que los elementos existen
        const dropdownBtn = document.getElementById('dropdown-btn');
        const dropdownMenu = document.getElementById('dropdown-menu');
        const searchButton = document.getElementById('search-button');
        const searchInput = document.getElementById('search-input');

        console.log('Navbar elements:', {
            dropdownBtn: !!dropdownBtn,
            dropdownMenu: !!dropdownMenu,
            searchButton: !!searchButton,
            searchInput: !!searchInput
        });

        // Configurar componentes
        this.setupUserDropdown();
        this.setupSearch();
        this.updateUI();
        this.applySavedNightMode();

        console.log('✅ Navbar initialization complete');
    }

    setupUserDropdown() {
        const dropdownBtn = document.getElementById('dropdown-btn');
        const dropdownMenu = document.getElementById('dropdown-menu');

        if (!dropdownBtn || !dropdownMenu) {
            console.error('❌ Dropdown elements missing:', {
                dropdownBtn: !!dropdownBtn,
                dropdownMenu: !!dropdownMenu
            });
            return;
        }

        console.log('✅ Setting up user dropdown');

        dropdownBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            console.log('Dropdown button clicked');
            dropdownMenu.classList.toggle('hidden');
        });

        // Cerrar dropdown al hacer clic fuera
        document.addEventListener('click', (e) => {
            if (!dropdownBtn.contains(e.target) && !dropdownMenu.contains(e.target)) {
                dropdownMenu.classList.add('hidden');
            }
        });

        // Prevenir que el clic dentro del dropdown lo cierre
        dropdownMenu.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    setupSearch() {
        const searchButton = document.getElementById('search-button');
        const searchInput = document.getElementById('search-input');

        if (!searchButton || !searchInput) {
            console.error('❌ Search elements missing');
            return;
        }

        console.log('✅ Setting up search functionality');

        searchButton.addEventListener('click', (e) => {
            e.stopPropagation();
            const isOpen = searchInput.classList.contains('w-0');
            console.log('Search button clicked, isOpen:', isOpen);

            if (isOpen) {
                searchInput.classList.remove('w-0', 'opacity-0');
                searchInput.classList.add('w-64', 'opacity-100');
                searchInput.focus();
            } else {
                searchInput.classList.add('w-0', 'opacity-0');
                searchInput.classList.remove('w-64', 'opacity-100');
            }
        });

        // Cerrar búsqueda al hacer clic fuera
        document.addEventListener('click', (e) => {
            if (!searchButton.contains(e.target) && !searchInput.contains(e.target)) {
                searchInput.classList.add('w-0', 'opacity-0');
                searchInput.classList.remove('w-64', 'opacity-100');
            }
        });

        // Cerrar búsqueda al presionar Escape
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                searchInput.classList.add('w-0', 'opacity-0');
                searchInput.classList.remove('w-64', 'opacity-100');
            }
        });
    }

    applySavedNightMode() {
        const savedNightMode = localStorage.getItem('nightMode') === 'true';
        if (savedNightMode) {
            document.body.classList.add('night-mode-active');
            console.log('🌙 Night mode applied from storage');
        }
    }

    toggleNightMode() {
        document.body.classList.toggle('night-mode-active');
        const isNightMode = document.body.classList.contains('night-mode-active');
        localStorage.setItem('nightMode', isNightMode.toString());

        console.log(`🌙 Night mode: ${isNightMode ? 'ON' : 'OFF'}`);
        this.updateUserDropdown();
    }

    updateUI() {
        this.updateUserDropdown();
    }

    updateUserDropdown() {
        const dropdownMenu = document.getElementById('dropdown-menu');
        if (!dropdownMenu) {
            console.error('❌ Dropdown menu not found for update');
            return;
        }

        const isAuthenticated = AuthService.isAuthenticated();
        const isNightMode = document.body.classList.contains('night-mode-active');

        console.log(`🔄 Updating dropdown: Authenticated=${isAuthenticated}, NightMode=${isNightMode}`);

        if (isAuthenticated) {
            const user = AuthService.getCurrentUser();
            dropdownMenu.innerHTML = `
                <a href="#" class="dropdown-menu-item night-mode-toggle">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                    </svg>
                    ${isNightMode ? 'MODO DÍA' : 'MODO NOCHE'}
                </a>
                <a href="./profile.html" class="dropdown-menu-item">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    MI PERFIL
                </a>
                <a href="#" class="dropdown-menu-item logout-btn">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                    </svg>
                    CERRAR SESIÓN
                </a>
            `;
        } else {
            dropdownMenu.innerHTML = `
                <a href="#" class="dropdown-menu-item night-mode-toggle">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                    </svg>
                    ${isNightMode ? 'MODO DÍA' : 'MODO NOCHE'}
                </a>
                <a href="./login.html" class="dropdown-menu-item">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                    </svg>
                    INICIAR SESIÓN
                </a>
                <a href="./signup.html" class="dropdown-menu-item">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                    </svg>
                    REGISTRARSE
                </a>
            `;
        }

        this.setupDynamicEventListeners();
        console.log('✅ Dropdown menu updated');
    }

    setupDynamicEventListeners() {
        // Modo noche desde dropdown
        const nightModeToggle = document.querySelector('.night-mode-toggle');
        if (nightModeToggle) {
            // Remover event listeners anteriores para evitar duplicados
            nightModeToggle.replaceWith(nightModeToggle.cloneNode(true));

            document.querySelector('.night-mode-toggle').addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleNightMode();

                // Cerrar dropdown
                const dropdownMenu = document.getElementById('dropdown-menu');
                if (dropdownMenu) {
                    dropdownMenu.classList.add('hidden');
                }
            });
        }

        // Logout
        const logoutBtn = document.querySelector('.logout-btn');
        if (logoutBtn) {
            // Remover event listeners anteriores
            logoutBtn.replaceWith(logoutBtn.cloneNode(true));

            document.querySelector('.logout-btn').addEventListener('click', (e) => {
                e.preventDefault();
                AuthService.logout();

                // Cerrar dropdown
                const dropdownMenu = document.getElementById('dropdown-menu');
                if (dropdownMenu) {
                    dropdownMenu.classList.add('hidden');
                }

                // Redirigir al home
                setTimeout(() => {
                    window.location.href = './home.html';
                }, 500);
            });
        }
    }

    createFallbackNavbar() {
        console.log('🔄 Creating fallback navbar');
        const fallbackNavbar = `
            <nav class="neo-brutalist bg-red-600 text-white p-4 mb-8">
                <div class="container mx-auto flex justify-between items-center">
                    <div class="flex items-center space-x-6">
                        <a href="./home.html" class="text-3xl font-extrabold text-yellow-400">STARTHUB</a>
                        <a href="./home.html" class="text-lg font-bold text-white">Inicio</a>
                    </div>
                    <div class="flex space-x-4 items-center">
                        <span class="text-yellow-400">Navbar Fallback</span>
                    </div>
                </div>
            </nav>
        `;
        document.body.insertAdjacentHTML('afterbegin', fallbackNavbar);
    }
}