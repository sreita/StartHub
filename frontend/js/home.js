// js/home.js
const DATA_API = 'http://localhost:8000';

export class HomePage {
    constructor() {
        this.userVotes = {};
        this.currentSort = 'newest';
        this.init();
    }

    async init() {
        console.log('Inicializando HomePage...');
        this.setupDropdown();
        this.setupNightMode();
        this.setupNavigation();
        this.setupVotingSystem();
        this.setupSearch();
        this.setupSortDropdown();
        this.checkAuthStatus();

        // Cargar votos primero, luego startups
        await this.loadUserVotes();
        await this.loadStartups();

        console.log('HomePage inicializada completamente');
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

            document.addEventListener('click', (e) => {
                if (!sortDropdownBtn.contains(e.target) && !sortDropdownMenu.contains(e.target)) {
                    sortDropdownMenu.classList.add('hidden');
                }
            });

            const sortOptions = sortDropdownMenu.querySelectorAll('.sort-option');
            sortOptions.forEach(option => {
                option.addEventListener('click', (e) => {
                    e.preventDefault();
                    const sortType = option.dataset.sort;
                    this.handleSortChange(sortType);
                    sortDropdownMenu.classList.add('hidden');

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
        this.loadStartups();
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

    async handleVote(button, voteType) {
        if (!this.isAuthenticated()) {
            alert('Por favor inicia sesión para votar');
            window.location.href = './login.html';
            return;
        }

        const startupId = button.dataset.startupId;
        console.log('Procesando voto:', { startupId, voteType, currentVotes: this.userVotes });

        const upvoteBtn = document.querySelector(`.upvote[data-startup-id="${startupId}"]`);
        const downvoteBtn = document.querySelector(`.downvote[data-startup-id="${startupId}"]`);
        const countSpan = document.querySelector(`.vote-count[data-startup-id="${startupId}"]`);

        if (!countSpan || !upvoteBtn || !downvoteBtn) {
            console.error('Elementos de voto no encontrados para startup:', startupId);
            return;
        }

        const currentVote = this.userVotes[startupId];
        const isUpvote = voteType === 'up';
        const newVoteType = isUpvote ? 'upvote' : 'downvote';

        console.log('Estado actual del voto:', currentVote);
        console.log('Nuevo voto:', newVoteType);

        let shouldUpdate = false;
        let voteChange = 0;

        // Lógica de votación
        if (!currentVote) {
            // Nuevo voto
            this.userVotes[startupId] = newVoteType;
            voteChange = isUpvote ? 1 : -1;
            shouldUpdate = true;
            console.log('Nuevo voto registrado');
        } else if (currentVote === newVoteType) {
            // Quitar voto existente
            delete this.userVotes[startupId];
            voteChange = isUpvote ? -1 : 1;
            shouldUpdate = true;
            console.log('Voto eliminado');
        } else {
            // Cambiar de upvote a downvote o viceversa
            this.userVotes[startupId] = newVoteType;
            voteChange = isUpvote ? 2 : -2;
            shouldUpdate = true;
            console.log('Voto cambiado');
        }

        if (shouldUpdate) {
            // Actualizar UI inmediatamente
            this.updateVoteUI(startupId, currentVote, newVoteType, voteChange);

            // Enviar al servidor
            try {
                await this.saveVoteToServer(startupId, this.userVotes[startupId] || null);
                console.log('Voto guardado en servidor exitosamente');

                // Verificar sincronización
                await this.verifyVoteSync(startupId);

            } catch (error) {
                console.error('Error al procesar voto:', error);
                alert('Error al registrar el voto');
                // Revertir cambios en caso de error
                this.revertVoteUI(startupId, currentVote, voteChange);
            }
        }
    }

    updateVoteUI(startupId, previousVote, newVote, voteChange) {
        const upvoteBtn = document.querySelector(`.upvote[data-startup-id="${startupId}"]`);
        const downvoteBtn = document.querySelector(`.downvote[data-startup-id="${startupId}"]`);
        const countSpan = document.querySelector(`.vote-count[data-startup-id="${startupId}"]`);

        if (!countSpan || !upvoteBtn || !downvoteBtn) return;

        // Actualizar contador visual inmediatamente
        const currentCount = parseInt(countSpan.textContent) || 0;
        countSpan.textContent = currentCount + voteChange;

        // Resetear estilos de ambos botones
        upvoteBtn.classList.remove('active', 'bg-green-500', 'text-white', 'border-green-500');
        downvoteBtn.classList.remove('active', 'bg-red-500', 'text-white', 'border-red-500');

        // Aplicar estilos base
        upvoteBtn.classList.add('border', 'border-gray-300', 'hover:bg-gray-100');
        downvoteBtn.classList.add('border', 'border-gray-300', 'hover:bg-gray-100');

        // Aplicar estilos activos según el voto actual
        if (newVote === 'upvote') {
            upvoteBtn.classList.add('active', 'bg-green-500', 'text-white', 'border-green-500');
            upvoteBtn.classList.remove('border-gray-300', 'hover:bg-gray-100');
        } else if (newVote === 'downvote') {
            downvoteBtn.classList.add('active', 'bg-red-500', 'text-white', 'border-red-500');
            downvoteBtn.classList.remove('border-gray-300', 'hover:bg-gray-100');
        }

        console.log(`UI actualizada para startup ${startupId}: ${newVote}`);
    }

    revertVoteUI(startupId, previousVote, voteChange) {
        const countSpan = document.querySelector(`.vote-count[data-startup-id="${startupId}"]`);
        if (countSpan) {
            const currentCount = parseInt(countSpan.textContent) || 0;
            countSpan.textContent = currentCount - voteChange;
        }

        // Restaurar estado anterior de votos
        if (previousVote) {
            this.userVotes[startupId] = previousVote;
        } else {
            delete this.userVotes[startupId];
        }

        this.updateVoteButtons();
    }

    async saveVoteToServer(startupId, voteType) {
        const userRaw = localStorage.getItem('user');
        if (!userRaw) throw new Error('Usuario no autenticado');

        const user = JSON.parse(userRaw);
        let response;

        try {
            if (voteType === null) {
                // Eliminar voto
                response = await fetch(
                    `${DATA_API}/votes/?user_id=${user.id}&startup_id=${startupId}`,
                    {
                        method: 'DELETE',
                        headers: { 'Content-Type': 'application/json' }
                    }
                );
            } else {
                // Crear o actualizar voto
                response = await fetch(`${DATA_API}/votes/?user_id=${user.id}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        startup_id: parseInt(startupId),
                        vote_type: voteType
                    })
                });
            }

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }

            return true;
        } catch (error) {
            console.error('Error en saveVoteToServer:', error);
            throw error;
        }
    }

    async verifyVoteSync(startupId) {
        try {
            const serverCount = await this.getServerVoteCount(startupId);
            const countSpan = document.querySelector(`.vote-count[data-startup-id="${startupId}"]`);

            if (countSpan && serverCount !== null) {
                const localCount = parseInt(countSpan.textContent);
                if (localCount !== serverCount) {
                    countSpan.textContent = serverCount;
                    console.log(`Sincronizado voto para startup ${startupId}: local=${localCount}, servidor=${serverCount}`);
                }
            }
        } catch (error) {
            console.error('Error en verificación de sincronización:', error);
        }
    }

    async getServerVoteCount(startupId) {
        try {
            const response = await fetch(`${DATA_API}/votes/count/${startupId}`);
            if (response.ok) {
                const data = await response.json();
                return (data.upvotes || 0) - (data.downvotes || 0);
            }
        } catch (error) {
            console.error('Error obteniendo conteo del servidor:', error);
        }
        return null;
    }

    async updateVoteCount(startupId) {
        try {
            const response = await fetch(`${DATA_API}/votes/count/${startupId}`);
            if (response.ok) {
                const voteData = await response.json();
                const countSpan = document.querySelector(`.vote-count[data-startup-id="${startupId}"]`);
                if (countSpan) {
                    const totalVotes = (voteData.upvotes || 0) - (voteData.downvotes || 0);
                    countSpan.textContent = totalVotes;
                }
            }
        } catch (error) {
            console.error('Error updating vote count:', error);
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
        setTimeout(() => {
            const searchInput = document.getElementById('search-input');
            const searchButton = document.getElementById('search-button');

            console.log('🔍 Buscando elementos de búsqueda...');
            console.log('Input encontrado:', searchInput);
            console.log('Botón encontrado:', searchButton);

            if (searchInput && searchButton) {
                console.log('✅ Elementos de búsqueda encontrados y configurados');

                const showSearchInput = () => {
                    searchInput.classList.remove('w-0', 'opacity-0');
                    searchInput.classList.add('w-48', 'md:w-64', 'opacity-100');
                    searchInput.focus();
                };

                const hideSearchInput = () => {
                    searchInput.classList.add('w-0', 'opacity-0');
                    searchInput.classList.remove('w-48', 'md:w-64', 'opacity-100');
                    searchInput.value = '';
                };

                searchButton.addEventListener('click', (e) => {
                    console.log('🖱️ Botón de búsqueda clickeado');
                    if (searchInput.classList.contains('opacity-100')) {
                        console.log('🔍 Ejecutando búsqueda desde el botón');
                        this.handleSearch();
                    } else {
                        showSearchInput();
                    }
                });

                searchInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        console.log('↵ Enter presionado en búsqueda');
                        this.handleSearch();
                    }
                });

                searchInput.addEventListener('keydown', (e) => {
                    if (e.key === 'Escape') {
                        hideSearchInput();
                        this.loadStartups();
                    }
                });

                document.addEventListener('click', (e) => {
                    if (!searchInput.contains(e.target) && !searchButton.contains(e.target)) {
                        hideSearchInput();
                    }
                });

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

    sortStartups(startups, sortType) {
        const sortedStartups = [...startups];

        switch(sortType) {
            case 'newest':
                return sortedStartups.sort((a, b) => {
                    return new Date(b.created_date) - new Date(a.created_date);
                });
            case 'oldest':
                return sortedStartups.sort((a, b) => {
                    return new Date(a.created_date) - new Date(b.created_date);
                });
            case 'most-voted':
                return sortedStartups.sort((a, b) => {
                    return b.votes - a.votes;
                });
            default:
                return sortedStartups;
        }
    }

    async loadUserVotes() {
        if (!this.isAuthenticated()) {
            console.log('Usuario no autenticado, no hay votos que cargar');
            this.userVotes = {};
            return;
        }

        try {
            const userRaw = localStorage.getItem('user');
            if (!userRaw) {
                console.log('No se encontró información del usuario en localStorage');
                return;
            }

            const user = JSON.parse(userRaw);
            console.log('Cargando votos para usuario:', user.id);

            const response = await fetch(`${DATA_API}/votes/user/${user.id}`);
            if (response.ok) {
                const userVotes = await response.json();
                console.log('Votos recibidos del servidor:', userVotes);

                this.userVotes = {};
                userVotes.forEach(vote => {
                    this.userVotes[vote.startup_id] = vote.vote_type;
                    console.log(`Voto encontrado: startup ${vote.startup_id} -> ${vote.vote_type}`);
                });

                console.log('Estado final de userVotes:', this.userVotes);
            } else {
                console.error('Error cargando votos:', response.status);
            }
        } catch (error) {
            console.error('Error loading user votes:', error);
            this.userVotes = {};
        }
    }

    updateVoteButtons() {
        console.log('Actualizando botones de voto con estado:', this.userVotes);

        Object.keys(this.userVotes).forEach(startupId => {
            const voteType = this.userVotes[startupId];
            const upvoteBtn = document.querySelector(`.upvote[data-startup-id="${startupId}"]`);
            const downvoteBtn = document.querySelector(`.downvote[data-startup-id="${startupId}"]`);

            if (upvoteBtn && downvoteBtn) {
                // Resetear ambos botones
                upvoteBtn.classList.remove('active', 'bg-green-500', 'text-white', 'border-green-500');
                downvoteBtn.classList.remove('active', 'bg-red-500', 'text-white', 'border-red-500');

                // Aplicar estilos base
                upvoteBtn.classList.add('border', 'border-gray-300', 'hover:bg-gray-100');
                downvoteBtn.classList.add('border', 'border-gray-300', 'hover:bg-gray-100');

                // Activar el botón correspondiente
                if (voteType === 'upvote') {
                    upvoteBtn.classList.add('active', 'bg-green-500', 'text-white', 'border-green-500');
                    upvoteBtn.classList.remove('border-gray-300', 'hover:bg-gray-100');
                } else if (voteType === 'downvote') {
                    downvoteBtn.classList.add('active', 'bg-red-500', 'text-white', 'border-red-500');
                    downvoteBtn.classList.remove('border-gray-300', 'hover:bg-gray-100');
                }

                console.log(`Botones actualizados para startup ${startupId}: ${voteType}`);
            } else {
                console.log(`Botones no encontrados para startup ${startupId}`);
            }
        });
    }

    async fetchStartups() {
        const res = await fetch(`${DATA_API}/startups/?skip=0&limit=50`);
        if (!res.ok) throw new Error('No se pudieron cargar las startups');
        const items = await res.json();

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
                    email: s.email || '',
                    website: s.website || '',
                    social_media: s.social_media || '',
                    category: s.category_name || (s.category_id ? `Categoría ${s.category_id}` : 'General'),
                    created_date: s.created_date || new Date().toISOString(),
                    votes,
                };
            } catch (e) {
                console.error('Error loading votes for startup:', s.startup_id, e);
                return {
                    id: s.startup_id,
                    name: s.name,
                    description: s.description || '',
                    email: s.email || '',
                    website: s.website || '',
                    social_media: s.social_media || '',
                    category: s.category_name || (s.category_id ? `Categoría ${s.category_id}` : 'General'),
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

        container.innerHTML = startups.map(startup => {
            const userVote = this.userVotes[startup.id];
            const upvoteClass = userVote === 'upvote' ? 'active bg-green-500 text-white border-green-500' : 'border border-gray-300 hover:bg-gray-100';
            const downvoteClass = userVote === 'downvote' ? 'active bg-red-500 text-white border-red-500' : 'border border-gray-300 hover:bg-gray-100';

            console.log(`Renderizando startup ${startup.id}, voto del usuario:`, userVote);

            return `
            <div class="startup-card bg-white neo-brutalist rounded-lg shadow-md transition duration-300 ease-in-out flex mb-8">
                <!-- Sección de votos -->
                <div class="flex flex-col items-center justify-start vote-container flex-shrink-0 p-3">
                    <button class="vote-btn upvote mb-1 rounded p-2 transition-colors ${upvoteClass}"
                            data-startup-id="${startup.id}">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                        </svg>
                    </button>
                    <span class="vote-count text-base font-bold my-1" data-startup-id="${startup.id}">${startup.votes}</span>
                    <button class="vote-btn downvote mt-1 rounded p-2 transition-colors ${downvoteClass}"
                            data-startup-id="${startup.id}">
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

                    <!-- Información de contacto y botón -->
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
            `;
        }).join('');

        // Aplicar estilos de votos después de renderizar
        setTimeout(() => {
            this.updateVoteButtons();
        }, 50);
    }

    formatDate(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        const date = new Date(dateString);
        return date.toLocaleDateString('es-ES', options);
    }
}