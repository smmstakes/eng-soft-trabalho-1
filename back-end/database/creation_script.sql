CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "funcao" (
        "nome_funcao"   TEXT,
        PRIMARY KEY("nome_funcao")
);
CREATE TABLE IF NOT EXISTS "usuario" (
        "cpf"   TEXT,
        "email" TEXT NOT NULL,
        "nome"  TEXT NOT NULL,
        "senha" TEXT NOT NULL,
        PRIMARY KEY("cpf")
);
CREATE TABLE IF NOT EXISTS "user_story" (
        "id_user_story" INTEGER,
        "id_projeto"    INTEGER,
        "titulo_user_story"     TEXT,
        "objetivo"      TEXT,
        "beneficio"     TEXT,
        PRIMARY KEY("id_user_story" AUTOINCREMENT),
        FOREIGN KEY("id_projeto") REFERENCES "projeto"("id_projeto")
);
CREATE TABLE IF NOT EXISTS "task" (
        "id_task"       INTEGER,
        "id_sprint"     INTEGER,
        "cpf"   TEXT,
        "nome_estado"   TEXT,
        "descricao_task"        TEXT,
        PRIMARY KEY("id_task" AUTOINCREMENT),
        FOREIGN KEY("id_sprint") REFERENCES "sprint"("id_sprint"),
        FOREIGN KEY("nome_estado") REFERENCES "estado_task"("nome_estado")
);
CREATE TABLE IF NOT EXISTS "estado_task" (
        "nome_estado"   TEXT,
        PRIMARY KEY("nome_estado")
);
CREATE TABLE IF NOT EXISTS "sprint" (
        "id_sprint"     INTEGER,
        "id_user_story" INTEGER,
        "meta"  TEXT,
        "prazo" DATE,
        "revisao_sprint"        TEXT,
        PRIMARY KEY("id_sprint" AUTOINCREMENT),
        FOREIGN KEY("id_user_story") REFERENCES "user_story"("id_user_story")
);
CREATE TABLE IF NOT EXISTS "usuario_projeto" (
        "cpf"   TEXT,
        "id_projeto"    INTEGER,
        "nome_funcao"   TEXT,
        PRIMARY KEY("cpf","id_projeto"),
        FOREIGN KEY("cpf") REFERENCES "usuario"("cpf"),
        FOREIGN KEY("id_projeto") REFERENCES "projeto"("id_projeto"),
        FOREIGN KEY("nome_funcao") REFERENCES "funcao"("nome_funcao")
);
CREATE TABLE IF NOT EXISTS "projeto" (
        "id_projeto"    INTEGER,
        "titulo_projeto"        TEXT,
        "descricao"     TEXT,
        "cpf"   TEXT,
        PRIMARY KEY("id_projeto" AUTOINCREMENT),
        FOREIGN KEY("cpf") REFERENCES "usuario"("cpf")
);