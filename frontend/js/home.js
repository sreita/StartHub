// js/home.js
const DATA_API = 'http://localhost:8000';

export class HomePage {
    constructor() {
        this.userVotes = {};
        this.currentSort = 'newest'; // Valor por defecto
        this.init();
    }

    init() {
        console.log('Inicializando HomePage...');
        this.setupDropdown();
        this.setupNightMode();
        this.setupNavigation();
        this.setupVotingSystem();
        this.setupSearch();
        this.setupSortDropdown();
        this.loadStartups();
        this.checkAuthStatus();
    }

    setupDropdown() {
        const dropdownBtn = document.getElementById('dropdown-btn');
        const dropdownMenu = document.getElementById('dropdown-menu');

        if (dropdownBtn && dropdownMenu) {
            dropdownBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                dropdownMenu.classList.toggle('hidden');
            });

            dropdownMenu.addEventListener('click', (e) => {
                e.stopPropagation();
            });

            document.addEventListener('click', () => {
                if (!dropdownMenu.classList.contains('hidden')) {
                    dropdownMenu.classList.add('hidden');
                }
            });

            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && !dropdownMenu.classList.contains('hidden')) {
                    dropdownMenu.classList.add('hidden');
                }
            });
        }
    }

    setupSortDropdown() {
        const sortDropdownBtn = document.getElementById('sort-dropdown-btn');
        const sortDropdownMenu = document.getElementById('sort-dropdown-menu');

        if (sortDropdownBtn && sortDropdownMenu) {
            sortDropdownBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                sortDropdownMenu.classList.toggle('hidden');
            });

            // Cerrar el menú si se hace clic fuera
            document.addEventListener('click', (e) => {
                if (!sortDropdownBtn.contains(e.target) && !sortDropdownMenu.contains(e.target)) {
                    sortDropdownMenu.classList.add('hidden');
                }
            });

            // Manejar selección de opciones de ordenamiento
            const sortOptions = sortDropdownMenu.querySelectorAll('.sort-option');
            sortOptions.forEach(option => {
                option.addEventListener('click', (e) => {
                    e.preventDefault();
                    const sortType = option.dataset.sort;
                    this.handleSortChange(sortType);
                    sortDropdownMenu.classList.add('hidden');

                    // Actualizar texto del botón
                    let sortText = 'Ordenar por';
                    switch(sortType) {
                        case 'newest':
                            sortText = 'Más nuevos';
                            break;
                        case 'oldest':
                            sortText = 'Más antiguos';
                            break;
                        case 'most-voted':
                            sortText = 'Más votados';
                            break;
                    }

                    sortDropdownBtn.innerHTML = `
                        <span>${sortText}</span>
                        <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                        </svg>
                    `;
                });
            });
        }
    }

    handleSortChange(sortType) {
        this.currentSort = sortType;
        this.loadStartups(); // Recargar las startups con el nuevo orden
    }

    setupNightMode() {
        const nightModeToggle = document.getElementById('night-mode-toggle');
        if (nightModeToggle) {
            nightModeToggle.addEventListener('click', (e) => {
                e.preventDefault();
                document.body.classList.toggle('night-mode-active');

                const isNightMode = document.body.classList.contains('night-mode-active');
                localStorage.setItem('nightMode', isNightMode);

                const dropdownMenu = document.getElementById('dropdown-menu');
                if (dropdownMenu) {
                    dropdownMenu.classList.add('hidden');
                }
            });

            const savedNightMode = localStorage.getItem('nightMode') === 'true';
            if (savedNightMode) {
                document.body.classList.add('night-mode-active');
            }
        }
    }

    setupVotingSystem() {
        document.addEventListener('click', (e) => {
            if (e.target.closest('.upvote')) {
                this.handleVote(e.target.closest('.upvote'), 'up');
            } else if (e.target.closest('.downvote')) {
                this.handleVote(e.target.closest('.downvote'), 'down');
            }
        });
    }

    handleVote(button, voteType) {
        if (!this.isAuthenticated()) {
            alert('Por favor inicia sesión para votar');
            window.location.href = './login.html';
            return;
        }

        const startupId = button.dataset.startupId;
        const countSpan = document.querySelector(`.vote-count[data-startup-id="${startupId}"]`);
        const upvoteBtn = document.querySelector(`.upvote[data-startup-id="${startupId}"]`);
        const downvoteBtn = document.querySelector(`.downvote[data-startup-id="${startupId}"]`);

        let count = parseInt(countSpan.textContent);
        const currentVote = this.userVotes[startupId];

        upvoteBtn.classList.remove('active');
        downvoteBtn.classList.remove('active');

        if (currentVote === voteType) {
            count += (voteType === 'up') ? -1 : 1;
            delete this.userVotes[startupId];
        } else {
            if (currentVote === 'up') count -= 1;
            if (currentVote === 'down') count += 1;

            count += (voteType === 'up') ? 1 : -1;
            this.userVotes[startupId] = voteType;
            button.classList.add('active');
        }

        countSpan.textContent = count;
        this.saveVoteToServer(startupId, voteType, currentVote);
    }

    async saveVoteToServer(startupId, newVote, oldVote) {
        try {
            const userRaw = localStorage.getItem('user');
            if (!userRaw) return;
            const user = JSON.parse(userRaw);
            const vote_type = newVote === 'up' ? 'upvote' : 'downvote';
            await fetch(`${DATA_API}/votes/?user_id=${user.id}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ startup_id: Number(startupId), vote_type })
            });
        } catch (error) {
            console.error('Error saving vote:', error);
        }
    }

    isAuthenticated() {
        return !!localStorage.getItem('authToken');
    }

    setupNavigation() {
        this.updateAuthLinks();
    }

    checkAuthStatus() {
        const token = localStorage.getItem('authToken');
        const user = localStorage.getItem('user');

        if (token && user) {
            this.updateUIForAuthenticatedUser(JSON.parse(user));
        } else {
            this.updateUIForGuest();
        }
    }

    updateAuthLinks() {
        // Los enlaces ya están configurados en el HTML
    }

    updateUIForAuthenticatedUser(user) {
        const dropdownMenu = document.getElementById('dropdown-menu');
        if (dropdownMenu) {
            const loginLink = dropdownMenu.querySelector('a[href="./login.html"]');
            const signupLink = dropdownMenu.querySelector('a[href="./signup.html"]');

            if (loginLink && signupLink) {
                loginLink.parentElement.innerHTML = `
                    <a href="./profile.html" class="dropdown-menu-item">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                        MI PERFIL
                    </a>
                    <a href="#" class="dropdown-menu-item" id="logout-btn">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                        CERRAR SESIÓN
                    </a>
                `;

                const logoutBtn = document.getElementById('logout-btn');
                if (logoutBtn) {
                    logoutBtn.addEventListener('click', (e) => {
                        e.preventDefault();
                        this.logout();
                    });
                }
            }
        }
    }

    updateUIForGuest() {
        // Asegurar que los enlaces de login/signup estén presentes
    }

    logout() {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        window.location.href = './home.html';
    }

    setupSearch() {
        // Esperar un poco para asegurar que el DOM esté listo
        setTimeout(() => {
            const searchInput = document.getElementById('search-input');
            const searchButton = document.getElementById('search-button');

            console.log('🔍 Buscando elementos de búsqueda...');
            console.log('Input encontrado:', searchInput);
            console.log('Botón encontrado:', searchButton);

            if (searchInput && searchButton) {
                console.log('✅ Elementos de búsqueda encontrados y configurados');

                // Función para mostrar el input
                const showSearchInput = () => {
                    searchInput.classList.remove('w-0', 'opacity-0');
                    searchInput.classList.add('w-48', 'md:w-64', 'opacity-100');
                    searchInput.focus();
                };

                // Función para ocultar el input
                const hideSearchInput = () => {
                    searchInput.classList.add('w-0', 'opacity-0');
                    searchInput.classList.remove('w-48', 'md:w-64', 'opacity-100');
                    searchInput.value = '';
                };

                // Búsqueda al hacer clic en el botón
                searchButton.addEventListener('click', (e) => {
                    console.log('🖱️ Botón de búsqueda clickeado');

                    // Si el input está visible, ejecutar búsqueda
                    if (searchInput.classList.contains('opacity-100')) {
                        console.log('🔍 Ejecutando búsqueda desde el botón');
                        this.handleSearch();
                    } else {
                        // Si no está visible, mostrar el input
                        showSearchInput();
                    }
                });

                // Búsqueda al presionar Enter
                searchInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        console.log('↵ Enter presionado en búsqueda');
                        this.handleSearch();
                    }
                });

                // Ocultar el input cuando se presione Escape
                searchInput.addEventListener('keydown', (e) => {
                    if (e.key === 'Escape') {
                        hideSearchInput();
                        this.loadStartups();
                    }
                });

                // Ocultar el input cuando se haga clic fuera
                document.addEventListener('click', (e) => {
                    if (!searchInput.contains(e.target) && !searchButton.contains(e.target)) {
                        hideSearchInput();
                    }
                });

                // Búsqueda en tiempo real después de escribir
                searchInput.addEventListener('input', (e) => {
                    const query = e.target.value.trim();
                    if (query.length >= 2) {
                        console.log('⚡ Búsqueda en tiempo real:', query);
                        this.performSearch(query);
                    } else if (query.length === 0) {
                        console.log('🔄 Recargando startups (búsqueda vacía)');
                        this.loadStartups();
                    }
                });

            } else {
                console.error('❌ Elementos de búsqueda no encontrados');
                console.log('Elementos en la página:', {
                    inputs: document.querySelectorAll('input'),
                    buttons: document.querySelectorAll('button')
                });
            }
        }, 100);
    }

    handleSearch() {
        const searchInput = document.getElementById('search-input');
        const query = searchInput.value.trim();

        console.log('🔍 Ejecutando búsqueda:', query);

        if (query) {
            this.performSearch(query);
        } else {
            this.loadStartups();
        }
    }

    async performSearch(query) {
        try {
            const startupsContainer = document.getElementById('startups-container');
            startupsContainer.innerHTML = '<div class="text-center py-8">Buscando...</div>';

            const allStartups = await this.fetchStartups();
            const filteredStartups = allStartups.filter(startup =>
                startup.name.toLowerCase().includes(query.toLowerCase()) ||
                startup.description.toLowerCase().includes(query.toLowerCase()) ||
                startup.category.toLowerCase().includes(query.toLowerCase())
            );

            console.log(`✅ ${filteredStartups.length} resultados encontrados`);

            // Aplicar ordenamiento a los resultados de búsqueda
            const sortedStartups = this.sortStartups(filteredStartups, this.currentSort);
            this.renderStartups(sortedStartups);

        } catch (error) {
            console.error('❌ Error en búsqueda:', error);
            const startupsContainer = document.getElementById('startups-container');
            startupsContainer.innerHTML = '<div class="text-center py-8 text-red-500">Error en la búsqueda</div>';
        }
    }

    async loadStartups() {
        try {
            let startups = await this.fetchStartups();
            startups = this.sortStartups(startups, this.currentSort);
            this.renderStartups(startups);
        } catch (error) {
            console.error('Error loading startups:', error);
        }
    }

    // Método para ordenar startups
    sortStartups(startups, sortType) {
        const sortedStartups = [...startups]; // Crear copia para no mutar el original

        switch(sortType) {
            case 'newest':
                return sortedStartups.sort((a, b) => {
                    // Ordenar por fecha más reciente primero
                    return new Date(b.created_date) - new Date(a.created_date);
                });

            case 'oldest':
                return sortedStartups.sort((a, b) => {
                    // Ordenar por fecha más antigua primero
                    return new Date(a.created_date) - new Date(b.created_date);
                });

            case 'most-voted':
                return sortedStartups.sort((a, b) => {
                    // Ordenar por más votos primero
                    return b.votes - a.votes;
                });

            default:
                return sortedStartups;
        }
    }

    async fetchStartups() {
        const res = await fetch(`${DATA_API}/startups/?skip=0&limit=50`);
        if (!res.ok) throw new Error('No se pudieron cargar las startups');
        const items = await res.json();
        // Enriquecer con votos (upvotes - downvotes)
        const withVotes = await Promise.all(items.map(async (s) => {
            try {
                const vc = await fetch(`${DATA_API}/votes/count/${s.startup_id}`);
                let votes = 0;
                if (vc.ok) {
                    const data = await vc.json();
                    votes = (data.upvotes || 0) - (data.downvotes || 0);
                }
                return {
                    id: s.startup_id,
                    name: s.name,
                    description: s.description || '',
                    email: '',
                    website: '',
                    social_media: '',
                    category: s.category_id ? `Categoría ${s.category_id}` : 'General',
                    created_date: s.created_date || new Date().toISOString(),
                    votes,
                };
            } catch (e) {
                return {
                    id: s.startup_id,
                    name: s.name,
                    description: s.description || '',
                    email: '',
                    website: '',
                    social_media: '',
                    category: s.category_id ? `Categoría ${s.category_id}` : 'General',
                    created_date: s.created_date || new Date().toISOString(),
                    votes: 0,
                };
            }
        }));
        return withVotes;
    }

    renderStartups(startups) {
    const container = document.getElementById('startups-container');
    if (!container) {
        console.error('❌ Contenedor de startups no encontrado');
        return;
    }

    container.innerHTML = startups.map(startup => `
        <div class="startup-card bg-white neo-brutalist rounded-lg shadow-md transition duration-300 ease-in-out flex mb-8">
            <!-- Sección de votos - más compacta -->
            <div class="flex flex-col items-center justify-start vote-container flex-shrink-0">
                <button class="vote-btn upvote mb-1" data-startup-id="${startup.id}">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                    </svg>
                </button>
                <span class="vote-count text-base font-bold my-1" data-startup-id="${startup.id}">${startup.votes}</span>
                <button class="vote-btn downvote mt-1" data-startup-id="${startup.id}">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </button>
            </div>

            <!-- Contenido principal -->
            <div class="p-4 flex-grow flex flex-col border-l-2 border-black min-h-0">
                <!-- Header con nombre y categoría -->
                <div class="flex justify-between items-start mb-3 flex-shrink-0">
                    <h2 class="text-xl font-bold text-gray-900">${startup.name}</h2>
                    <span class="category-badge bg-black text-white px-3 py-1 rounded-full text-xs font-bold">
                        ${startup.category}
                    </span>
                </div>

                <!-- Descripción -->
                <p class="text-gray-700 text-sm leading-relaxed mb-4 flex-grow">
                    ${startup.description}
                </p>

                <!-- Información de contacto y botón - SIEMPRE VISIBLE -->
                <div class="flex items-center justify-between pt-3 border-t border-gray-300 flex-shrink-0 bg-white">
                    <div class="flex items-center space-x-3 text-xs text-gray-600">
                        ${startup.email ? `<span class="flex items-center whitespace-nowrap bg-gray-100 px-2 py-1 rounded">
                            <svg class="w-3 h-3 mr-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                            </svg>
                            <span class="truncate" style="max-width: 100px;">${startup.email}</span>
                        </span>` : ''}
                        ${startup.website ? `<span class="flex items-center whitespace-nowrap bg-gray-100 px-2 py-1 rounded">
                            <svg class="w-3 h-3 mr-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9"/>
                            </svg>
                            Sitio web
                        </span>` : ''}
                    </div>

                    <div class="flex items-center space-x-3 ml-2">
                        <span class="text-xs text-gray-700 date-text whitespace-nowrap bg-gray-100 px-2 py-1 rounded">
                            ${this.formatDate(startup.created_date)}
                        </span>
                        <a href="./startup_info.html?id=${startup.id}"
                           class="read-more text-black bg-yellow-400 py-2 px-3 rounded font-bold text-xs transition-all duration-200 hover:scale-105">
                            DETALLES »
                        </a>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

    formatDate(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        const date = new Date(dateString);
        return date.toLocaleDateString('es-ES', options);
    }
}