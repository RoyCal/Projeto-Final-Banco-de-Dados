import mysql.connector

class BancoDeDados:
    def __init__(self):
        pass

    def conectar(self, senha):
        try:
            self.conexao = mysql.connector.connect(host = 'localhost', user = 'root', password = senha, database = 'banco_projeto')
            self.cursor = self.conexao.cursor()
        except:
            return 0
        
        try:
            self.criarBanco()
        except:
            pass

        self.atualizarAtributos()
        
        return 1
    
    def atualizarAtributos(self):
        comando = f'SELECT * FROM produtos'             
        self.cursor.execute(comando)             
        self.listaProdutos = self.cursor.fetchall()          

        self.nProdutos = self.listaProdutos.__len__()

        self.valorEstoque = 0
        for produto in self.listaProdutos:
            self.valorEstoque += produto[1]*produto[2]

        self.nomes_produtos = []
        for produto in self.listaProdutos:
            self.nomes_produtos.append(produto[0])

        self.armazenamento = 0
        for produto in self.listaProdutos:
            self.armazenamento += produto[2]

    def criarBanco(self):   
        comando = f'CREATE DATABASE banco_projeto; USE banco_projeto; CREATE TABLE produtos(nome_produto varchar(50), valor int, quantidade int)' 
        self.cursor.execute(comando)

    def produtoExiste(self, nome):
        comando = f'SELECT * FROM produtos WHERE nome_produto = "{nome}"'
        self.cursor.execute(comando)
        resultado = self.cursor.fetchall()
        if resultado.__len__():
            return 1
        else:
            return 0

    def inserir(self, nome, preco, quantidade): #CREATE
        comando = f'INSERT INTO produtos (nome_produto, valor, quantidade) VALUES ("{nome}", {preco}, {quantidade})'                   
        self.cursor.execute(comando)
        self.conexao.commit()
        self.atualizarAtributos()

    def listar_todos(self): #READ
        comando = f'SELECT * FROM produtos'             
        self.cursor.execute(comando)             
        resultado = self.cursor.fetchall()

        lista = ''
        
        for produto in resultado:
            lista += f'Nome: {produto[0]}\nValor: R${produto[1]},00\nQuantidade: {produto[2]}\n\n'

        return lista

    def alterarValor(self, nome, novoValor): #UPDATE
        if not self.produtoExiste(nome):
            print("Produto inexistente")
            return

        comando = f'UPDATE produtos SET valor = {novoValor} WHERE nome_produto = "{nome}"'                   
        self.cursor.execute(comando)
        self.conexao.commit()

        self.atualizarAtributos()

    def alterarQuantidade(self, nome, inc):
        if not self.produtoExiste(nome):
            print("Produto inexistente")
            return

        comando = f'UPDATE produtos SET quantidade = quantidade + {inc} WHERE nome_produto = "{nome}"'
        self.cursor.execute(comando)
        self.conexao.commit()

        self.atualizarAtributos()

    def remover(self, nome): #DELETE
        if not self.produtoExiste(nome):
            print("Produto inexistente")
            return

        comando = f'DELETE FROM produtos WHERE nome_produto = "{nome}"'                   
        self.cursor.execute(comando)
        self.conexao.commit()

        self.atualizarAtributos()

    def close(self):
        self.cursor.close()
        self.conexao.close()