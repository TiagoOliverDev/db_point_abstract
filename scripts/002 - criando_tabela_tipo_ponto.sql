CREATE TABLE TIPO_PONTO (
    ID_TIPO_PONTO SERIAL PRIMARY KEY,
    TIPO VARCHAR(100) NOT NULL,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
