CREATE TABLE pedidos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cliente TEXT,
  total REAL,
  estado TEXT
);

CREATE TABLE clientes (
  nombre TEXT,
  alta TEXT
);

-- tabla de 2019 que ya nadie usa pero de la que sigue leyendo un endpoint
CREATE TABLE pedidos_2019 (
  id INTEGER PRIMARY KEY,
  cliente TEXT,
  total REAL
);
