-- 1. Habilitar extensión para generar UUIDs automáticamente
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Tabla Empresa (Tenant principal)
CREATE TABLE empresa (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(100) NOT NULL,
    giro VARCHAR(100),
    descripcion TEXT,
    logo_url TEXT,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL, -- Aquí guardas el hash, no la clave real
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabla Producto
CREATE TABLE producto (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio NUMERIC(12, 2) NOT NULL CHECK (precio >= 0),
    stock_actual INT DEFAULT 0,
    estado VARCHAR(20) DEFAULT 'activo',
    empresa_id UUID NOT NULL REFERENCES empresa(id) ON DELETE CASCADE
);

-- 4. Tabla Venta (Cabecera)
CREATE TABLE venta (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    nombre_cliente VARCHAR(100),
    nombre_vendedor VARCHAR(100),
    total_venta NUMERIC(12, 2) DEFAULT 0,
    empresa_id UUID NOT NULL REFERENCES empresa(id) ON DELETE CASCADE
);

-- 5. Tabla Detalle de Venta (Para soportar múltiples productos por venta)
CREATE TABLE venta_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    venta_id UUID NOT NULL REFERENCES venta(id) ON DELETE CASCADE,
    producto_id UUID NOT NULL REFERENCES producto(id),
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(12, 2) NOT NULL, -- Se guarda el precio del momento de la venta
    subtotal NUMERIC(12, 2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    empresa_id UUID NOT NULL REFERENCES empresa(id) ON DELETE CASCADE
);

-- 6. Configuración de Row Level Security (RLS)
-- Activamos la seguridad en todas las tablas que contienen datos de los clientes
ALTER TABLE producto ENABLE ROW LEVEL SECURITY;
ALTER TABLE venta ENABLE ROW LEVEL SECURITY;
ALTER TABLE venta_items ENABLE ROW LEVEL SECURITY;

-- 7. Crear la política de aislamiento (Isolation Policy)
-- Esta política asume que tu backend enviará el ID de la empresa en una variable de sesión
CREATE POLICY empresa_isolation_policy_productos ON producto
    USING (empresa_id = current_setting('app.current_tenant_id')::uuid);

CREATE POLICY empresa_isolation_policy_ventas ON venta
    USING (empresa_id = current_setting('app.current_tenant_id')::uuid);

CREATE POLICY empresa_isolation_policy_items ON venta_items
    USING (empresa_id = current_setting('app.current_tenant_id')::uuid);


WITH nuevas_empresas AS (
    INSERT INTO empresa (nombre, giro, descripcion, email, password_hash)
    VALUES 
        ('TechNova Solutions', 'Tecnología', 'Venta de hardware y servicios cloud.', 'contacto@technova.com', 'hash_provisional_1'),
        ('Café Aroma Real', 'Alimentos y Bebidas', 'Distribuidora de café orgánico artesanal.', 'ventas@aromareal.com', 'hash_provisional_2'),
        ('Moda Urbana', 'Textil', 'Tienda de ropa de diseño independiente.', 'info@modaurbana.com', 'hash_provisional_3')
    RETURNING id, nombre
)
INSERT INTO producto (nombre, descripcion, precio, stock_actual, empresa_id)
VALUES 
    -- Productos para TechNova
    ('Laptop Pro 15', 'Laptop con 16GB RAM y 512GB SSD', 1200.00, 15, (SELECT id FROM nuevas_empresas WHERE nombre = 'TechNova Solutions')),
    ('Mouse Ergonómico', 'Mouse inalámbrico con sensor óptico', 45.50, 50, (SELECT id FROM nuevas_empresas WHERE nombre = 'TechNova Solutions')),
    
    -- Productos para Café Aroma Real
    ('Café de Grano 1kg', 'Café tostado medio de altura', 25.00, 100, (SELECT id FROM nuevas_empresas WHERE nombre = 'Café Aroma Real')),
    ('Prensa Francesa', 'Prensa de acero inoxidable 1L', 35.00, 20, (SELECT id FROM nuevas_empresas WHERE nombre = 'Café Aroma Real')),
    
    -- Productos para Moda Urbana
    ('Camiseta Basic Black', 'Algodón 100% orgánico', 15.99, 200, (SELECT id FROM nuevas_empresas WHERE nombre = 'Moda Urbana')),
    ('Jeans Slim Fit', 'Mezclilla elástica azul oscuro', 49.90, 80, (SELECT id FROM nuevas_empresas WHERE nombre = 'Moda Urbana'));

SET app.current_tenant_id = '4bf1fb2a-189f-495b-b3d1-67c941fcd0f6';
SELECT * FROM producto;