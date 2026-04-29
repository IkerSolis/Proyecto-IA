// auth.js
// Lógica para Login y Onboarding

document.addEventListener('DOMContentLoaded', () => {
    
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = document.getElementById('loginBtn');
            const spinner = btn.querySelector('.spinner-border');
            
            // "Fail-fast" validations
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            if (!email || !password) {
                showToast('Por favor completa todos los campos', 'warning');
                return;
            }

            // Button state
            btn.classList.add('disabled');
            spinner.classList.remove('d-none');

            try {
                // Se usa fetch normal para login, ya que no requiere token previo (no usamos apiFetch wrapper aqui para evitar re-redirecciones infinitas)
                const response = await fetch('/api/iam/login/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.detail || data.error || 'Credenciales inválidas');
                }

                // Guardar tokens
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
                
                showToast('Inicio de sesión exitoso', 'success');
                setTimeout(() => window.location.href = '/', 500);

            } catch (error) {
                showToast(error.message, 'danger');
                btn.classList.remove('disabled');
                spinner.classList.add('d-none');
            }
        });
    }

    const onboardingForm = document.getElementById('onboardingForm');
    if (onboardingForm) {
        onboardingForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = document.getElementById('onboardingBtn');
            const spinner = btn.querySelector('.spinner-border');
            
            const nombre = document.getElementById('nombre_empresa').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            if (!nombre || !email || !password) {
                showToast('Por favor completa todos los campos', 'warning');
                return;
            }

            btn.classList.add('disabled');
            spinner.classList.remove('d-none');

            try {
                const response = await fetch('/api/iam/onboarding/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nombre: nombre, email: email, password: password })
                });

                const data = await response.json();

                if (!response.ok) {
                    // Extract model errors
                    let errorMsg = 'Error al registrar';
                    if (data.email) errorMsg = data.email[0];
                    throw new Error(errorMsg);
                }

                showToast('Empresa registrada exitosamente. Inicia sesión.', 'success');
                setTimeout(() => window.location.href = '/login/', 1500);

            } catch (error) {
                showToast(error.message, 'danger');
                btn.classList.remove('disabled');
                spinner.classList.add('d-none');
            }
        });
    }
});
