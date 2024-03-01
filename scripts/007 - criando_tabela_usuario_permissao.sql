CREATE TABLE USUARIO_PERMISSAO (
    ID_USUARIO_PERMISSAO SERIAL PRIMARY KEY,
    ID_USUARIO INT REFERENCES USUARIO(ID_USUARIO),
    TIPO_PERMISSAO INT REFERENCES TIPO_PERMISSAO(ID_PERMISSAO),
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);