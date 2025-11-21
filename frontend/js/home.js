// js/home.js
export class HomePage {
    constructor() {
        this.userVotes = {};
        this.init();
    }

    init() {
        console.log('Inicializando HomePage...');
        this.setupDropdown();
        this.setupNightMode();
        this.setupNavigation();
        this.setupVotingSystem();
        this.setupSearch();
        this.loadPosts();
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

        const postId = button.dataset.postId;
        const countSpan = document.querySelector(`.vote-count[data-post-id="${postId}"]`);
        const upvoteBtn = document.querySelector(`.upvote[data-post-id="${postId}"]`);
        const downvoteBtn = document.querySelector(`.downvote[data-post-id="${postId}"]`);

        let count = parseInt(countSpan.textContent);
        const currentVote = this.userVotes[postId];

        upvoteBtn.classList.remove('active');
        downvoteBtn.classList.remove('active');

        if (currentVote === voteType) {
            count += (voteType === 'up') ? -1 : 1;
            delete this.userVotes[postId];
        } else {
            if (currentVote === 'up') count -= 1;
            if (currentVote === 'down') count += 1;

            count += (voteType === 'up') ? 1 : -1;
            this.userVotes[postId] = voteType;
            button.classList.add('active');
        }

        countSpan.textContent = count;
        this.saveVoteToServer(postId, voteType, currentVote);
    }

    async saveVoteToServer(postId, newVote, oldVote) {
        try {
            // Integrar con tu API de votos aquí
            console.log(`Voto guardado: Post ${postId}, Voto: ${newVote}, Anterior: ${oldVote}`);
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
                        this.loadPosts();
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
                        console.log('🔄 Recargando posts (búsqueda vacía)');
                        this.loadPosts();
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
            this.loadPosts();
        }
    }

    async performSearch(query) {
        try {
            const postsContainer = document.getElementById('posts-container');
            postsContainer.innerHTML = '<div class="text-center py-8">Buscando...</div>';

            const allPosts = await this.fetchPosts();
            const filteredPosts = allPosts.filter(post =>
                post.title.toLowerCase().includes(query.toLowerCase()) ||
                post.content.toLowerCase().includes(query.toLowerCase())
            );

            console.log(`✅ ${filteredPosts.length} resultados encontrados`);
            this.renderPosts(filteredPosts);

        } catch (error) {
            console.error('❌ Error en búsqueda:', error);
            const postsContainer = document.getElementById('posts-container');
            postsContainer.innerHTML = '<div class="text-center py-8 text-red-500">Error en la búsqueda</div>';
        }
    }

    async loadPosts() {
        try {
            const posts = await this.fetchPosts();
            this.renderPosts(posts);
        } catch (error) {
            console.error('Error loading posts:', error);
        }
    }

    async fetchPosts() {
        // Datos de ejemplo
        return [
            {
                id: 1,
                title: "Responsive Web Design",
                content: "Learn how to create responsive web designs that look great on all devices.",
                image: "https://media.geeksforgeeks.org/wp-content/uploads/20240117155347/responsive-web-design-copy.webp",
                date: "March 21, 2024",
                votes: 12
            },
            {
                id: 2,
                title: "JavaScript Fundamentals",
                content: "Get started with JavaScript and master the fundamentals of this powerful programming language.",
                image: "https://media.geeksforgeeks.org/wp-content/uploads/20230809133232/JavaScript-Complete-Guide-copy-2.webp",
                date: "March 18, 2024",
                votes: 5
            },
            {
                id: 3,
                title: "CSS Flexbox Tutorial",
                content: "Learn how to use CSS Flexbox to create flexible layouts with ease.",
                image: "https://media.geeksforgeeks.org/wp-content/uploads/20240507112025/75s2.png",
                date: "March 15, 2024",
                votes: 24
            }
        ];
    }

    renderPosts(posts) {
        const container = document.getElementById('posts-container');
        if (!container) {
            console.error('❌ Contenedor de posts no encontrado');
            return;
        }

        container.innerHTML = posts.map(post => `
            <div class="blog-post bg-white neo-brutalist rounded-lg overflow-hidden shadow-md transition duration-300 ease-in-out flex">
                <div class="flex flex-col items-center justify-start vote-container flex-shrink-0">
                    <button class="vote-btn upvote" data-post-id="${post.id}">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                        </svg>
                    </button>
                    <span class="vote-count text-lg font-bold my-1" data-post-id="${post.id}">${post.votes}</span>
                    <button class="vote-btn downvote" data-post-id="${post.id}">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                        </svg>
                    </button>
                </div>
                <img src="${post.image}" alt="${post.title}" class="w-64 h-32 object-cover rounded-l-sm flex-shrink-0">
                <div class="p-6 flex-grow border-l-4 border-black">
                    <h2 class="text-2xl font-semibold mb-2">${post.title}</h2>
                    <p class="text-gray-700 mb-4 text-base">${post.content}</p>
                    <div class="flex items-center justify-between mt-2">
                        <p class="text-sm text-gray-700 date-text">${post.date}</p>
                        <a href="./post-detail.html?id=${post.id}" class="text-black bg-yellow-400 py-1 px-3 border-2 border-black hover:bg-black hover:text-yellow-400 read-more">
                            LEER MÁS »
                        </a>
                    </div>
                </div>
            </div>
        `).join('');
    }
}