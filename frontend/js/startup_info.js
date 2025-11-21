// js/startup_info.js
export class StartupInfoPage {
    constructor() {
        this.startupId = this.getStartupIdFromURL();
        this.currentUser = null;
        this.userVote = null;
        this.init();
    }

    init() {
        console.log('Inicializando StartupInfoPage...');
        this.checkAuthStatus();
        this.loadStartupData();
        this.setupEventListeners();
        this.setupNightMode();
        this.setupDropdown();
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
            this.updateUIForAuthenticatedUser();
        }
    }

    updateUIForAuthenticatedUser() {
        // Habilitar funcionalidades para usuarios autenticados
        const commentForm = document.getElementById('comment-form');
        if (commentForm) {
            commentForm.style.display = 'block';
        }
    }

    async loadStartupData() {
        try {
            const startup = await this.fetchStartupById(this.startupId);
            this.renderStartupInfo(startup);

            // Cargar datos adicionales
            await this.loadVotes();
            await this.loadComments();
            await this.loadPartners();

        } catch (error) {
            console.error('Error loading startup data:', error);
            this.showError('Error al cargar la información de la startup');
        }
    }

    async fetchStartupById(startupId) {
        // Simulación de datos - reemplazar con llamada real a la API
        return {
            startup_id: startupId,
            name: "TechInnovate",
            description: "Una startup dedicada a la innovación tecnológica en el campo de la inteligencia artificial y machine learning. Desarrollamos soluciones personalizadas para empresas que buscan transformar digitalmente sus operaciones.",
            email: "contact@techinnovate.com",
            website: "https://techinnovate.com",
            social_media: "@techinnovate",
            created_date: "2024-03-21",
            owner_user_id: 1,
            category_id: 1,
            category_name: "Tecnología",
            owner_name: "Ana García"
        };
    }

    renderStartupInfo(startup) {
        const container = document.getElementById('startup-info');
        container.innerHTML = `
            <div class="flex justify-between items-start mb-6">
                <h1 class="text-4xl md:text-5xl font-bold">${startup.name}</h1>
                <span class="bg-yellow-400 text-black px-3 py-1 border-2 border-black font-bold">${startup.category_name}</span>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div class="lg:col-span-2">
                    <h2 class="text-2xl font-bold mb-4">Descripción</h2>
                    <p class="text-gray-700 text-lg leading-relaxed">${startup.description}</p>
                </div>

                <div class="bg-gray-50 p-6 border-2 border-black">
                    <h3 class="text-xl font-bold mb-4">Información de Contacto</h3>
                    <div class="space-y-3">
                        ${startup.email ? `<p><strong>Email:</strong> <a href="mailto:${startup.email}" class="text-blue-600 hover:underline">${startup.email}</a></p>` : ''}
                        ${startup.website ? `<p><strong>Website:</strong> <a href="${startup.website}" target="_blank" class="text-blue-600 hover:underline">${startup.website}</a></p>` : ''}
                        ${startup.social_media ? `<p><strong>Redes Sociales:</strong> ${startup.social_media}</p>` : ''}
                        <p><strong>Fundador:</strong> ${startup.owner_name}</p>
                        <p><strong>Fecha de creación:</strong> ${new Date(startup.created_date).toLocaleDateString('es-ES')}</p>
                    </div>
                </div>
            </div>
        `;
    }

    async loadVotes() {
        try {
            const votes = await this.fetchVotes(this.startupId);
            const userVote = await this.fetchUserVote(this.startupId);

            this.updateVoteDisplay(votes, userVote);
        } catch (error) {
            console.error('Error loading votes:', error);
        }
    }

    async fetchVotes(startupId) {
        // Simulación - reemplazar con llamada real a la API
        return {
            upvotes: 15,
            downvotes: 3,
            total: 12
        };
    }

    async fetchUserVote(startupId) {
        if (!this.currentUser) return null;

        // Simulación - reemplazar con llamada real a la API
        return null; // o 'upvote' o 'downvote'
    }

    updateVoteDisplay(votes, userVote) {
        const voteCount = document.getElementById('vote-count');
        const voteStatus = document.getElementById('vote-status');
        const upvoteBtn = document.getElementById('upvote-btn');
        const downvoteBtn = document.getElementById('downvote-btn');

        voteCount.textContent = votes.total;

        if (userVote === 'upvote') {
            upvoteBtn.classList.add('active', 'bg-green-500', 'text-white');
            voteStatus.textContent = 'Has votado positivamente';
        } else if (userVote === 'downvote') {
            downvoteBtn.classList.add('active', 'bg-red-500', 'text-white');
            voteStatus.textContent = 'Has votado negativamente';
        } else if (!this.currentUser) {
            voteStatus.textContent = 'Inicia sesión para votar';
            upvoteBtn.disabled = true;
            downvoteBtn.disabled = true;
        } else {
            voteStatus.textContent = 'Vota esta startup';
        }
    }

    async loadComments() {
        try {
            const comments = await this.fetchComments(this.startupId);
            this.renderComments(comments);
        } catch (error) {
            console.error('Error loading comments:', error);
        }
    }

    async fetchComments(startupId) {
        // Simulación - reemplazar con llamada real a la API
        return [
            {
                comment_id: 1,
                content: "¡Excelente proyecto! Me encanta el enfoque en IA responsable.",
                created_date: "2024-03-22T10:30:00",
                user_name: "Carlos Rodríguez",
                user_id: 2
            },
            {
                comment_id: 2,
                content: "Interesante propuesta de valor. ¿Tienen planes de expansión internacional?",
                created_date: "2024-03-21T15:45:00",
                user_name: "María López",
                user_id: 3
            }
        ];
    }

    renderComments(comments) {
        const container = document.getElementById('comments-list');
        const countElement = document.getElementById('comment-count');

        countElement.textContent = comments.length;

        if (comments.length === 0) {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">No hay comentarios todavía. ¡Sé el primero en comentar!</p>';
            return;
        }

        container.innerHTML = comments.map(comment => `
            <div class="border-b-2 border-black pb-4 mb-4 last:border-b-0 last:mb-0">
                <div class="flex justify-between items-start mb-2">
                    <strong class="text-lg">${comment.user_name}</strong>
                    <span class="text-sm text-gray-600">${new Date(comment.created_date).toLocaleDateString('es-ES')}</span>
                </div>
                <p class="text-gray-700">${comment.content}</p>
                ${this.currentUser && this.currentUser.user_id === comment.user_id ? `
                    <div class="mt-2">
                        <button class="text-red-600 text-sm hover:underline" onclick="startupInfoPage.deleteComment(${comment.comment_id})">
                            Eliminar
                        </button>
                    </div>
                ` : ''}
            </div>
        `).join('');
    }

    async loadPartners() {
        try {
            const partners = await this.fetchPartners(this.startupId);
            this.renderPartners(partners);
        } catch (error) {
            console.error('Error loading partners:', error);
        }
    }

    async fetchPartners(startupId) {
        // Simulación - reemplazar con llamada real a la API
        return [
            {
                user_id: 1,
                user_name: "Ana García",
                role: "Fundadora & CEO",
                partnership_date: "2024-01-15"
            },
            {
                user_id: 4,
                user_name: "David Chen",
                role: "CTO",
                partnership_date: "2024-02-01"
            }
        ];
    }

    renderPartners(partners) {
        const container = document.getElementById('partners-list');
        const countElement = document.getElementById('partner-count');

        countElement.textContent = partners.length;

        container.innerHTML = partners.map(partner => `
            <div class="flex justify-between items-center border-b-2 border-black pb-4 mb-4 last:border-b-0 last:mb-0">
                <div>
                    <strong class="text-lg">${partner.user_name}</strong>
                    <p class="text-gray-600">${partner.role}</p>
                    <p class="text-sm text-gray-500">Se unió el ${new Date(partner.partnership_date).toLocaleDateString('es-ES')}</p>
                </div>
                ${this.currentUser && this.currentUser.user_id === partner.user_id ? `
                    <button class="text-red-600 hover:underline" onclick="startupInfoPage.leavePartnership(${partner.user_id})">
                        Abandonar
                    </button>
                ` : ''}
            </div>
        `).join('');
    }

    setupEventListeners() {
        // Votación
        document.getElementById('upvote-btn').addEventListener('click', () => this.handleVote('upvote'));
        document.getElementById('downvote-btn').addEventListener('click', () => this.handleVote('downvote'));

        // Comentarios
        document.getElementById('comment-form').addEventListener('submit', (e) => this.handleCommentSubmit(e));
    }

    async handleVote(voteType) {
        if (!this.currentUser) {
            alert('Por favor inicia sesión para votar');
            window.location.href = './login.html';
            return;
        }

        try {
            await this.submitVote(voteType);
            await this.loadVotes(); // Recargar votos
        } catch (error) {
            console.error('Error submitting vote:', error);
            this.showError('Error al registrar el voto');
        }
    }

    async submitVote(voteType) {
        // Simulación - reemplazar con llamada real a la API
        console.log(`Enviando voto ${voteType} para startup ${this.startupId}`);
        return new Promise(resolve => setTimeout(resolve, 500));
    }

    async handleCommentSubmit(e) {
        e.preventDefault();

        if (!this.currentUser) {
            alert('Por favor inicia sesión para comentar');
            window.location.href = './login.html';
            return;
        }

        const content = document.getElementById('comment-content').value.trim();
        if (!content) {
            alert('Por favor escribe un comentario');
            return;
        }

        try {
            await this.submitComment(content);
            document.getElementById('comment-content').value = '';
            await this.loadComments(); // Recargar comentarios
        } catch (error) {
            console.error('Error submitting comment:', error);
            this.showError('Error al publicar el comentario');
        }
    }

    async submitComment(content) {
        // Simulación - reemplazar con llamada real a la API
        console.log(`Enviando comentario: ${content}`);
        return new Promise(resolve => setTimeout(resolve, 500));
    }

    async deleteComment(commentId) {
        if (!confirm('¿Estás seguro de que quieres eliminar este comentario?')) {
            return;
        }

        try {
            await this.performDeleteComment(commentId);
            await this.loadComments(); // Recargar comentarios
        } catch (error) {
            console.error('Error deleting comment:', error);
            this.showError('Error al eliminar el comentario');
        }
    }

    async performDeleteComment(commentId) {
        // Simulación - reemplazar con llamada real a la API
        console.log(`Eliminando comentario ${commentId}`);
        return new Promise(resolve => setTimeout(resolve, 500));
    }

    async leavePartnership(userId) {
        if (!confirm('¿Estás seguro de que quieres abandonar esta startup?')) {
            return;
        }

        try {
            await this.performLeavePartnership(userId);
            await this.loadPartners(); // Recargar socios
        } catch (error) {
            console.error('Error leaving partnership:', error);
            this.showError('Error al abandonar la startup');
        }
    }

    async performLeavePartnership(userId) {
        // Simulación - reemplazar con llamada real a la API
        console.log(`Usuario ${userId} abandonando startup ${this.startupId}`);
        return new Promise(resolve => setTimeout(resolve, 500));
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
const startupInfoPage = new StartupInfoPage();
window.startupInfoPage = startupInfoPage;