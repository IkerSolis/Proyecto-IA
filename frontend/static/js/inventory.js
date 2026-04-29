// inventory.js

let productsData = [];

document.addEventListener('DOMContentLoaded', () => {
    loadInventory();

    const form = document.getElementById('productoForm');
    form.addEventListener('submit', handleSaveProduct);
});

async function loadInventory() {
    try {
        const data = await apiFetch('/catalog/productos/');
        if (data) {
            productsData = data;
            renderTable(productsData);
        }
    } catch (error) {
        console.error('Failed to load inventory', error);
    }
}

function renderTable(data) {
    const tbody = document.getElementById('inventoryBody');
    tbody.innerHTML = '';

    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-muted">No hay productos en el catálogo.</td></tr>';
        return;
    }

    data.forEach(prod => {
        if (!prod.is_active) return; // Solo activos

        const tr = document.createElement('tr');
        // Usar .toFixed() para display
        tr.innerHTML = `
            <td class="fw-medium">${prod.nombre}</td>
            <td class="text-muted small">${prod.descripcion || 'Sin descripción'}</td>
            <td class="text-success fw-bold">$${parseFloat(prod.precio).toFixed(2)}</td>
            <td>
                <span class="${prod.stock_actual <= 0 ? 'text-danger fw-bold' : ''}">
                    ${prod.stock_actual}
                </span>
            </td>
            <td class="text-end">
                <button class="btn btn-sm btn-outline-secondary me-1" onclick="prepareEditModal('${prod.id}')">Editar</button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteProduct('${prod.id}')">Desactivar</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function filterTable() {
    const term = document.getElementById('searchBox').value.toLowerCase();
    const filtered = productsData.filter(p => 
        p.nombre.toLowerCase().includes(term) || (p.descripcion && p.descripcion.toLowerCase().includes(term))
    );
    renderTable(filtered);
}

function prepareCreateModal() {
    document.getElementById('productoForm').reset();
    document.getElementById('prod_id').value = '';
    document.getElementById('productoModalLabel').textContent = 'Nuevo Producto';
}

function prepareEditModal(id) {
    const prod = productsData.find(p => p.id === id);
    if (!prod) return;

    document.getElementById('prod_id').value = prod.id;
    document.getElementById('prod_nombre').value = prod.nombre;
    document.getElementById('prod_descripcion').value = prod.descripcion || '';
    document.getElementById('prod_precio').value = prod.precio;
    document.getElementById('prod_stock_actual').value = prod.stock_actual;
    
    document.getElementById('productoModalLabel').textContent = 'Editar Producto';
    
    const modal = new bootstrap.Modal(document.getElementById('productoModal'));
    modal.show();
}

async function handleSaveProduct(e) {
    e.preventDefault();
    const btn = document.getElementById('saveProdBtn');
    const spinner = btn.querySelector('.spinner-border');
    btn.classList.add('disabled');
    spinner.classList.remove('d-none');

    const id = document.getElementById('prod_id').value;
    const payload = {
        nombre: document.getElementById('prod_nombre').value,
        descripcion: document.getElementById('prod_descripcion').value,
        precio: document.getElementById('prod_precio').value,
        stock_actual: parseInt(document.getElementById('prod_stock_actual').value, 10),
    };

    try {
        if (id) {
            // Update
            await apiFetch(`/catalog/productos/${id}/`, {
                method: 'PUT',
                body: JSON.stringify(payload)
            });
            showToast('Producto actualizado exitosamente', 'success');
        } else {
            // Create
            await apiFetch('/catalog/productos/', {
                method: 'POST',
                body: JSON.stringify(payload)
            });
            showToast('Producto creado exitosamente', 'success');
        }
        
        const modalEl = document.getElementById('productoModal');
        const modalInstance = bootstrap.Modal.getInstance(modalEl);
        if (modalInstance) modalInstance.hide();
        
        // Reload data
        await loadInventory();
    } catch (error) {
        // Error is handled in apiFetch
    } finally {
        btn.classList.remove('disabled');
        spinner.classList.add('d-none');
    }
}

async function deleteProduct(id) {
    if (!confirm('¿Seguro que deseas desactivar este producto? (Borrado Lógico)')) return;

    try {
        await apiFetch(`/catalog/productos/${id}/`, {
            method: 'DELETE'
        });
        showToast('Producto desactivado', 'info');
        await loadInventory();
    } catch (error) {
        // Error is handled in apiFetch
    }
}
