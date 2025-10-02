Criação do banco de dados:

CREATE DATABASE IF NOT EXISTS mercado_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mercado_db;

-- Tabela de produtos
CREATE TABLE IF NOT EXISTS produtos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tipo VARCHAR(100) NOT NULL,
  descricao TEXT,
  valor DECIMAL(10,2) NOT NULL,
  peso DECIMAL(10,3),
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Instalação do requirements.txt

pip install -r requirements.txt
