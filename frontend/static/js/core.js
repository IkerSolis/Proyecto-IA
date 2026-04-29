// core.js
// Gestor central de configuración y estado para el frontend

const API_BASE_URL = '/api';

/**
 * Muestra una notificación Toast
 * @param {string} message - Mensaje a mostrar
 * @param {string} type - 'success', 'danger', 'warning', 'info'
 */
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', toastHtml);
    const toastElement = document.getElementById(toastId);
    const bsToast = new bootstrap.Toast(toastElement, { delay: 3000 });
    bsToast.show();

    // Eliminar el nodo del DOM tras ocultarse
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

/**
 * Wrapper sobre fetch para adjuntar JWT automáticamente y estandarizar respuestas
 */
async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('access_token');
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers
        });

        // Manejo de expiración de token o desautorización
        if (response.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login/';
            return null;
        }

        // Si la respuesta no es OK, extraer error
        if (!response.ok) {
            let errorMsg = 'Error en el servidor';
            try {
                const errorData = await response.json();
                errorMsg = errorData.detail || errorData.error || Object.values(errorData).join(', ') || errorMsg;
            } catch (e) {}
            throw new Error(errorMsg);
        }

        // Procesar JSON o retornar null si es No Content (204)
        if (response.status === 204) return null;
        
        return await response.json();
    } catch (error) {
        showToast(error.message, 'danger');
        throw error;
    }
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login/';
}

// Proteger rutas si no hay token, excepto en /login y /onboarding
document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    const isPublicRoute = currentPath === '/login/' || currentPath === '/onboarding/';
    const token = localStorage.getItem('access_token');

    if (!token && !isPublicRoute) {
        window.location.href = '/login/';
    }
    
    // Decodificar JWT para obtener nombre de empresa (payload) y mostrarlo
    if (token && !isPublicRoute) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            if (payload.email) {
                const emailEl = document.getElementById('current_user_email');
                if (emailEl) emailEl.textContent = payload.email;
            }
        } catch (e) {
            console.error('Error decodificando JWT', e);
        }
    }
});
