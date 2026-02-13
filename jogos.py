import psycopg2
from abc import ABC, abstractmethod

class ConexaoSingleton:
    _instancia = None
    
    @classmethod
    def conectar(cls):
        if cls._instancia is None:
            cls._instancia = psycopg2.connect(
                host="localhost",
                database="jp_jogos",
                user="postgres",
                password="urssL1922"
            )
        return cls._instancia
    
    @classmethod
    def fechar(cls):
        if cls._instancia:
            cls._instancia.close()
            cls._instancia = None

class JogadorDAO(ABC):
    @abstractmethod
    def inserir(self, nome, email, data, nivel):
        pass
    
    @abstractmethod
    def listar(self):
        pass
    
    @abstractmethod
    def atualizar(self, idj, nome, email, data, nivel):
        pass
    
    @abstractmethod
    def deletar(self, idj):
        pass


class TabelaDAO(ABC):
    @abstractmethod
    def listar_todos(self, nome_tabela):
        pass


class ConsultaDAO(ABC):
    @abstractmethod
    def join_ranking_jogador(self):
        pass
    
    @abstractmethod
    def groupby_pontuacao_jogador(self):
        pass

class JogadorPostgresDAO(JogadorDAO):
    def __init__(self, conexao):
        self.conexao = conexao
    
    def inserir(self, nome, email, data, nivel):
        cur = self.conexao.cursor()
        cur.execute("""
            INSERT INTO jogador(nome, email, datacriacaoconta, nivel)
            VALUES (%s, %s, %s, %s)
        """, (nome, email, data, nivel))
        self.conexao.commit()
        cur.close()
    
    def listar(self):
        cur = self.conexao.cursor()
        cur.execute("SELECT * FROM jogador ORDER BY idjogador")
        jogadores = cur.fetchall()
        cur.close()
        return jogadores
    
    def atualizar(self, idj, nome, email, data, nivel):
        cur = self.conexao.cursor()
        cur.execute("""
            UPDATE jogador
            SET nome=%s, email=%s, datacriacaoconta=%s, nivel=%s
            WHERE idjogador=%s
        """, (nome, email, data, nivel, idj))
        self.conexao.commit()
        cur.close()
    
    def deletar(self, idj):
        cur = self.conexao.cursor()
        cur.execute("DELETE FROM jogador WHERE idjogador=%s", (idj,))
        self.conexao.commit()
        cur.close()


class TabelaPostgresDAO(TabelaDAO):
    def __init__(self, conexao):
        self.conexao = conexao
    
    def listar_todos(self, nome_tabela):
        cur = self.conexao.cursor()
        cur.execute(f"SELECT * FROM {nome_tabela}")
        dados = cur.fetchall()
        cur.close()
        return dados


class ConsultaPostgresDAO(ConsultaDAO):
    def __init__(self, conexao):
        self.conexao = conexao
    
    def join_ranking_jogador(self):
        cur = self.conexao.cursor()
        cur.execute("""
            SELECT r.posicao, j.nome, r.pontuacao
            FROM ranking r
            JOIN jogador j ON r.idjogador = j.idjogador
            ORDER BY r.posicao
        """)
        dados = cur.fetchall()
        cur.close()
        return dados
    
    def groupby_pontuacao_jogador(self):
        cur = self.conexao.cursor()
        cur.execute("""
            SELECT j.nome, SUM(p.valor) AS total_pontos
            FROM jogador j
            JOIN pontuacao p ON j.idjogador = p.idjogador
            GROUP BY j.nome
            ORDER BY total_pontos DESC
        """)
        dados = cur.fetchall()
        cur.close()
        return dados

class JogadorService:
    def __init__(self, jogador_dao):
        self.jogador_dao = jogador_dao
    
    def inserir_jogador(self):
        nome = input("Nome: ")
        email = input("Email: ")
        data = input("Data Criação (YYYY-MM-DD): ")
        nivel = int(input("Nível: "))
        
        self.jogador_dao.inserir(nome, email, data, nivel)
        print("✅ Jogador inserido com sucesso!")
    
    def listar_jogadores(self):
        jogadores = self.jogador_dao.listar()
        print("\n=== LISTA DE JOGADORES ===")
        for j in jogadores:
            print(j)
    
    def atualizar_jogador(self):
        idj = int(input("ID do jogador: "))
        nome = input("Novo nome: ")
        email = input("Novo email: ")
        data = input("Nova data criação (YYYY-MM-DD): ")
        nivel = int(input("Novo nível: "))
        
        self.jogador_dao.atualizar(idj, nome, email, data, nivel)
        print("✅ Jogador atualizado com sucesso!")
    
    def deletar_jogador(self):
        idj = int(input("ID do jogador para deletar: "))
        self.jogador_dao.deletar(idj)
        print("✅ Jogador deletado com sucesso!")


class TabelaService:
    def __init__(self, tabela_dao):
        self.tabela_dao = tabela_dao
    
    def listar_tabela(self, nome_tabela):
        dados = self.tabela_dao.listar_todos(nome_tabela)
        print(f"\n=== {nome_tabela.upper()} ===")
        for linha in dados:
            print(linha)


class ConsultaService:
    def __init__(self, consulta_dao):
        self.consulta_dao = consulta_dao
    
    def consulta_join(self):
        dados = self.consulta_dao.join_ranking_jogador()
        print("\n=== JOIN (RANKING + JOGADOR) ===")
        for linha in dados:
            print(linha)
    
    def consulta_groupby(self):
        dados = self.consulta_dao.groupby_pontuacao_jogador()
        print("\n=== (TOTAL DE PONTOS POR JOGADOR) ===")
        for linha in dados:
            print(linha)

def menu():
    conn = ConexaoSingleton.conectar()
    
    jogador_dao = JogadorPostgresDAO(conn)
    tabela_dao = TabelaPostgresDAO(conn)
    consulta_dao = ConsultaPostgresDAO(conn)
    
    jogador_service = JogadorService(jogador_dao)
    tabela_service = TabelaService(tabela_dao)
    consulta_service = ConsultaService(consulta_dao)
    
    while True:
        print("\n========== MENU ==========")
        print("1 - Inserir Jogador")
        print("2 - Listar Jogadores")
        print("3 - Atualizar Jogador")
        print("4 - Deletar Jogador")
        print("5 - Listar Jogos")
        print("6 - Listar Partidas")
        print("7 - Listar Pontuação")
        print("8 - Listar Ranking")
        print("9 - Listar Conquista")
        print("10 - Listar Estatística")
        print("11 - Ranking + jogador")
        print("12 - Ttotal de pontos por jogador")
        print("0 - Sair")

        op = input("Escolha: ")

        if op == "1":
            jogador_service.inserir_jogador()

        elif op == "2":
            jogador_service.listar_jogadores()

        elif op == "3":
            jogador_service.atualizar_jogador()

        elif op == "4":
            jogador_service.deletar_jogador()

        elif op == "5":
            tabela_service.listar_tabela("jogo")

        elif op == "6":
            tabela_service.listar_tabela("partidas")

        elif op == "7":
            tabela_service.listar_tabela("pontuacao")

        elif op == "8":
            tabela_service.listar_tabela("ranking")

        elif op == "9":
            tabela_service.listar_tabela("conquista")

        elif op == "10":
            tabela_service.listar_tabela("estatistica")

        elif op == "11":
            consulta_service.consulta_join()

        elif op == "12":
            consulta_service.consulta_groupby()

        elif op == "0":
            print("Saindo...")
            ConexaoSingleton.fechar()
            break

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu()