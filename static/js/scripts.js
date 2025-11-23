// Script principal da plataforma DuploTech 6040

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    console.log('🚀 DuploTech 6040 - Plataforma inicializada');
    
    // Inicializar componentes
    setupFlashMessages();
    setupRealTimeUpdates();
    setupButtonInteractions();
    setupFormValidations();
}

// Gerenciar mensagens flash
function setupFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        // Fechar automaticamente após 5 segundos
        setTimeout(() => {
            closeFlashMessage(message);
        }, 5000);
        
        // Botão de fechar
        const closeBtn = message.querySelector('.flash-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => closeFlashMessage(message));
        }
    });
}

function closeFlashMessage(message) {
    message.style.transition = 'all 0.3s ease-out';
    message.style.transform = 'translateX(100%)';
    message.style.opacity = '0';
    
    setTimeout(() => {
        if (message.parentElement) {
            message.remove();
        }
    }, 300);
}

// Atualizações em tempo real
function setupRealTimeUpdates() {
    // Atualizar hora atual
    setInterval(updateCurrentTime, 1000);
    
    // Simular atualizações de status (apenas demonstração)
    if (document.querySelector('.status-grid')) {
        setInterval(simulateStatusUpdates, 10000);
    }
}

function updateCurrentTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('pt-BR');
    
    // Atualizar elementos de tempo
    document.querySelectorAll('#update-time, .current-time').forEach(element => {
        element.textContent = timeString;
    });
}

function simulateStatusUpdates() {
    // Simular pequenas variações nos dados (apenas para demonstração)
    const statusCards = document.querySelectorAll('.status-card');
    
    statusCards.forEach(card => {
        if (Math.random() > 0.7) { // 30% de chance de atualização
            const valueElement = card.querySelector('.status-value');
            if (valueElement) {
                const currentValue = parseFloat(valueElement.textContent);
                if (!isNaN(currentValue)) {
                    const variation = (Math.random() - 0.5) * 2; // ±1
                    const newValue = Math.max(0, currentValue + variation);
                    valueElement.textContent = newValue.toFixed(1);
                }
            }
        }
    });
}

// Interações dos botões
function setupButtonInteractions() {
    // Botões sem ação específica
    document.querySelectorAll('.btn:not([href]):not([type="submit"])').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            showFeatureMessage(this);
        });
    });
    
    // Efeitos hover nos cards
    document.querySelectorAll('.feature-card, .status-card, .analise-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

function showFeatureMessage(button) {
    const messages = [
        'Funcionalidade em desenvolvimento!',
        'Recurso disponível em breve!',
        'Estamos trabalhando nisso!'
    ];
    
    const randomMessage = messages[Math.floor(Math.random() * messages.length)];
    showToast(randomMessage, 'info');
}

// Validações de formulário
function setupFormValidations() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#ef4444';
                } else {
                    field.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showToast('Por favor, preencha todos os campos obrigatórios.', 'error');
            }
        });
    });
}

// Utilitários
function showToast(message, type = 'info') {
    // Criar elemento de toast
    const toast = document.createElement('div');
    toast.className = `flash-message ${type}`;
    toast.innerHTML = `
        <i class="fas fa-${getToastIcon(type)}"></i>
        ${message}
        <button class="flash-close"><i class="fas fa-times"></i></button>
    `;
    
    const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
    flashContainer.appendChild(toast);
    
    // Configurar fechamento
    setupFlashMessages();
}

function getToastIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.appendChild(container);
    return container;
}

// API Helpers
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`Erro na requisição: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Erro na chamada da API:', error);
        showToast('Erro ao conectar com o servidor', 'error');
        throw error;
    }
}

// Exportar funções para uso global
window.DuploTechApp = {
    initializeApp,
    showToast,
    apiCall,
    updateCurrentTime
};