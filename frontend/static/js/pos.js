// pos.js

let catalogData = [];
let cart = []; // Array de { producto, cantidad }

document.addEventListener('DOMContentLoaded', () => {
    loadCatalog();

    const searchBox = document.getElementById('posSearchBox');
    searchBox.addEventListener('input', handleSearch);
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.key === 'F3') {
            e.preventDefault();
            searchBox.focus();
        } else if (e.key === 'F12') {
            e.preventDefault();
            processCheckout();
        }
    });
});

async function loadCatalog() {
    try {
        const data = await apiFetch('/catalog/productos/');
        if (data) {
            catalogData = data.filter(p => p.is_active && p.stock_actual > 0);
            renderQuickCatalog();
        }
    } catch (error) {
        console.error('Error cargando catálogo POS', error);
    }
}

function renderQuickCatalog() {
    const container = document.getElementById('quickCatalog');
    container.innerHTML = '';

    catalogData.forEach(prod => {
        const col = document.createElement('div');
        col.className = 'col';
        col.innerHTML = `
            <div class="card h-100 cursor-pointer shadow-sm border-0" style="cursor: pointer; background-color: var(--bg-color);" onclick="addToCart('${prod.id}')">
                <div class="card-body p-3 text-center">
                    <h6 class="fw-bold mb-1 text-truncate" title="${prod.nombre}">${prod.nombre}</h6>
                    <p class="text-success fw-bold mb-1">$${parseFloat(prod.precio).toFixed(2)}</p>
                    <small class="text-muted d-block">${prod.stock_actual} en stock</small>
                </div>
            </div>
        `;
        container.appendChild(col);
    });
}

function handleSearch(e) {
    const term = e.target.value.toLowerCase();
    const resultsContainer = document.getElementById('searchResults');
    
    if (term.length < 2) {
        resultsContainer.classList.add('d-none');
        return;
    }

    const filtered = catalogData.filter(p => 
        p.nombre.toLowerCase().includes(term) || (p.descripcion && p.descripcion.toLowerCase().includes(term))
    );

    resultsContainer.innerHTML = '';
    
    if (filtered.length === 0) {
        resultsContainer.innerHTML = `<button type="button" class="list-group-item list-group-item-action disabled">Sin resultados</button>`;
    } else {
        filtered.forEach(prod => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'list-group-item list-group-item-action d-flex justify-content-between align-items-center';
            btn.innerHTML = `
                <div><strong>${prod.nombre}</strong></div>
                <div class="text-success fw-bold">$${parseFloat(prod.precio).toFixed(2)}</div>
            `;
            btn.onclick = () => {
                addToCart(prod.id);
                document.getElementById('posSearchBox').value = '';
                resultsContainer.classList.add('d-none');
                document.getElementById('posSearchBox').focus();
            };
            resultsContainer.appendChild(btn);
        });
    }
    
    resultsContainer.classList.remove('d-none');
}

// Ocultar busqueda al hacer clic fuera
document.addEventListener('click', (e) => {
    if (e.target.id !== 'posSearchBox') {
        document.getElementById('searchResults')?.classList.add('d-none');
    }
});

function addToCart(productId) {
    const prod = catalogData.find(p => p.id === productId);
    if (!prod) return;

    const existingItem = cart.find(item => item.producto.id === productId);
    
    if (existingItem) {
        if (existingItem.cantidad < prod.stock_actual) {
            existingItem.cantidad += 1;
        } else {
            showToast(`Stock insuficiente de ${prod.nombre}`, 'warning');
            return;
        }
    } else {
        cart.push({ producto: prod, cantidad: 1 });
    }

    renderCart();
}

function updateQuantity(productId, qty) {
    const qtyNum = parseFloat(qty);
    const item = cart.find(i => i.producto.id === productId);
    
    if (!item) return;

    if (isNaN(qtyNum) || qtyNum <= 0) {
        removeFromCart(productId);
        return;
    }

    if (qtyNum > item.producto.stock_actual) {
        showToast(`Solo hay ${item.producto.stock_actual} en stock`, 'warning');
        item.cantidad = item.producto.stock_actual; // Set to max available
    } else {
        item.cantidad = qtyNum;
    }
    
    renderCart();
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.producto.id !== productId);
    renderCart();
}

function clearCart() {
    cart = [];
    renderCart();
}

function renderCart() {
    const tbody = document.getElementById('cartBody');
    tbody.innerHTML = '';

    if (cart.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center py-4 text-muted">Carrito vacío</td></tr>';
        document.getElementById('cartSubtotal').textContent = '$0.00';
        document.getElementById('cartTotal').textContent = '$0.00';
        return;
    }

    let total = 0;

    cart.forEach(item => {
        const subtotal = item.cantidad * item.producto.precio;
        total += subtotal;

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>
                <div class="fw-bold">${item.producto.nombre}</div>
                <small class="text-muted">$${parseFloat(item.producto.precio).toFixed(2)} c/u</small>
            </td>
            <td>
                <input type="number" class="form-control form-control-sm text-center" value="${item.cantidad}" 
                       onchange="updateQuantity('${item.producto.id}', this.value)" min="0" max="${item.producto.stock_actual}" step="0.01">
            </td>
            <td class="text-end fw-bold">$${subtotal.toFixed(2)}</td>
            <td class="text-end">
                <button class="btn btn-sm btn-outline-danger border-0" onclick="removeFromCart('${item.producto.id}')">
                    <i class="bi bi-trash"></i>X
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    document.getElementById('cartSubtotal').textContent = `$${total.toFixed(2)}`;
    document.getElementById('cartTotal').textContent = `$${total.toFixed(2)}`;
}

async function processCheckout() {
    if (cart.length === 0) {
        showToast('El carrito está vacío', 'warning');
        return;
    }

    const btn = document.getElementById('checkoutBtn');
    const spinner = btn.querySelector('.spinner-border');
    btn.classList.add('disabled');
    spinner.classList.remove('d-none');

    // Construir payload SOLO con IDs y cantidades (Prohibición de cálculos de confianza)
    const items = cart.map(item => ({
        producto_id: item.producto.id,
        cantidad: item.cantidad
    }));

    const payload = {
        cliente_nombre: "Cliente General", // Podría ser dinámico si agregamos un input
        metodo_pago: "EFECTIVO", // Podría ser dinámico
        items: items
    };

    try {
        await apiFetch('/sales/ventas/', {
            method: 'POST',
            body: JSON.stringify(payload)
        });

        showToast('Venta registrada exitosamente', 'success');
        clearCart();
        await loadCatalog(); // Refrescar stock visual

    } catch (error) {
        // El error ya es mostrado por el Toast de apiFetch
    } finally {
        btn.classList.remove('disabled');
        spinner.classList.add('d-none');
    }
}
