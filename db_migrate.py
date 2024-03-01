import os

import psycopg2

class DbMigrate:
    def __init__(self):
        self.__criar_db = True
        self.__ativo = True

    @property
    def __db_config(self) -> dict:
        return {
            "host": "localhost",
            "db_name": "teste",
            "user": "postgres",
            "senha": "root"
        }

    def __executar_query(self, sql: str):
        db_config = self.__db_config
        if "CREATE DATABASE" in sql:
            db_config["db_name"] = "postgres"

        is_tem_resultado = sql.startswith("SELECT")

        res = []
        with psycopg2.connect(
            host=db_config["host"],
            database=db_config["db_name"],
            user=db_config["user"],
            password=db_config["senha"]
        ) as con:
            cursor = con.cursor()
            cursor.execute(sql)
            if is_tem_resultado:
                res = cursor.fetchall()
            else:
                con.commit()
            cursor.close()

        return res

    def migrate(self):
        print(f"Info: Iniciando db_migrate [ATIVO={self.__ativo}]")

        if not self.__ativo:
            return

        if self.__criar_db:
            print(f"Info: Db_migrate - Criando base de dados")

            # Verifique se o banco de dados existe
            if not self.__executar_query("SELECT 1 FROM pg_database WHERE datname = '%s'" % self.__db_config["db_name"]):
                sql = "CREATE DATABASE %s" % self.__db_config["db_name"]
                self.__executar_query(sql)

        print(f"Info: Db_migrate - Criando tabela do migrate")
        sql = "CREATE TABLE IF NOT EXISTS db_migrate (\
            id SERIAL PRIMARY KEY, \
            dt_execucao TIMESTAMP NOT NULL, \
            script VARCHAR(250) NOT NULL)"
        self.__executar_query(sql)

        pasta = "scripts/"
        for script in sorted(os.listdir(pasta)):
            if not script.endswith(".sql"):
                continue

            with open(f"{pasta}/{script}", "r", encoding="utf-8") as f:
                res = self.__executar_query("SELECT * FROM db_migrate WHERE script = '%s'" % script)
                if res:
                    continue

                print(f"Info: Executando Db_migrate - {script}")

                sql = f.read()
                for query in sql.split(";"):
                    if query.strip():
                        self.__executar_query(query)

                sql = "INSERT INTO db_migrate (dt_execucao, script) VALUES (CURRENT_TIMESTAMP, '%s')" % script
                self.__executar_query(sql)

DbMigrate().migrate()