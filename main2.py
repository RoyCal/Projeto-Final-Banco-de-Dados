from classeBD import *
import os

bd = BancoDeDados()

while True:
    os.system("cls")
    senha = input("Acessar plataforma: ")

    if not bd.conectar(senha):
        continue
    else:
        break

def cadastrarCliente():
    os.system("cls")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    cpf = input("CPF: ")

    bd.cadastrarCliente(nome, sobrenome, cpf)

def cadastrarVendedor():
    os.system("cls")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    cpf = input("CPF: ")

    bd.cadastrarVendedor(nome, sobrenome, cpf)

def vender():
    carrinho = {}

    while True:
        os.system("cls")

        produto = input("Qual produto quer adicionar ao carrinho: ")

        if produto not in bd.nomes_produtos:
            continue

        qtd = int(input("Quanto do produto quer comprar: "))

        if qtd > bd.produtoQtd[produto]:
            continue

        carrinho[produto] = qtd
            
        finish = int(input("Algo mais? (1)sim (0)nao "))

        if finish:
            continue

        while True:
            os.system("cls")
            cpfCliente = input("Informe o cpf do cliente: ")

            if cpfCliente in bd.listaCpfCliente:
                break
            else:
                continue
        
        while True:
            os.system("cls")
            cpfVendedor = input("Informe o cpf do vendedor: ")

            if cpfVendedor in bd.listaCpfVendedor:
                break
            else:
                continue

        for produto in carrinho:
            bd.alterarQuantidade(produto, -carrinho[produto])
            bd.registrarVenda(produto, carrinho[produto], cpfVendedor, cpfCliente, 11, 2023)

        bd.atualizarAtributos

        break

def listarProdutos():
    print(bd.listar_todos())

def listarProdutosFiltro():
    pass

def listarProdutosMenosQue5():
    print(bd.listar_menos_que_5())

def relatorioVendedores():
    os.system("cls")

    print(bd.returnRelatorioVendas())

    input()

def historicoCliente():
    os.system("cls")

    cpfCliente = input("Qual o cpf do cliente: ")

    print(bd.returnHistoricoCliente(cpfCliente))

    input()

def cadastroCliente():
    os.system("cls")

    cpfCliente = input("Qual o cpf do cliente: ")

    print(bd.returnCliente(cpfCliente))

    input()

def printMenu():
    menu = '''(1) - Cadastrar cliente\n(2) - Cadastrar vendedor\n(3) - Vender\n(4) - Listar produtos\n(5) - Relatorio dos vendedores\n(6) - Historico de compras do cliente\n(7) - Cadastro do cliente\n(8) - Fechar\n'''
    
    os.system("cls")
    print(menu)

while True:
    printMenu()

    choice = input()

    match(choice):
        case '1':
            cadastrarCliente()
        case '2':
            cadastrarVendedor()
        case '3':
            vender()
        case '4':
            listarProdutos()
            input()
        case '5':
            relatorioVendedores()
        case '6':
            historicoCliente()
        case '7':
            cadastroCliente()
        case '8':
            break
        case _:
            continue

bd.close()