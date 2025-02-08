CREATE TABLE gastos (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    precio NUMERIC(10, 2) NOT NULL,
    descripcion TEXT
);

