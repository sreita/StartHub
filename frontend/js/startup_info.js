// js/startup_info.js
const DATA_API = 'http://localhost:8000';

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
    const res = await fetch(`${DATA_API}/startups/${startupId}`);
    if (!res.ok) throw new Error('Startup no encontrada');
    const s = await res.json();
    return {
        startup_id: s.startup_id,
        name: s.name,
        description: s.description || '',
        email: '',
        website: '',
        social_media: '',
        created_date: s.created_date || new Date().toISOString(),
        owner_user_id: s.owner_user_id,
        category_id: s.category_id,
        category_name: s.category_name || (s.category_id ? `Categoría ${s.category_id}` : 'General'),
        owner_name: s.owner_name || (s.owner_user_id ? `Usuario ${s.owner_user_id}` : 'Usuario')  // NUEVO
    };
}

    renderStartupInfo(startup) {
    const container = document.getElementById('startup-info');
    container.innerHTML = `
        <div class="flex justify-between items-start mb-6">
            <h1 class="text-4xl md:text-5xl font-bold">${startup.name}</h1>
            <span class="category-badge text-black px-3 py-1 border-2 border-black font-bold">${startup.category_name}</span>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div class="lg:col-span-2">
                <h2 class="text-2xl font-bold mb-4">Descripción</h2>
                <p class="text-gray-700 text-lg leading-relaxed">${startup.description}</p>
            </div>

            <div class="contact-info p-6 border-2 border-black">
                <h3 class="text-xl font-bold mb-4">Información de Contacto</h3>
                <div class="space-y-3">
                    ${startup.email ? `<p><strong>Email:</strong> <a href="mailto:${startup.email}" class="text-blue-600 hover:underline">${startup.email}</a></p>` : ''}
                    ${startup.website ? `<p><strong>Website:</strong> <a href="${startup.website}" target="_blank" class="text-blue-600 hover:underline">${startup.website}</a></p>` : ''}
                    ${startup.social_media ? `<p><strong>Redes Sociales:</strong> ${startup.social_media}</p>` : ''}
                    <p><strong>Fundador:</strong> ${startup.owner_name}</p>  <!-- CAMBIADO -->
                    <p><strong>Fecha de creación:</strong> ${new Date(startup.created_date).toLocaleDateString('es-ES')}</p>
                </div>
            </div>
        </div>
    `;

    this.forceNightModeStyles();
}

// Agregar este nuevo método a la clase StartupInfoPage
forceNightModeStyles() {
    if (document.body.classList.contains('night-mode-active')) {
        console.log('Aplicando estilos forzados de modo noche...');

        // Forzar estilos en el badge de categoría
        const categoryBadge = document.querySelector('.category-badge');
        if (categoryBadge) {
            categoryBadge.style.backgroundColor = '#2d3748'; // gray-darker
            categoryBadge.style.color = '#FFD166'; // yellow-accent
            categoryBadge.style.borderColor = '#0f3460'; // night-border
            categoryBadge.style.boxShadow = '4px 4px 0 #0f3460';
            categoryBadge.classList.remove('bg-yellow-400', 'text-black');
            categoryBadge.classList.add('night-mode-category');
        }

        // Forzar estilos en el cuadro de contacto
        const contactInfo = document.querySelector('.contact-info');
        if (contactInfo) {
            contactInfo.style.backgroundColor = '#16213e'; // night-card
            contactInfo.style.color = '#e2e8f0'; // night-text
            contactInfo.style.borderColor = '#0f3460'; // night-border
            contactInfo.style.boxShadow = '6px 6px 0 #0f3460';
            contactInfo.classList.remove('bg-gray-50');
            contactInfo.classList.add('night-mode-contact');

            // Forzar estilos en los textos dentro del contacto
            const strongElements = contactInfo.querySelectorAll('strong');
            strongElements.forEach(strong => {
                strong.style.color = '#e2e8f0';
            });

            const links = contactInfo.querySelectorAll('a');
            links.forEach(link => {
                link.style.color = '#FFD166'; // yellow-accent
                link.classList.remove('text-blue-600');
            });

            const spans = contactInfo.querySelectorAll('span');
            spans.forEach(span => {
                span.style.color = '#cbd5e0'; // night-text-secondary
            });
        }

        // Forzar estilos en la descripción
        const description = document.querySelector('.text-gray-700');
        if (description) {
            description.style.color = '#cbd5e0'; // night-text-secondary
        }
    }
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
        const res = await fetch(`${DATA_API}/votes/count/${startupId}`);
        if (!res.ok) return { upvotes: 0, downvotes: 0, total: 0 };
        const data = await res.json();
        return {
            upvotes: data.upvotes || 0,
            downvotes: data.downvotes || 0,
            total: (data.upvotes || 0) - (data.downvotes || 0)
        };
    }

    async fetchUserVote(startupId) {
        // No hay endpoint específico para el voto del usuario actualmente
        return null;
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
        const res = await fetch(`${DATA_API}/comments/?startup_id=${startupId}&skip=0&limit=50`);
        if (!res.ok) return [];
        const items = await res.json();
        return items.map(c => ({
            comment_id: c.comment_id,
            content: c.content,
            created_date: c.created_date,
            user_name: `Usuario ${c.user_id}`,
            user_id: c.user_id,
        }));
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
        const user = this.currentUser;
        await fetch(`${DATA_API}/votes/?user_id=${user.id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ startup_id: Number(this.startupId), vote_type: voteType })
        });
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
        await fetch(`${DATA_API}/comments/?user_id=${this.currentUser.id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content, startup_id: Number(this.startupId) })
        });
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
        await fetch(`${DATA_API}/comments/${commentId}?user_id=${this.currentUser.id}`, { method: 'DELETE' });
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