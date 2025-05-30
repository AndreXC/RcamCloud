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



#server
CREATE TABLE file_hashes (
    id SERIAL PRIMARY KEY,
    filename TEXT UNIQUE NOT NULL,
    hash TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



#client
CREATE TABLE retry_actions (
    id SERIAL PRIMARY KEY,
    action TEXT NOT NULL,
    args JSONB NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    executado BOOLEAN DEFAULT FALSE
);


CREATE OR REPLACE FUNCTION delete_executed_actions()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.executado = TRUE THEN
        DELETE FROM retry_actions WHERE id = NEW.id;
    END IF;
    RETURN NULL; -- evitar UPDATE após DELETE
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_delete_after_execution
AFTER UPDATE ON retry_actions
FOR EACH ROW
WHEN (NEW.executado = TRUE)
EXECUTE FUNCTION delete_executed_actions();



CREATE TABLE historico_acoes (
    id SERIAL PRIMARY KEY,
    acao TEXT NOT NULL,
    data_acao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);