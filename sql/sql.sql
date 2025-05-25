CREATE TABLE tokens_autenticacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    token_dispositivo VARCHAR(255) NOT NULL UNIQUE,
    token VARCHAR(128) NOT NULL,
    data_criacao DATETIME NOT NULL,
    data_validacao DATETIME NOT NULL,
    idUser INT NOT NULL,
    username VARCHAR(100) NOT NULL,
    INDEX (idUser),
    INDEX (username)
);

CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    erro_message TEXT NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    client_id VARCHAR(100) NOT NULL
)

ALTER TABLE logs ADD COLUMN tipo ENUM('cliente', 'server') NOT NULL DEFAULT 'cliente';

