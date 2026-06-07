// Global variables
let efommTopics = [];

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Toasts
    window.showToast = function(message, type = 'success') {
        const container = document.getElementById('toast-container');
        if (!container) return;
        
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        let icon = '<i class="fa-solid fa-circle-check"></i>';
        if (type === 'error') {
            icon = '<i class="fa-solid fa-triangle-exclamation"></i>';
        } else if (type === 'info') {
            icon = '<i class="fa-solid fa-circle-info"></i>';
        }
        
        toast.innerHTML = `${icon}<span>${message}</span>`;
        container.appendChild(toast);
        
        // Remove toast after 3.5 seconds
        setTimeout(() => {
            toast.style.animation = 'slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1) reverse';
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    };

    // 2. Countdown Timer (if dashboard elements exist)
    initCountdown();

    // 3. Profile / Config Modal Handlers
    initProfileConfig();

    // 4. Video Add Modal & Youtube Thumbnail Handler
    initVideosPage();

    // 5. EFOMM Tracker Handler
    initEfommPage();
});

// ==========================================
// 2. Countdown Timer
// ==========================================
function initCountdown() {
    const statDays = document.getElementById('stat-days-left');
    if (!statDays) return;

    // examDateStr is passed via HTML script tag
    if (typeof examDateStr === 'undefined' || !examDateStr) return;

    function updateCountdown() {
        const examDate = new Date(examDateStr + 'T00:00:00');
        const now = new Date();
        
        // Reset hours for accurate day difference
        examDate.setHours(0,0,0,0);
        now.setHours(0,0,0,0);

        const diffTime = examDate - now;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (isNaN(diffDays)) {
            statDays.innerText = '--';
        } else if (diffDays < 0) {
            statDays.innerText = 'Realizada';
            statDays.nextElementSibling.innerText = 'Prova já ocorrida';
        } else if (diffDays === 0) {
            statDays.innerText = 'Hoje!';
            statDays.nextElementSibling.innerText = 'Dia do Concurso';
            statDays.parentElement.parentElement.style.borderColor = 'var(--color-danger)';
        } else {
            statDays.innerText = diffDays;
        }
    }

    updateCountdown();
}

// ==========================================
// 3. Profile Configurations
// ==========================================
function initProfileConfig() {
    const configModal = document.getElementById('config-modal');
    const openBtn = document.getElementById('open-config-btn');
    const closeBtn = document.getElementById('close-config-modal');
    const cancelBtn = document.getElementById('cancel-config-btn');
    const form = document.getElementById('config-form');

    if (!configModal || !openBtn) return;

    const openModal = () => configModal.classList.add('show');
    const closeModal = () => configModal.classList.remove('show');

    openBtn.addEventListener('click', openModal);
    closeBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);

    // Close modal on background click
    configModal.addEventListener('click', (e) => {
        if (e.target === configModal) closeModal();
    });

    // Handle form submit
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const userName = document.getElementById('config-user-name').value.trim();
        const examDate = document.getElementById('config-exam-date').value;

        if (!userName || !examDate) {
            showToast('Preencha todos os campos!', 'error');
            return;
        }

        try {
            const response = await fetch('/api/settings/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_name: userName, exam_date: examDate })
            });
            const data = await response.json();

            if (data.success) {
                showToast('Configurações salvas com sucesso!');
                
                // Update DOM text dynamically
                const welcomeName = document.getElementById('welcome-name');
                const profileName = document.getElementById('profile-name');
                const avatar = document.getElementById('profile-avatar');
                
                if (welcomeName) welcomeName.innerText = userName;
                if (profileName) profileName.innerText = userName;
                if (avatar) avatar.innerText = userName.charAt(0).toUpperCase();

                // Update countdown global state & reload page or recount
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                showToast(data.message || 'Erro ao salvar.', 'error');
            }
        } catch (err) {
            console.error(err);
            showToast('Erro de conexão com o servidor.', 'error');
        }
        closeModal();
    });
}

// ==========================================
// 4. Videos Page Logic
// ==========================================
function initVideosPage() {
    // 4a. Load Youtube Thumbnails dynamically
    const ytThumbnails = document.querySelectorAll('img[data-yt-url]');
    ytThumbnails.forEach(img => {
        const url = img.getAttribute('data-yt-url');
        const ytId = getYoutubeId(url);
        if (ytId) {
            img.src = `https://img.youtube.com/vi/${ytId}/mqdefault.jpg`;
        }
    });

    // 4b. Modal Toggle
    const videoModal = document.getElementById('video-modal');
    const openBtn = document.getElementById('open-video-modal-btn');
    const closeBtn = document.getElementById('close-video-modal');
    const cancelBtn = document.getElementById('cancel-video-btn');

    if (videoModal && openBtn) {
        const openModal = () => videoModal.classList.add('show');
        const closeModal = () => videoModal.classList.remove('show');

        openBtn.addEventListener('click', openModal);
        closeBtn.addEventListener('click', closeModal);
        cancelBtn.addEventListener('click', closeModal);

        videoModal.addEventListener('click', (e) => {
            if (e.target === videoModal) closeModal();
        });
    }

    // 4c. Video Categories Filter
    const filterContainer = document.getElementById('video-category-filters');
    if (filterContainer) {
        const filters = filterContainer.querySelectorAll('.filter-tag');
        const videoCards = document.querySelectorAll('.video-card');

        filters.forEach(filter => {
            filter.addEventListener('click', () => {
                filters.forEach(f => f.classList.remove('active'));
                filter.classList.add('active');
                
                const category = filter.getAttribute('data-category');
                
                videoCards.forEach(card => {
                    if (category === 'all' || card.getAttribute('data-category') === category) {
                        card.style.display = 'flex';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    }
}

// Extract Youtube ID
function getYoutubeId(url) {
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : null;
}

// Toggle Watched Status via AJAX
async function toggleVideoWatched(videoId, element) {
    try {
        const response = await fetch(`/api/videos/toggle/${videoId}`, {
            method: 'POST'
        });
        const data = await response.json();

        if (data.success) {
            element.classList.toggle('active');
            const label = element.querySelector('.toggle-label');
            
            if (element.classList.contains('active')) {
                label.innerText = 'Assistido';
                showToast('Vídeo marcado como assistido!');
            } else {
                label.innerText = 'Não assistido';
                showToast('Vídeo marcado como não assistido!', 'info');
            }
            
            // If on Dashboard, update video count stats
            const statVideos = document.getElementById('stat-videos-count');
            if (statVideos) {
                // Quick page refresh or fetch update
                setTimeout(() => window.location.reload(), 800);
            }
        } else {
            showToast('Erro ao atualizar status do vídeo.', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast('Erro de conexão.', 'error');
    }
}

// Delete Video via AJAX
async function deleteVideo(videoId) {
    if (!confirm('Deseja realmente excluir este vídeo?')) return;
    
    try {
        const response = await fetch(`/api/videos/delete/${videoId}`, {
            method: 'DELETE'
        });
        const data = await response.json();

        if (data.success) {
            showToast('Vídeo excluído com sucesso!');
            
            // Remove video card from DOM with visual fade
            const card = document.querySelector(`.video-card[data-video-id="${videoId}"]`);
            if (card) {
                card.style.opacity = '0';
                card.style.transform = 'scale(0.9)';
                setTimeout(() => {
                    card.remove();
                    // If no video cards remaining, reload to show empty state
                    const remaining = document.querySelectorAll('.video-card');
                    if (remaining.length === 0) {
                        window.location.reload();
                    }
                }, 300);
            }
        } else {
            showToast('Erro ao excluir vídeo.', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast('Erro de conexão.', 'error');
    }
}

// Submit Add Video Form
async function submitVideoForm(event) {
    event.preventDefault();
    
    const title = document.getElementById('video-title').value.trim();
    const url = document.getElementById('video-url').value.trim();
    const category = document.getElementById('video-category').value;
    const notes = document.getElementById('video-notes').value.trim();

    try {
        const response = await fetch('/api/videos/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, url, category, notes })
        });
        const data = await response.json();

        if (data.success) {
            showToast('Vídeo cadastrado com sucesso!');
            document.getElementById('video-form').reset();
            document.getElementById('close-video-modal').click();
            
            // Reload page to show new video with proper rendering
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showToast(data.message || 'Erro ao cadastrar vídeo.', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast('Erro de conexão.', 'error');
    }
}

// Play Video in Modal Player
function playVideo(url, title) {
    const playerModal = document.getElementById('video-player-modal');
    const container = document.getElementById('player-iframe-container');
    const headerTitle = document.getElementById('video-player-title');
    
    if (!playerModal || !container) return;

    headerTitle.innerText = title;
    
    const ytId = getYoutubeId(url);
    if (ytId) {
        container.innerHTML = `<iframe src="https://www.youtube.com/embed/${ytId}?autoplay=1" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
    } else {
        // Fallback simple link helper inside modal
        container.innerHTML = `
            <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height: 350px; text-align:center; padding: 2rem;">
                <i class="fa-solid fa-arrow-up-right-from-square" style="font-size: 2.5rem; color: var(--color-primary); margin-bottom: 1rem;"></i>
                <p style="margin-bottom: 1.5rem; font-size: 0.95rem;">Este link não é do YouTube. Clique no botão abaixo para assistir externamente:</p>
                <a href="${url}" target="_blank" class="btn btn-primary">Abrir Link Externo <i class="fa-solid fa-arrow-up-right-from-square"></i></a>
            </div>
        `;
    }
    
    playerModal.classList.add('show');
}

function closePlayerModal() {
    const playerModal = document.getElementById('video-player-modal');
    const container = document.getElementById('player-iframe-container');
    
    if (playerModal) {
        playerModal.classList.remove('show');
    }
    if (container) {
        container.innerHTML = ''; // Stop the video playing in background
    }
}

// ==========================================
// 5. EFOMM Page Logic
// ==========================================
function initEfommPage() {
    const tabsContainer = document.getElementById('subject-tabs-container');
    if (!tabsContainer) return; // Not on EFOMM page

    // Fetch EFOMM Topics list
    loadEfommTopics();

    // Setup tab clicks
    const tabs = tabsContainer.querySelectorAll('.subject-tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            const subject = tab.getAttribute('data-subject');
            document.getElementById('current-tab-name').innerText = subject;
            
            renderSubjectTopics(subject);
        });
    });
}

// Fetch all topics once on page load
async function loadEfommTopics() {
    try {
        const response = await fetch('/api/efomm/list');
        const data = await response.json();
        
        if (data.success) {
            efommTopics = data.topics;
            
            // Get active subject and render
            const activeTab = document.querySelector('.subject-tab.active');
            const initialSubject = activeTab ? activeTab.getAttribute('data-subject') : 'Matemática';
            renderSubjectTopics(initialSubject);
        } else {
            document.getElementById('topics-tbody').innerHTML = `
                <tr>
                    <td colspan="3" style="text-align: center; color: var(--color-danger); padding: 2rem;">
                        Erro ao carregar matérias.
                    </td>
                </tr>
            `;
        }
    } catch (err) {
        console.error(err);
        document.getElementById('topics-tbody').innerHTML = `
            <tr>
                <td colspan="3" style="text-align: center; color: var(--color-danger); padding: 2rem;">
                    Erro de conexão com o servidor.
                </td>
            </tr>
        `;
    }
}

// Render topics for specific subject and update progress details
function renderSubjectTopics(subject) {
    const tbody = document.getElementById('topics-tbody');
    if (!tbody) return;

    // Filter topics
    const filtered = efommTopics.filter(t => t.subject === subject);
    
    if (filtered.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="3" style="text-align: center; color: var(--text-secondary); padding: 2rem;">
                    Nenhum tópico encontrado para esta disciplina.
                </td>
            </tr>
        `;
        updateSubjectProgressBar(0, 0);
        return;
    }

    // Calculate progress stats
    const total = filtered.length;
    const completed = filtered.filter(t => t.status === 'completed').length;
    const studying = filtered.filter(t => t.status === 'studying').length;
    
    updateSubjectProgressBar(completed, total);

    // Build rows
    tbody.innerHTML = '';
    filtered.forEach(topic => {
        const tr = document.createElement('tr');
        
        // Topic Title & Videos Button
        const tdTitle = document.createElement('td');
        tdTitle.className = 'topic-title-cell';
        
        const titleText = document.createElement('span');
        titleText.className = 'topic-title';
        titleText.innerText = topic.topic_name;
        tdTitle.appendChild(titleText);
        
        if (topic.videos && topic.videos.length > 0) {
            const videoBtn = document.createElement('div');
            videoBtn.className = 'topic-videos-btn';
            videoBtn.id = `videos-btn-${topic.id}`;
            videoBtn.innerHTML = `<i class="fa-solid fa-circle-play"></i> Videoaulas (${topic.videos.length})`;
            videoBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                toggleTopicVideos(topic.id);
            });
            tdTitle.appendChild(videoBtn);
        }
        
        // Topic Status Dropdown Wrapper
        const tdStatus = document.createElement('td');
        
        const wrapper = document.createElement('div');
        wrapper.className = `status-select-wrapper ${topic.status}`;
        
        const select = document.createElement('select');
        select.className = `status-select ${topic.status}`;
        select.innerHTML = `
            <option value="not_started" ${topic.status === 'not_started' ? 'selected' : ''}>Não Iniciado</option>
            <option value="studying" ${topic.status === 'studying' ? 'selected' : ''}>Estudando</option>
            <option value="completed" ${topic.status === 'completed' ? 'selected' : ''}>Concluído</option>
        `;
        
        select.addEventListener('change', (e) => {
            updateTopicStatus(topic.id, e.target.value, wrapper, select, subject);
        });
        
        wrapper.appendChild(select);
        tdStatus.appendChild(wrapper);
        
        // Topic Notes Input
        const tdNotes = document.createElement('td');
        
        const notesWrapper = document.createElement('div');
        notesWrapper.className = 'notes-input-wrapper';
        
        const input = document.createElement('textarea');
        input.className = 'notes-input';
        input.placeholder = 'Digite notas ou fórmulas...';
        input.value = topic.notes || '';
        
        const saveBtn = document.createElement('button');
        saveBtn.className = 'btn-save-notes';
        saveBtn.innerHTML = '<i class="fa-regular fa-floppy-disk"></i>';
        saveBtn.title = 'Salvar anotação';
        
        const saveAction = () => {
            saveTopicNotes(topic.id, input.value.trim(), saveBtn);
        };
        
        saveBtn.addEventListener('click', saveAction);
        // Save on Ctrl+Enter
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                e.preventDefault();
                saveAction();
            }
        });
        
        notesWrapper.appendChild(input);
        notesWrapper.appendChild(saveBtn);
        tdNotes.appendChild(notesWrapper);
        
        tr.appendChild(tdTitle);
        tr.appendChild(tdStatus);
        tr.appendChild(tdNotes);
        
        tbody.appendChild(tr);
        
        // Se houver vídeos, insere a linha do acordeão logo abaixo do tópico
        if (topic.videos && topic.videos.length > 0) {
            const trVideos = document.createElement('tr');
            trVideos.id = `videos-row-${topic.id}`;
            trVideos.className = 'videos-accordion-row';
            trVideos.style.display = 'none';
            
            const tdVideos = document.createElement('td');
            tdVideos.colSpan = 3;
            tdVideos.style.padding = '0';
            
            const accordionContent = document.createElement('div');
            accordionContent.className = 'videos-accordion-content';
            
            const grid = document.createElement('div');
            grid.className = 'accordion-videos-grid';
            
            topic.videos.forEach(video => {
                const card = document.createElement('div');
                card.className = 'accordion-video-card';
                
                const ytId = getYoutubeId(video.url);
                const thumbUrl = ytId ? `https://img.youtube.com/vi/${ytId}/mqdefault.jpg` : 'https://images.unsplash.com/photo-1516116211223-5c359a36298a?w=500&auto=format&fit=crop&q=60';
                
                card.innerHTML = `
                    <div class="accordion-video-thumb">
                        <img src="${thumbUrl}" alt="Thumbnail">
                        <div class="accordion-video-play-overlay">
                            <i class="fa-solid fa-play"></i>
                        </div>
                    </div>
                    <div class="accordion-video-info">
                        <span class="accordion-video-title" title="${video.title}">${video.title}</span>
                        <span class="accordion-video-channel"><i class="fa-brands fa-youtube" style="color: #ff0000; margin-right: 4px;"></i> YouTube</span>
                    </div>
                `;
                
                card.addEventListener('click', () => {
                    playVideo(video.url, video.title);
                });
                
                grid.appendChild(card);
            });
            
            accordionContent.appendChild(grid);
            tdVideos.appendChild(accordionContent);
            trVideos.appendChild(tdVideos);
            tbody.appendChild(trVideos);
        }
    });
}

// Controla a abertura e fechamento das linhas de acordeão
function toggleTopicVideos(topicId) {
    const row = document.getElementById(`videos-row-${topicId}`);
    if (!row) return;
    
    const isHidden = row.style.display === 'none';
    
    // Fechar todas as outras linhas abertas para manter a interface organizada
    const allRows = document.querySelectorAll('.videos-accordion-row');
    allRows.forEach(r => {
        if (r.id !== `videos-row-${topicId}`) {
            r.style.display = 'none';
            const siblingId = r.id.replace('videos-row-', '');
            const siblingBtn = document.getElementById(`videos-btn-${siblingId}`);
            if (siblingBtn) siblingBtn.classList.remove('active');
        }
    });
    
    // Alternar a linha atual
    const btn = document.getElementById(`videos-btn-${topicId}`);
    if (isHidden) {
        row.style.display = 'table-row';
        if (btn) btn.classList.add('active');
    } else {
        row.style.display = 'none';
        if (btn) btn.classList.remove('active');
    }
}

// Update Subject Progress visual components
function updateSubjectProgressBar(completed, total) {
    const statsText = document.getElementById('subject-progress-stats');
    const fill = document.getElementById('subject-progress-bar-fill');
    
    if (!statsText || !fill) return;
    
    const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
    statsText.innerText = `${completed} de ${total} Concluídos (${pct}%)`;
    fill.style.width = `${pct}%`;
    
    // Choose gradient/color depending on percentage
    if (pct < 30) {
        fill.style.background = 'linear-gradient(90deg, #ef4444, #f59e0b)';
    } else if (pct < 75) {
        fill.style.background = 'linear-gradient(90deg, #f59e0b, var(--color-primary))';
    } else {
        fill.style.background = 'linear-gradient(90deg, var(--color-primary), var(--color-success))';
    }
}

// AJAX: Update topic status
async function updateTopicStatus(topicId, newStatus, wrapper, select, subject) {
    try {
        const response = await fetch(`/api/efomm/update/${topicId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });
        const data = await response.json();

        if (data.success) {
            // Update wrapper class
            wrapper.className = `status-select-wrapper ${newStatus}`;
            select.className = `status-select ${newStatus}`;
            
            // Update local memory list
            const index = efommTopics.findIndex(t => t.id === topicId);
            if (index !== -1) {
                efommTopics[index].status = newStatus;
            }
            
            // Re-render calculations
            const subjectTopics = efommTopics.filter(t => t.subject === subject);
            const total = subjectTopics.length;
            const completed = subjectTopics.filter(t => t.status === 'completed').length;
            updateSubjectProgressBar(completed, total);
            
            showToast('Status do tópico atualizado!');
        } else {
            showToast('Erro ao atualizar status.', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast('Erro de conexão.', 'error');
    }
}

// AJAX: Save notes for EFOMM topic
async function saveTopicNotes(topicId, notesContent, saveBtn) {
    try {
        const response = await fetch(`/api/efomm/update/${topicId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ notes: notesContent })
        });
        const data = await response.json();

        if (data.success) {
            // Update local memory list
            const index = efommTopics.findIndex(t => t.id === topicId);
            if (index !== -1) {
                efommTopics[index].notes = notesContent;
            }
            
            // Show save animation success
            saveBtn.innerHTML = '<i class="fa-solid fa-check"></i>';
            saveBtn.classList.add('saved');
            
            setTimeout(() => {
                saveBtn.innerHTML = '<i class="fa-regular fa-floppy-disk"></i>';
                saveBtn.classList.remove('saved');
            }, 2000);
            
            showToast('Anotações salvas com sucesso!');
        } else {
            showToast('Erro ao salvar anotação.', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast('Erro de conexão.', 'error');
    }
}
