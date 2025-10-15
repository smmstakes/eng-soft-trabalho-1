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
        "nivel_story" TEXT,
        PRIMARY KEY("id_user_story" AUTOINCREMENT),
        FOREIGN KEY("id_projeto") REFERENCES "projeto"("id_projeto"),
        FOREIGN KEY("nivel_story") REFERENCES "prioridade_story"("nivel_story")
);
CREATE TABLE IF NOT EXISTS "prioridade_story"(
        "nivel_story" TEXT,
        PRIMARY KEY("nivel_story")
);
CREATE TABLE IF NOT EXISTS "task" (
        "id_task"       INTEGER,
        "id_sprint"     INTEGER,
        "cpf"   TEXT,
        "nome_estado"   TEXT,
        "descricao_task"        TEXT,
        "nivel_task" TEXT,
        PRIMARY KEY("id_task" AUTOINCREMENT),
        FOREIGN KEY("id_sprint") REFERENCES "sprint"("id_sprint"),
        FOREIGN KEY("nome_estado") REFERENCES "estado_task"("nome_estado"),
        FOREIGN KEY("nivel_task") REFERENCES "prioridade_task"("nivel_task")
);
CREATE TABLE IF NOT EXISTS "prioridade_task"(
        "nivel_task" TEXT,
        PRIMARY KEY("nivel_task")
);
CREATE TABLE IF NOT EXISTS "estado_task" (
        "nome_estado"   TEXT,
        PRIMARY KEY("nome_estado")
);
CREATE TABLE IF NOT EXISTS "sprint" (
        "id_sprint"     INTEGER,
        "meta"  TEXT,
        "inicio" DATE,
        "termino" DATE,
        "revisao_sprint"        TEXT,
        PRIMARY KEY("id_sprint" AUTOINCREMENT)
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
CREATE TABLE IF NOT EXISTS "user_story_sprint" (
        "id_user_story" INTEGER,
        "id_sprint" INTEGER, 
        PRIMARY KEY("id_user_story", "id_sprint"),
        FOREIGN KEY("id_user_story") REFERENCES "user_story"("id_user_story"),
        FOREIGN KEY("id_sprint") REFERENCES "sprint"("id_sprint")
);