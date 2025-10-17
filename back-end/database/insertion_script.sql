INSERT OR IGNORE INTO funcao (nome_funcao) VALUES
('Scrum Master'),
('Developer'),
('Product Owner');

INSERT OR IGNORE INTO prioridade_story (nivel_story) VALUES
('Alta'),
('Media'),
('Baixa');

INSERT OR IGNORE INTO prioridade_task (nivel_task) VALUES
('Alta'),
('Media'),
('Baixa');

INSERT INTO estado_task (nome_estado) VALUES
('A fazer'),
('Em progresso'),
('Em revisao'),
('Concluido');
