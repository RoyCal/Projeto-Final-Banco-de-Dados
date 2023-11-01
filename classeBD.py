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
        self.atualizarClientes()
        self.atualizarVendedores()
        
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

        self.produtoQtd = {}
        for produto in self.listaProdutos:
            self.produtoQtd[produto[0]] = produto[2]

        self.produtoPreco = {}
        for produto in self.listaProdutos:
            self.produtoPreco[produto[0]] = produto[1]

    def atualizarClientes(self):
        comando = f'SELECT * FROM clientes'             
        self.cursor.execute(comando)             
        self.listaClientes = self.cursor.fetchall() 

        self.listaCpfCliente = []
        for cliente in self.listaClientes:
            self.listaCpfCliente.append(cliente[2]) 

    def atualizarVendedores(self):
        comando = f'SELECT * FROM vendedores'             
        self.cursor.execute(comando)             
        self.listaVendedores = self.cursor.fetchall()

        self.listaCpfVendedor = []
        for vendedor in self.listaVendedores:
            self.listaCpfVendedor.append(vendedor[2])

    def criarBanco(self):   
        comando = f'CREATE DATABASE banco_projeto; USE banco_projeto; CREATE TABLE produtos(nome_produto varchar(50), valor int, quantidade int); CREATE TABLE vendas(id_venda int auto_increment, produto_vendido varchar(50), qtd int, valor_venda int, cpf_vendedor varchar(50), cpf_cliente varchar(50), mes int, ano int, primary key(id_venda)); CREATE TABLE vendedores(nome_vendedor varchar(50), sobrenome_vendedor varchar(50), cpf_vendedor varchar(11) primary key); CREATE TABLE clientes(nome_cliente varchar(50), sobrenome_cliente varchar(50), cpf_cliente varchar(11) PRIMARY KEY)' 
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

    def cadastrarCliente(self, nome, sobrenome, CPF):
        comando = f'INSERT INTO clientes (nome_cliente, sobrenome_cliente, cpf_cliente) VALUES ("{nome}", "{sobrenome}", "{CPF}")'
        self.cursor.execute(comando)
        self.conexao.commit()

        self.atualizarClientes()

    def cadastrarVendedor(self, nome, sobrenome, CPF):
        comando = f'INSERT INTO vendedores (nome_vendedor, sobrenome_vendedor, cpf_vendedor) VALUES ("{nome}", "{sobrenome}", "{CPF}")'
        self.cursor.execute(comando)
        self.conexao.commit()

        self.atualizarVendedores()

    def listar_menos_que_5(self):
        comando = f'SELECT * FROM produtos WHERE quantidade < 5'
        self.cursor.execute(comando)             
        resultado = self.cursor.fetchall()

        lista = ''
        
        for produto in resultado:
            lista += f'Nome: {produto[0]}\nValor: R${produto[1]},00\nQuantidade: {produto[2]}\n\n'

        return lista

    def registrarVenda(self, produto, quantidade, cpfVendedor, cpfcliente, mes, ano):
        comando = f'INSERT INTO vendas (produto_vendido, qtd, valor_venda, cpf_vendedor, cpf_cliente, mes, ano) VALUES ("{produto}", {quantidade}, {quantidade*self.produtoPreco[produto]}, "{cpfVendedor}", "{cpfcliente}", {mes}, {ano})'
        self.cursor.execute(comando)
        self.conexao.commit()

    def returnCliente(self, cpf):
        comando = f'SELECT * FROM clientes WHERE cpf_cliente = "{cpf}"'
        self.cursor.execute(comando)
        
        cliente = self.cursor.fetchall()

        return f'Nome: {cliente[0][0]} {cliente[0][1]}, CPF: {cliente[0][2]}'

    def returnHistoricoCliente(self, cpf):
        comando = f'SELECT * FROM vendas WHERE cpf_cliente = "{cpf}"'
        self.cursor.execute(comando)

        historico = self.cursor.fetchall()

        string = ''

        for compra in historico:
            string += f'\nid da venda: {compra[0]}, Produto: {compra[1]}, Quantidade: {compra[2]}, Valor: {compra[3]}, Data: {compra[6]}/{compra[7]}'

        return string

    def returnRelatorioVendas(self):
        relatorio = ''

        for vendedor in self.listaVendedores:
            cpfVendedor = vendedor[2]
            nomeVendedor = f'{vendedor[0]} {vendedor[1]}'

            relatorio += nomeVendedor

            valorTotal = 0

            comando = f'SELECT * FROM vendas WHERE cpf_vendedor = "{cpfVendedor}"'
            self.cursor.execute(comando)

            vendas = self.cursor.fetchall()

            for compra in vendas:
                relatorio += f'\nid da venda: {compra[0]}, Produto: {compra[1]}, Quantidade: {compra[2]}, Valor: {compra[3]}, Data: {compra[6]}/{compra[7]}'
                valorTotal += compra[3]

            relatorio += f"\nValor total vendido: {valorTotal}\n\n"

        return relatorio

    def close(self):
        self.cursor.close()
        self.conexao.close()