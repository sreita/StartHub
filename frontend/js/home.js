// js/home.js
export class HomePage {
    constructor() {
        this.init();
    }

    init() {
        this.setupDropdown();
        this.setupNightMode();
        this.setupNavigation();
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

            // Prevenir que el menú se cierre al hacer clic dentro de él
            dropdownMenu.addEventListener('click', (e) => {
                e.stopPropagation();
            });

            // Cerrar menú al hacer clic fuera
            document.addEventListener('click', () => {
                if (!dropdownMenu.classList.contains('hidden')) {
                    dropdownMenu.classList.add('hidden');
                }
            });

            // También cerrar con la tecla Escape
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

                // Cerrar el menú después de seleccionar
                const dropdownMenu = document.getElementById('dropdown-menu');
                if (dropdownMenu) {
                    dropdownMenu.classList.add('hidden');
                }
            });
        }
    }

    setupNavigation() {
        // Verificar autenticación y actualizar enlaces
        this.updateAuthLinks();
    }

    checkAuthStatus() {
        // Verificar si el usuario está autenticado
        const token = localStorage.getItem('authToken');
        const user = localStorage.getItem('user');

        if (token && user) {
            this.updateUIForAuthenticatedUser(JSON.parse(user));
        } else {
            this.updateUIForGuest();
        }
    }

    updateAuthLinks() {
        const loginLink = document.querySelector('a[href="./login.html"]');
        const signupLink = document.querySelector('a[href="./signup.html"]');

        if (loginLink && signupLink) {
            // Estos enlaces ya están correctos en el HTML
            console.log('Enlaces de autenticación configurados');
        }
    }

    updateUIForAuthenticatedUser(user) {
        const dropdownMenu = document.getElementById('dropdown-menu');
        if (dropdownMenu) {
            // Reemplazar opciones de login/signup por opciones de usuario
            const authSection = dropdownMenu.querySelector('a[href="./login.html"]')?.closest('.dropdown-menu-item')?.nextElementSibling;

            if (authSection) {
                authSection.innerHTML = `
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

                // Agregar evento para cerrar sesión
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
        // Asegurarse de que los enlaces de login/signup estén presentes
        const dropdownMenu = document.getElementById('dropdown-menu');
        if (dropdownMenu) {
            const existingLogin = dropdownMenu.querySelector('a[href="./login.html"]');
            const existingSignup = dropdownMenu.querySelector('a[href="./signup.html"]');

            if (!existingLogin || !existingSignup) {
                // Restaurar enlaces si faltan
                const authSection = dropdownMenu.querySelector('.dropdown-menu-item:last-child');
                if (authSection) {
                    authSection.outerHTML = `
                        <a href="./login.html" class="dropdown-menu-item">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                            </svg>
                            INICIAR SESIÓN
                        </a>
                        <a href="./signup.html" class="dropdown-menu-item">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                            </svg>
                            REGISTRARSE
                        </a>
                    `;
                }
            }
        }
    }

    logout() {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        window.location.href = './home.html';
    }

    async loadPosts() {
        try {
            // Aquí integrarías con tu API de posts
            const posts = await this.fetchPosts();
            this.renderPosts(posts);
        } catch (error) {
            console.error('Error loading posts:', error);
        }
    }

    async fetchPosts() {
        // Ejemplo de llamada a la API
        // const response = await fetch('http://localhost:8080/api/posts');
        // return await response.json();

        // Datos de ejemplo por ahora
        return [
            {
                id: 1,
                title: "Responsive Web Design",
                content: "Learn how to create responsive web designs that look great on all devices.",
                image: "https://media.geeksforgeeks.org/wp-content/uploads/20240117155347/responsive-web-design-copy.webp",
                date: "March 21, 2024"
            },
            {
                id: 2,
                title: "JavaScript Fundamentals",
                content: "Get started with JavaScript and master the fundamentals of this powerful programming language.",
                image: "https://media.geeksforgeeks.org/wp-content/uploads/20230809133232/JavaScript-Complete-Guide-copy-2.webp",
                date: "March 18, 2024"
            }
        ];
    }

    renderPosts(posts) {
        const container = document.getElementById('posts-container');
        if (!container) return;

        container.innerHTML = posts.map(post => `
            <div class="blog-post bg-white neo-brutalist rounded-lg overflow-hidden shadow-md transition duration-300 ease-in-out flex">
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