import customtkinter as ctk
from tkinter import *
from classeBD import *

bd = BancoDeDados()

class Gui():
    def __init__(self):
        self.count_acesso = 0
        self.count_principal = 0
        self.count_listar = 0
        self.count_adicionar = 0
        self.count_remover = 0
        self.count_buscar = 0
        self.count_venda = 0
        self.count_recebido = 0
        self.count_altValor = 0

        self.janela = ctk.CTk()
        self.acesso_frame = ctk.CTkFrame(master=self.janela, width=700, height=400)
        self.principal_frame = ctk.CTkFrame(master=self.janela, width=350, height=400)
        self.listaProdutos_frame = ctk.CTkScrollableFrame(master=self.janela, width=350, height=400, fg_color="white")
        self.adicionarProdutos_frame = ctk.CTkFrame(master=self.janela, width=350, height=400, fg_color="white")
        self.removerProdutos_frame = ctk.CTkFrame(master=self.janela, width=350, height=400, fg_color="white")
        self.buscarProdutos_frame = ctk.CTkFrame(master=self.janela, width=350, height=400, fg_color="white")
        self.vendaProdutos_frame = ctk.CTkFrame(master=self.janela, width=350, height=400, fg_color="white")
        self.recebidoProdutos_frame = ctk.CTkFrame(master=self.janela, width=350, height=400, fg_color="white")
        self.altValorProdutos_frame = ctk.CTkFrame(master=self.janela, width=350, height=400, fg_color="white")
        self.listaFramesRight = [self.listaProdutos_frame, self.adicionarProdutos_frame, self.removerProdutos_frame, self.buscarProdutos_frame, self.vendaProdutos_frame, self.recebidoProdutos_frame, self.altValorProdutos_frame]
        self.user_input1 = ctk.StringVar(master=self.janela)
        self.tema()
        self.tela()
        self.tela_acesso()
        self.janela.mainloop()
    
    def tema(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

    def tela(self):
        self.janela.geometry("700x400")
        self.janela.title("Estoque de produtos")
        self.janela.resizable(False, False)

    def tela_acesso(self):
        self.acesso_frame.pack()

        if self.count_acesso == 0:
            ctk.CTkLabel(master=self.acesso_frame, text="VPRH Pharma", width=200, font=("Times", 25), text_color="yellow").place(x=250, y=30)

            ctk.CTkLabel(master=self.acesso_frame, text="Acesso ao estoque", width=200).place(x=250, y=130)

            ctk.CTkLabel(master=self.acesso_frame, text="senha", width=200).place(x=250, y=205)

            ctk.CTkEntry(master=self.acesso_frame, show="*", textvariable=self.user_input1, placeholder_text="senha").place(x=280, y=230)

            ctk.CTkButton(master=self.acesso_frame, text="acessar", command=self.tela_principal).place(x=280, y=330)

            self.count_acesso += 1

    def listar_produtos(self):
        for frame in self.listaFramesRight:
            if frame != self.listaProdutos_frame:
                frame.pack_forget()

        self.listaProdutos_frame.pack(side=RIGHT)

        if self.count_listar == 0:
            ctk.CTkLabel(master=self.listaProdutos_frame, text="Lista de produtos", height=50, width=200, text_color="black", font=("Times", 30)).grid(row=0)

            self.count_listar += 1

        ctk.CTkLabel(master=self.listaProdutos_frame, text=bd.listar_todos(), width=350, text_color="black").grid(row=1)

        ctk.CTkLabel(master=self.listaProdutos_frame, text=f'Produtos cadastrados: {bd.nProdutos}\nValor do estoque: R${bd.valorEstoque},00\nPreenchimento do estoque: {bd.armazenamento}', width=350, text_color="black", font=("Times", 20)).grid(row=2)

    def remover_Produto(self):
        for frame in self.listaFramesRight:
            if frame != self.removerProdutos_frame:
                frame.pack_forget()
        
        self.removerProdutos_frame.pack()

        def verificarRemover():
            if nome_produto.get() == "":
                return

            if nome_produto.get() not in bd.nomes_produtos:
                ctk.CTkLabel(master=self.removerProdutos_frame, text="*produto inexistente", width=200, text_color="red").place(x=75, y=310)

                return
            else:
                ctk.CTkLabel(master=self.removerProdutos_frame, text="*produto inexistente", width=200, text_color="white").place(x=75, y=310)

            bd.remover(nome_produto.get())

            self.listar_produtos()

        nome_produto = ctk.StringVar(master=self.removerProdutos_frame)

        if self.count_remover == 0:
            ctk.CTkLabel(master=self.removerProdutos_frame, text="Nome do produto", width=200, text_color="black").place(x=75, y=141)

            ctk.CTkEntry(master=self.removerProdutos_frame, textvariable=nome_produto).place(x=105, y=166)

            ctk.CTkButton(master=self.removerProdutos_frame, text="remover", command=verificarRemover).place(x=105, y=270)

            self.count_remover += 1
        
    def alterarValor(self):
        for frame in self.listaFramesRight:
            if frame != self.altValorProdutos_frame:
                frame.pack_forget()
        
        self.altValorProdutos_frame.pack()

        def alterar():
            if nome_produto.get() == "" or novo_valor.get() == "":
                return
            
            if nome_produto.get() not in bd.nomes_produtos:
                ctk.CTkLabel(master=self.altValorProdutos_frame, text="*produto inexistente", width=350, text_color="red").place(y=310)

                return
            else:
                ctk.CTkLabel(master=self.altValorProdutos_frame, width=350, text_color="white").place(y=310)

            try:
                int(novo_valor.get())
                ctk.CTkLabel(master=self.altValorProdutos_frame, width=350, text_color="white").place(y=338)
            except:
                ctk.CTkLabel(master=self.altValorProdutos_frame, text="*valor inválido", width=350, text_color="red").place(y=338)

                return
            
            bd.alterarValor(nome_produto.get(), int(novo_valor.get()))

            self.listar_produtos()
            
        nome_produto = ctk.StringVar(master=self.altValorProdutos_frame)

        novo_valor = ctk.StringVar(master=self.altValorProdutos_frame)

        if self.count_altValor == 0:
            ctk.CTkLabel(master=self.altValorProdutos_frame, text="Nome do produto", width=200, text_color="black").place(x=75, y=76)

            ctk.CTkEntry(master=self.altValorProdutos_frame, textvariable=nome_produto).place(x=105, y=101)

            ctk.CTkLabel(master=self.altValorProdutos_frame, text="Novo valor", width=200, text_color="black").place(x=75, y=141)

            ctk.CTkEntry(master=self.altValorProdutos_frame, textvariable=novo_valor).place(x=105, y=166)

            ctk.CTkButton(master=self.altValorProdutos_frame, text="alterar", command=alterar).place(x=105, y=206)

            self.count_altValor += 1

    def estoqueRecebido(self):
        for frame in self.listaFramesRight:
            if frame != self.recebidoProdutos_frame:
                frame.pack_forget()
        
        self.recebidoProdutos_frame.pack()

        def incrementar():
            if nome_produto.get() == "" or quantidade_vendida.get() == "":
                return
            
            if nome_produto.get() not in bd.nomes_produtos:
                ctk.CTkLabel(master=self.recebidoProdutos_frame, text="*produto inexistente", width=350, text_color="red").place(y=310)

                return
            else:
                ctk.CTkLabel(master=self.recebidoProdutos_frame, width=350, text_color="white").place(y=310)

            try:
                int(quantidade_vendida.get())
                ctk.CTkLabel(master=self.recebidoProdutos_frame, width=350, text_color="white").place(y=338)
            except:
                ctk.CTkLabel(master=self.recebidoProdutos_frame, text="*quantidade inválida", width=350, text_color="red").place(y=338)

                return
            
            bd.alterarQuantidade(nome_produto.get(), int(quantidade_vendida.get()))

            self.listar_produtos()
            
        nome_produto = ctk.StringVar(master=self.recebidoProdutos_frame)

        quantidade_vendida = ctk.StringVar(master=self.recebidoProdutos_frame)

        if self.count_recebido == 0:
            ctk.CTkLabel(master=self.recebidoProdutos_frame, text="Nome do produto", width=200, text_color="black").place(x=75, y=76)

            ctk.CTkEntry(master=self.recebidoProdutos_frame, textvariable=nome_produto).place(x=105, y=101)

            ctk.CTkLabel(master=self.recebidoProdutos_frame, text="Quantidade recebida", width=200, text_color="black").place(x=75, y=141)

            ctk.CTkEntry(master=self.recebidoProdutos_frame, textvariable=quantidade_vendida).place(x=105, y=166)

            ctk.CTkButton(master=self.recebidoProdutos_frame, text="incrementar", command=incrementar).place(x=105, y=206)

            self.count_recebido += 1

    def vendaRealizada(self):
        for frame in self.listaFramesRight:
            if frame != self.vendaProdutos_frame:
                frame.pack_forget()
        
        self.vendaProdutos_frame.pack()

        def decrementar():
            if nome_produto.get() == "" or quantidade_vendida.get() == "":
                return
            
            if nome_produto.get() not in bd.nomes_produtos:
                ctk.CTkLabel(master=self.vendaProdutos_frame, text="*produto inexistente", width=350, text_color="red").place(y=310)

                return
            else:
                ctk.CTkLabel(master=self.vendaProdutos_frame, width=350, text_color="white").place(y=310)

            try:
                int(quantidade_vendida.get())
                ctk.CTkLabel(master=self.vendaProdutos_frame, width=350, text_color="white").place(y=338)
            except:
                ctk.CTkLabel(master=self.vendaProdutos_frame, text="*quantidade inválida", width=350, text_color="red").place(y=338)

                return
            
            bd.alterarQuantidade(nome_produto.get(), -int(quantidade_vendida.get()))

            self.listar_produtos()

        nome_produto = ctk.StringVar(master=self.vendaProdutos_frame)

        quantidade_vendida = ctk.StringVar(master=self.vendaProdutos_frame)

        if self.count_venda == 0:
            ctk.CTkLabel(master=self.vendaProdutos_frame, text="Nome do produto", width=200, text_color="black").place(x=75, y=76)

            ctk.CTkEntry(master=self.vendaProdutos_frame, textvariable=nome_produto).place(x=105, y=101)

            ctk.CTkLabel(master=self.vendaProdutos_frame, text="Quantidade vendida", width=200, text_color="black").place(x=75, y=141)

            ctk.CTkEntry(master=self.vendaProdutos_frame, textvariable=quantidade_vendida).place(x=105, y=166)

            ctk.CTkButton(master=self.vendaProdutos_frame, text="decrementar", command=decrementar).place(x=105, y=206)

            self.count_venda += 1

    def buscar_produto(self):
        for frame in self.listaFramesRight:
            if frame != self.buscarProdutos_frame:
                frame.pack_forget()
        
        self.buscarProdutos_frame.pack()

        def buscar():
            if nome_produto.get() == "":
                return
            
            if nome_produto.get() not in bd.nomes_produtos:
                ctk.CTkLabel(master=self.buscarProdutos_frame, text=f'produto inexistente', height=100, width=350, text_color="black").place(y=20)

                return

            for produto in bd.listaProdutos:
                if nome_produto.get() == produto[0]:
                    ctk.CTkLabel(master=self.buscarProdutos_frame, text=f'Nome: {produto[0]}\nValor: R${produto[1]},00\nQuantidade: {produto[2]}', width=350, text_color="black").place(y=50)
                

        nome_produto = ctk.StringVar(master=self.buscarProdutos_frame)

        if self.count_buscar == 0:
            ctk.CTkLabel(master=self.buscarProdutos_frame, text="Nome do produto", width=200, text_color="black").place(x=75, y=141)

            ctk.CTkEntry(master=self.buscarProdutos_frame, textvariable=nome_produto).place(x=105, y=166)

            ctk.CTkButton(master=self.buscarProdutos_frame, text="buscar", command=buscar).place(x=105, y=270)

            self.count_buscar += 1

    def adicionar_produto(self):
        for frame in self.listaFramesRight:
            if frame != self.adicionarProdutos_frame:
                frame.pack_forget()

        self.adicionarProdutos_frame.pack(side=RIGHT)

        def verificarAdicionar():

            if nome_produto.get() == "" or valor_produto.get() == "" or quantidade_produto.get() == "":
                return

            if nome_produto.get() in bd.nomes_produtos:
                ctk.CTkLabel(master=self.adicionarProdutos_frame, text="*produto já cadastrado", width=200, text_color="red").place(x=75, y=310)

                return
            else:
                ctk.CTkLabel(master=self.adicionarProdutos_frame, text="*produto já cadastrado", width=200, text_color="white").place(x=75, y=310)

            try:
                int(valor_produto.get())
                ctk.CTkLabel(master=self.adicionarProdutos_frame, text="*preço inválido", width=200, text_color="white").place(x=75, y=338)
            except:
                ctk.CTkLabel(master=self.adicionarProdutos_frame, text="*preço inválido", width=200, text_color="red").place(x=75, y=338)

                return

            try:
                int(quantidade_produto.get())
                ctk.CTkLabel(master=self.adicionarProdutos_frame, text="*quantidade inválida", width=200, text_color="white").place(x=75, y=366)
            except:
                ctk.CTkLabel(master=self.adicionarProdutos_frame, text="*quantidade inválida", width=200, text_color="red").place(x=75, y=366)

                return

            bd.inserir(nome_produto.get(), int(valor_produto.get()), int(quantidade_produto.get()))

            self.listar_produtos()

        nome_produto = ctk.StringVar(master=self.adicionarProdutos_frame)

        valor_produto = ctk.StringVar(master=self.adicionarProdutos_frame)

        quantidade_produto = ctk.StringVar(master=self.adicionarProdutos_frame)

        if self.count_adicionar == 0:
            ctk.CTkLabel(master=self.adicionarProdutos_frame, text="Nome do produto", width=200, text_color="black").place(x=75, y=76)

            ctk.CTkEntry(master=self.adicionarProdutos_frame, textvariable=nome_produto).place(x=105, y=101)

            ctk.CTkLabel(master=self.adicionarProdutos_frame, text="Preço do produto", width=200, text_color="black").place(x=75, y=141)

            ctk.CTkEntry(master=self.adicionarProdutos_frame, textvariable=valor_produto).place(x=105, y=166)

            ctk.CTkLabel(master=self.adicionarProdutos_frame, text="Quantidade do produto", width=200, text_color="black").place(x=75, y=206)

            ctk.CTkEntry(master=self.adicionarProdutos_frame, textvariable=quantidade_produto).place(x=105, y=231)

            ctk.CTkButton(master=self.adicionarProdutos_frame, text="adicionar", command=verificarAdicionar).place(x=105, y=270)

            self.count_adicionar += 1

    def tela_principal(self):
        if bd.conectar(self.user_input1.get()):
            pass
        else:
            ctk.CTkLabel(master=self.acesso_frame, text="senha incorreta", width=200, text_color="red").place(x=250, y=270)

            return

        self.acesso_frame.pack_forget()
        self.principal_frame.pack(side=LEFT)

        if self.count_principal == 0:
            ctk.CTkButton(master=self.principal_frame, text="Adicionar produto", command=self.adicionar_produto).place(x=105, y=66)

            ctk.CTkButton(master=self.principal_frame, text="Remover produto", command=self.remover_Produto).place(x=105, y=106)

            ctk.CTkButton(master=self.principal_frame, text="Venda realizada", command=self.vendaRealizada).place(x=105, y=146)

            ctk.CTkButton(master=self.principal_frame, text="Estoque recebido", command=self.estoqueRecebido).place(x=105, y=186)

            ctk.CTkButton(master=self.principal_frame, text="Lista de produtos", command=self.listar_produtos).place(x=105, y=226)

            ctk.CTkButton(master=self.principal_frame, text="Buscar produto", command=self.buscar_produto).place(x=105, y=266)

            ctk.CTkButton(master=self.principal_frame, text="Alterar preço", command=self.alterarValor).place(x=105, y=306)

            self.count_principal += 1

gui = Gui()
bd.close()