// js/startup_info.js
const DATA_API = 'http://localhost:8000';

export class StartupInfoPage {
    constructor() {
        this.startupId = this.getStartupIdFromURL();
        this.currentUser = null;
        this.userVote = null;
        this.comments = [];
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
        const userData = localStorage.getItem('user');

        if (token && userData) {
            try {
                this.currentUser = JSON.parse(userData);
                // Asegurar que tenemos user_id (compatibilidad con diferentes formatos)
                if (this.currentUser && !this.currentUser.user_id && this.currentUser.id) {
                    this.currentUser.user_id = this.currentUser.id;
                }
                this.updateUIForAuthenticatedUser();
            } catch (error) {
                console.error('Error parsing user data:', error);
                this.currentUser = null;
            }
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
            owner_name: s.owner_name || (s.owner_user_id ? `Usuario ${s.owner_user_id}` : 'Usuario')
        };
    }

    renderStartupInfo(startup) {
        const container = document.getElementById('startup-info');
        container.innerHTML = `
            <div class="flex justify-between items-start mb-6">
                <h1 class="text-4xl md:text-5xl font-bold">${this.escapeHtml(startup.name)}</h1>
                <span class="category-badge text-black px-3 py-1 border-2 border-black font-bold">${this.escapeHtml(startup.category_name)}</span>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div class="lg:col-span-2">
                    <h2 class="text-2xl font-bold mb-4">Descripción</h2>
                    <p class="text-gray-700 text-lg leading-relaxed">${this.escapeHtml(startup.description)}</p>
                </div>

                <div class="contact-info p-6 border-2 border-black">
                    <h3 class="text-xl font-bold mb-4">Información de Contacto</h3>
                    <div class="space-y-3">
                        ${startup.email ? `<p><strong>Email:</strong> <a href="mailto:${startup.email}" class="text-blue-600 hover:underline">${startup.email}</a></p>` : ''}
                        ${startup.website ? `<p><strong>Website:</strong> <a href="${startup.website}" target="_blank" class="text-blue-600 hover:underline">${startup.website}</a></p>` : ''}
                        ${startup.social_media ? `<p><strong>Redes Sociales:</strong> ${this.escapeHtml(startup.social_media)}</p>` : ''}
                        <p><strong>Fundador:</strong> ${this.escapeHtml(startup.owner_name)}</p>
                        <p><strong>Fecha de creación:</strong> ${new Date(startup.created_date).toLocaleDateString('es-ES')}</p>
                    </div>
                </div>
            </div>
        `;

        this.forceNightModeStyles();
    }

    forceNightModeStyles() {
        if (document.body.classList.contains('night-mode-active')) {
            console.log('Aplicando estilos forzados de modo noche...');

            const categoryBadge = document.querySelector('.category-badge');
            if (categoryBadge) {
                categoryBadge.style.backgroundColor = '#2d3748';
                categoryBadge.style.color = '#FFD166';
                categoryBadge.style.borderColor = '#0f3460';
                categoryBadge.style.boxShadow = '4px 4px 0 #0f3460';
                categoryBadge.classList.remove('bg-yellow-400', 'text-black');
            }

            const contactInfo = document.querySelector('.contact-info');
            if (contactInfo) {
                contactInfo.style.backgroundColor = '#16213e';
                contactInfo.style.color = '#e2e8f0';
                contactInfo.style.borderColor = '#0f3460';
                contactInfo.style.boxShadow = '6px 6px 0 #0f3460';
                contactInfo.classList.remove('bg-gray-50');

                const strongElements = contactInfo.querySelectorAll('strong');
                strongElements.forEach(strong => {
                    strong.style.color = '#e2e8f0';
                });

                const links = contactInfo.querySelectorAll('a');
                links.forEach(link => {
                    link.style.color = '#FFD166';
                    link.classList.remove('text-blue-600');
                });
            }

            const description = document.querySelector('.text-gray-700');
            if (description) {
                description.style.color = '#cbd5e0';
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
        if (!this.currentUser) return null;

        try {
            const res = await fetch(`${DATA_API}/votes/user/${startupId}?user_id=${this.currentUser.user_id}`);
            if (res.ok) {
                const data = await res.json();
                return data.vote_type;
            }
        } catch (error) {
            console.error('Error fetching user vote:', error);
        }
        return null;
    }

    updateVoteDisplay(votes, userVote) {
        const voteCount = document.getElementById('vote-count');
        const voteStatus = document.getElementById('vote-status');
        const upvoteBtn = document.getElementById('upvote-btn');
        const downvoteBtn = document.getElementById('downvote-btn');

        if (voteCount) voteCount.textContent = votes.total;

        // Resetear estilos
        upvoteBtn.classList.remove('active', 'bg-green-500', 'text-white');
        downvoteBtn.classList.remove('active', 'bg-red-500', 'text-white');

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
            upvoteBtn.disabled = false;
            downvoteBtn.disabled = false;
        }
    }

    async loadComments() {
        try {
            const comments = await this.fetchComments(this.startupId);
            this.comments = comments;
            this.renderComments(comments);
        } catch (error) {
            console.error('Error loading comments:', error);
            this.comments = [];
            this.renderComments([]);
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
            user_name: c.user_name,
            user_id: c.user_id,
        }));
    }

    renderComments(comments) {
        const container = document.getElementById('comments-list');
        const countElement = document.getElementById('comment-count');

        if (countElement) countElement.textContent = comments.length;

        if (!container) return;

        if (comments.length === 0) {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">No hay comentarios todavía. ¡Sé el primero en comentar!</p>';
            return;
        }

        container.innerHTML = comments.map(comment => this.createCommentHTML(comment)).join('');
        this.setupCommentActions();
    }

    createCommentHTML(comment) {
        const isOwner = this.currentUser && this.currentUser.user_id === comment.user_id;
        const formattedDate = new Date(comment.created_date).toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });

        return `
            <div class="comment-item neo-brutalist p-4 mb-4" data-comment-id="${comment.comment_id}">
                <div class="flex flex-col sm:flex-row justify-between items-start gap-2 mb-3">
                    <div class="flex items-center gap-3">
                        <strong class="text-base md:text-lg">${this.escapeHtml(comment.user_name)}</strong>
                        ${isOwner ? '<span class="category-badge text-xs px-2 py-1 rounded">Tú</span>' : ''}
                    </div>
                    <span class="text-xs md:text-sm text-gray-600">${formattedDate}</span>
                </div>
                <div class="comment-content">
                    <p class="text-sm md:text-base mb-3">${this.escapeHtml(comment.content)}</p>
                </div>
                ${isOwner ? `
                <div class="comment-actions flex gap-2 pt-2 border-t border-gray-200">
                    <button class="edit-comment-btn text-xs px-1 py-1 rounded font-bold hover:edit-comment-btn transition-colors">
                        Editar
                    </button>
                    <button class="delete-comment-btn text-xs bg-red-600 text-white px-3 py-1 rounded font-bold hover:delete-comment-btn transition-colors">
                        Eliminar
                    </button>
                </div>
                ` : ''}
            </div>
        `;
    }

    setupCommentActions() {
        // Configurar botones de editar
        document.querySelectorAll('.edit-comment-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const commentItem = e.target.closest('.comment-item');
                const commentId = parseInt(commentItem.dataset.commentId);
                this.editComment(commentId);
            });
        });

        // Configurar botones de eliminar
        document.querySelectorAll('.delete-comment-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const commentItem = e.target.closest('.comment-item');
                const commentId = parseInt(commentItem.dataset.commentId);
                this.deleteComment(commentId);
            });
        });
    }

    editComment(commentId) {
        const comment = this.comments.find(c => c.comment_id === commentId);
        if (!comment) return;

        const commentItem = document.querySelector(`[data-comment-id="${commentId}"]`);
        const contentElement = commentItem.querySelector('.comment-content p');
        const currentContent = contentElement.textContent;

        // Reemplazar con formulario de edición
        commentItem.querySelector('.comment-content').innerHTML = `
            <textarea class="edit-comment-textarea w-full p-3 mb-3 border-2 border-black focus:outline-none focus:shadow-[2px_2px_0_#000] text-sm md:text-base" rows="3">${this.escapeHtml(currentContent)}</textarea>
            <div class="flex gap-2">
                <button class="save-edit-btn text-xs px-3 py-1 rounded font-bold hover:save-edit-btn transition-colors">
                    Guardar
                </button>
                <button class="cancel-edit-btn text-xs px-3 py-1 rounded font-bold hover:cancel-edit-btn transition-colors">
                    Cancelar
                </button>
            </div>
        `;

        // Ocultar botones de acción temporalmente
        const actionsElement = commentItem.querySelector('.comment-actions');
        if (actionsElement) {
            actionsElement.style.display = 'none';
        }

        // Configurar eventos de los botones de edición
        commentItem.querySelector('.save-edit-btn').addEventListener('click', () => {
            this.saveCommentEdit(commentId);
        });

        commentItem.querySelector('.cancel-edit-btn').addEventListener('click', () => {
            this.cancelCommentEdit(commentId, currentContent);
        });
    }

    async saveCommentEdit(commentId) {
        const commentItem = document.querySelector(`[data-comment-id="${commentId}"]`);
        const textarea = commentItem.querySelector('.edit-comment-textarea');
        const newContent = textarea.value.trim();

        if (!newContent) {
            alert('El comentario no puede estar vacío');
            return;
        }

        if (!this.currentUser) {
            alert('Debes iniciar sesión para editar comentarios');
            return;
        }

        try {
            const response = await fetch(`${DATA_API}/comments/${commentId}?user_id=${this.currentUser.user_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content: newContent
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al actualizar el comentario');
            }

            await this.loadComments(); // Recargar comentarios
        } catch (error) {
            console.error('Error updating comment:', error);
            alert('Error al actualizar el comentario: ' + error.message);
        }
    }

    cancelCommentEdit(commentId, originalContent) {
        const commentItem = document.querySelector(`[data-comment-id="${commentId}"]`);
        commentItem.querySelector('.comment-content').innerHTML = `
            <p class="text-sm md:text-base mb-3">${this.escapeHtml(originalContent)}</p>
        `;

        // Mostrar botones de acción nuevamente
        const actionsElement = commentItem.querySelector('.comment-actions');
        if (actionsElement) {
            actionsElement.style.display = 'flex';
        }
    }

    async deleteComment(commentId) {
        if (!confirm('¿Estás seguro de que quieres eliminar este comentario?')) {
            return;
        }

        if (!this.currentUser) {
            alert('Debes iniciar sesión para eliminar comentarios');
            return;
        }

        try {
            const response = await fetch(`${DATA_API}/comments/${commentId}?user_id=${this.currentUser.user_id}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al eliminar el comentario');
            }

            await this.loadComments(); // Recargar comentarios
        } catch (error) {
            console.error('Error deleting comment:', error);
            alert('Error al eliminar el comentario: ' + error.message);
        }
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

        if (countElement) countElement.textContent = partners.length;

        if (!container) return;

        container.innerHTML = partners.map(partner => `
            <div class="flex justify-between items-center border-b-2 border-black pb-4 mb-4 last:border-b-0 last:mb-0">
                <div>
                    <strong class="text-lg">${this.escapeHtml(partner.user_name)}</strong>
                    <p class="text-gray-600">${this.escapeHtml(partner.role)}</p>
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
        const upvoteBtn = document.getElementById('upvote-btn');
        const downvoteBtn = document.getElementById('downvote-btn');

        if (upvoteBtn) {
            upvoteBtn.addEventListener('click', () => this.handleVote('upvote'));
        }
        if (downvoteBtn) {
            downvoteBtn.addEventListener('click', () => this.handleVote('downvote'));
        }

        // Comentarios
        const commentForm = document.getElementById('comment-form');
        if (commentForm) {
            commentForm.addEventListener('submit', (e) => this.handleCommentSubmit(e));
        }
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
        const response = await fetch(`${DATA_API}/votes/?user_id=${user.user_id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                startup_id: parseInt(this.startupId),
                vote_type: voteType
            })
        });

        if (!response.ok) {
            throw new Error('Error al enviar el voto');
        }
    }

    async handleCommentSubmit(e) {
        e.preventDefault();

        if (!this.currentUser) {
            alert('Por favor inicia sesión para comentar');
            window.location.href = './login.html';
            return;
        }

        const contentInput = document.getElementById('comment-content');
        const content = contentInput.value.trim();

        if (!content) {
            alert('Por favor escribe un comentario');
            return;
        }

        try {
            await this.submitComment(content);
            contentInput.value = '';
            await this.loadComments(); // Recargar comentarios
        } catch (error) {
            console.error('Error submitting comment:', error);
            this.showError('Error al publicar el comentario');
        }
    }

    async submitComment(content) {
        const response = await fetch(`${DATA_API}/comments/?user_id=${this.currentUser.user_id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                content: content,
                startup_id: parseInt(this.startupId)
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al crear el comentario');
        }
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
        // Implementar notificación de error más elegante
        alert(message);
    }

    setupNightMode() {
        const nightModeToggle = document.getElementById('night-mode-toggle');
        if (nightModeToggle) {
            nightModeToggle.addEventListener('click', (e) => {
                e.preventDefault();
                document.body.classList.toggle('night-mode-active');
                localStorage.setItem('nightMode', document.body.classList.contains('night-mode-active'));
                this.forceNightModeStyles();
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

    escapeHtml(unsafe) {
        if (!unsafe) return '';
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
}

// Inicializar la página
document.addEventListener('DOMContentLoaded', () => {
    window.startupInfoPage = new StartupInfoPage();
});