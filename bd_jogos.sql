CREATE TABLE jogador (
    idjogador SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    datacriacaoconta DATE NOT NULL,
    nivel INTEGER DEFAULT 1
);

CREATE TABLE jogo (
    idjogo SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    genero VARCHAR(50),
    datalancamento DATE
);

CREATE TABLE partidas (
    idpartida SERIAL PRIMARY KEY,
    idjogador INTEGER REFERENCES jogador(idjogador) ON DELETE CASCADE,
    idjogo INTEGER REFERENCES jogo(idjogo) ON DELETE CASCADE,
    datapartida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duracao_minutos INTEGER
);

CREATE TABLE pontuacao (
    idpontuacao SERIAL PRIMARY KEY,
    idjogador INTEGER REFERENCES jogador(idjogador) ON DELETE CASCADE,
    idpartida INTEGER REFERENCES partidas(idpartida) ON DELETE CASCADE,
    valor INTEGER NOT NULL,
    datapontuacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ranking (
    idranking SERIAL PRIMARY KEY,
    idjogador INTEGER REFERENCES jogador(idjogador) ON DELETE CASCADE UNIQUE,
    posicao INTEGER NOT NULL,
    pontuacao INTEGER DEFAULT 0,
    dataregistro DATE DEFAULT CURRENT_DATE
);

CREATE TABLE conquista (
    idconquista SERIAL PRIMARY KEY,
    idjogador INTEGER REFERENCES jogador(idjogador) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    dataconquista DATE DEFAULT CURRENT_DATE
);

CREATE TABLE estatistica (
    idestatistica SERIAL PRIMARY KEY,
    idjogador INTEGER REFERENCES jogador(idjogador) ON DELETE CASCADE,
    partidas_jogadas INTEGER DEFAULT 0,
    vitorias INTEGER DEFAULT 0,
    derrotas INTEGER DEFAULT 0,
    total_pontos INTEGER DEFAULT 0
);

INSERT INTO jogador (nome, email, datacriacaoconta, nivel) VALUES
('João Silva', 'joao@email.com', '2024-01-15', 10),
('Maria Santos', 'maria@email.com', '2024-01-20', 15),
('Pedro Costa', 'pedro@email.com', '2024-02-01', 8);

INSERT INTO jogo (nome, genero, datalancamento) VALUES
('Aventura Épica', 'Aventura', '2023-05-10'),
('Corrida Radical', 'Corrida', '2023-08-22'),
('Quebra-Cabeça', 'Puzzle', '2024-01-05');

INSERT INTO partidas (idjogador, idjogo, datapartida, duracao_minutos) VALUES
(1, 1, '2024-02-10 14:30:00', 45),
(2, 1, '2024-02-10 15:20:00', 60),
(1, 2, '2024-02-11 10:00:00', 30),
(3, 3, '2024-02-11 11:15:00', 50);

INSERT INTO pontuacao (idjogador, idpartida, valor) VALUES
(1, 1, 1500),
(2, 2, 1800),
(1, 3, 1200),
(3, 4, 2000);

INSERT INTO ranking (idjogador, posicao, pontuacao) VALUES
(1, 2, 2700),
(2, 1, 1800),
(3, 3, 2000);

INSERT INTO conquista (idjogador, nome, descricao) VALUES
(1, 'Primeira Vitória', 'Ganhou sua primeira partida'),
(2, 'Veterano', 'Completou 10 partidas'),
(3, 'Pontuação Máxima', 'Alcançou 2000 pontos');

INSERT INTO estatistica (idjogador, partidas_jogadas, vitorias, derrotas, total_pontos) VALUES
(1, 2, 1, 1, 2700),
(2, 1, 1, 0, 1800),
(3, 1, 1, 0, 2000);

SELECT r.posicao, j.nome, r.pontuacao
FROM ranking r
JOIN jogador j ON r.idjogador = j.idjogador
ORDER BY r.posicao;

SELECT j.nome, SUM(p.valor) AS total_pontos
FROM jogador j
JOIN pontuacao p ON j.idjogador = p.idjogador
GROUP BY j.nome
ORDER BY total_pontos DESC;