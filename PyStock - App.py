import os
import sys
import mysql.connector
import datetime


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from View.PY.FrmLogin import Ui_login
from View.PY.FrmAdmin import Ui_FrmAdmin
from View.PY.FrmColaborador import Ui_FrmColaborador

# Configurando Banco
banco = mysql.connector.connect(
    host='localhost',
    port='3307',
    user='root',
    passwd='',
    database='banco_pystock'
)

cursor = banco.cursor()


class FrmLogin(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        self.ui = Ui_login()
        self.ui.setupUi(self)

        # Botão de logar no sistema
        self.ui.pushButton.clicked.connect(lambda: self.logar())

    def logar(self):

        global window
        global UserLogado

        # Pegando os colaboradores cadastrados no banco
        cursor.execute("SELECT * FROM login")
        logins = cursor.fetchall()

        usuario = self.ui.lineEdit.text()
        senha = self.ui.lineEdit_2.text()

        print(f"Usuario inserido: {usuario}\n"
              f"Senha inserida: {senha}")

        # Verificando cada Usuário
        for login in logins:

            if usuario != login[0]:
                self.ui.lineEdit.setStyleSheet('background-color: rgba(0, 0 , 0, 0);border: 2px solid rgba(0,0,0,0);'
                                               'border-bottom-color: rgb(255, 17, 49);color: rgb(0,0,0);padding-bottom: 8px;'
                                               'border-radius: 0px;font: 10pt "Montserrat";')

            if senha != login[1]:
                self.ui.lineEdit_2.setStyleSheet('background-color: rgba(0, 0 , 0, 0);border: 2px solid rgba(0,0,0,0);'
                                                 'border-bottom-color: rgb(255, 17, 49);color: rgb(0,0,0);padding-bottom: 8px;'
                                                 'border-radius: 0px;font: 10pt "Montserrat";')

            # Caso os dados estejam no banco, é iniciado o Frm de acordo com o nivel
            if usuario == login[0] and senha == login[1]:

                UserLogado = login[3]

                self.ui.lineEdit.setStyleSheet('background-color: rgba(0, 0 , 0, 0);border: 2px solid rgba(0,0,0,0);'
                                               'border-bottom-color: rgb(159, 63, 250);color: rgb(0,0,0);padding-bottom: 8px;'
                                               'border-radius: 0px;font: 10pt "Montserrat";')

                self.ui.lineEdit_2.setStyleSheet('background-color: rgba(0, 0 , 0, 0);border: 2px solid rgba(0,0,0,0);'
                                                 'border-bottom-color: rgb(159, 63, 250);color: rgb(0,0,0);padding-bottom: 8px;'
                                                 'border-radius: 0px;font: 10pt "Montserrat";')
                if login[2] == 'admin':
                    print('Seu nivel de Login é: Admin')

                    window.close()
                    window = FrmAdmin()
                    window.show()

                if login[2] == 'colaborador':
                    window.close()
                    window = FrmColaborador()
                    window.show()
                break


class FrmAdmin(QMainWindow):

    def __init__(self):
        global filtro
        global search_fornecedores
        global window

        QMainWindow.__init__(self)

        self.ui = Ui_FrmAdmin()
        self.ui.setupUi(self)

        # Nome do User
        self.ui.lbl_seja_bem_vindo.setText(f'Seja Bem-Vindo(a) - {UserLogado}')
        self.ui.lbl_titulo_vendas.setText(f'Vendedor(a) - {UserLogado}')
        self.ui.lbl_seja_bem_vindo.setFixedWidth(500)

        ## Configurando páginas e os botões do menu

        # Home
        self.ui.btn_home.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_home))

        # Colaboradores
        self.ui.btn_colaboradores.clicked.connect(
            lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_colaboradores))
        self.ui.btn_cadastrar_colaboradores.clicked.connect(
            lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_cadastro_colaboradores))
        self.ui.btn_alterar_colaboradores.clicked.connect(
            lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.alterar_colaboradores))

        self.ui.btn_cadastro.clicked.connect(self.CadastroColaboradores)
        self.ui.btn_finalizar_alterar_colaboradores.clicked.connect(self.AlterarColaboradores)

        self.ui.line_senha_alterar_colaboradores.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.btn_exluir_colaboradores.clicked.connect(self.ExcluirColaboradores)
        self.ui.tabela_alterar_colaboradores.doubleClicked.connect(self.setTextAlterarColaboradores)

        # Botões para ver/esconder senha inserida
        self.ui.btn_ver_senha.clicked.connect(self.VerSenhaCadastroColaboradores)
        self.ui.btn_ver_senha_alterar.clicked.connect(self.VerSenhaAlterarColaboradores)

        # Tabela pg_colaboradores
        self.ui.tabela_colaboradores.setColumnWidth(0, 260)
        self.ui.tabela_colaboradores.setColumnWidth(1, 260)
        self.ui.tabela_colaboradores.setColumnWidth(2, 260)

        # Tabela alterar_colaboradores
        self.ui.tabela_alterar_colaboradores.setColumnWidth(0, 330)
        self.ui.tabela_alterar_colaboradores.setColumnWidth(1, 330)
        self.ui.tabela_alterar_colaboradores.setColumnWidth(2, 330)

        # Monitoramento
        self.ui.btn_monitoramento.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.monitoramento))

        # Tabela Monitoramento
        self.ui.tabela_monitoramento.setColumnWidth(0, 156)
        self.ui.tabela_monitoramento.setColumnWidth(1, 156)
        self.ui.tabela_monitoramento.setColumnWidth(2, 156)
        self.ui.tabela_monitoramento.setColumnWidth(3, 156)
        self.ui.tabela_monitoramento.setColumnWidth(4, 156)

        # Clientes
        self.ui.btn_clientes.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_clientes))
        self.ui.btn_cadastrar_clientes.clicked.connect(
            lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_cadastrar_clientes))
        self.ui.btn_alterar_clientes.clicked.connect(
            lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_alterar_clientes))
        self.ui.btn_finalizar_cadastro_clientes.clicked.connect(self.CadastrarClientes)
        self.ui.btn_exclui_fornecedores.clicked.connect(self.ExcluirClientes)
        self.ui.tabela_alterar_clientes.doubleClicked.connect(self.setTextAlterarClientes)
        self.ui.btn_finalizar_alteracao_fornecedores.clicked.connect(self.AlterarClientes)

        # Tabela Clientes
        self.ui.tabela_clientes.setColumnWidth(0, 192)
        self.ui.tabela_clientes.setColumnWidth(1, 192)
        self.ui.tabela_clientes.setColumnWidth(2, 192)
        self.ui.tabela_clientes.setColumnWidth(3, 194)

        # Tabela Cadastrar Clientes
        self.ui.tabela_cadastrar_clientes.setColumnWidth(0, 247)
        self.ui.tabela_cadastrar_clientes.setColumnWidth(1, 247)
        self.ui.tabela_cadastrar_clientes.setColumnWidth(2, 247)
        self.ui.tabela_cadastrar_clientes.setColumnWidth(3, 249)

        # Tabela Alterar Clientes
        self.ui.tabela_alterar_clientes.setColumnWidth(0, 247)
        self.ui.tabela_alterar_clientes.setColumnWidth(1, 247)
        self.ui.tabela_alterar_clientes.setColumnWidth(2, 247)
        self.ui.tabela_alterar_clientes.setColumnWidth(3, 249)

        # Vendas
        self.ui.btn_Vendas.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_vendas))

        # Tabela Vendas
        self.ui.tabela_vendas.setColumnWidth(0, 50)
        self.ui.tabela_vendas.setColumnWidth(1, 131)
        self.ui.tabela_vendas.setColumnWidth(2, 250)
        self.ui.tabela_vendas.setColumnWidth(3, 131)
        self.ui.tabela_vendas.setColumnWidth(4, 75)
        self.ui.tabela_vendas.setColumnWidth(5, 155)

        # Fornecedores
        self.ui.btn_fornecedores.clicked.connect(
            lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_fornecedores))
        self.ui.btn_adicionar_forncedores.clicked.connect(
            lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_cadastrar_fornecedores))
        self.ui.btn_editar_fornecedores.clicked.connect(
            lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_alterar_fornecedores))
        self.ui.btn_cadastrar_forncedores.clicked.connect(self.CadastrarFornecedores)
        self.ui.tabela_alterar_fornecedores.doubleClicked.connect(self.setTextAlterarFornecedores)
        self.ui.btn_alterar_fornecedores.clicked.connect(self.AlterarFornecedores)
        self.ui.btn_excluir_fornecedores.clicked.connect(self.ExluirFornecedores)

        # Tabela Fornecedores
        self.ui.tabela_fornecedores.setColumnWidth(0, 257)
        self.ui.tabela_fornecedores.setColumnWidth(1, 257)
        self.ui.tabela_fornecedores.setColumnWidth(2, 257)

        # Tabela Cadastrar Fornecedores
        self.ui.tabela_cadastrar_fornecedores.setColumnWidth(0, 330)
        self.ui.tabela_cadastrar_fornecedores.setColumnWidth(1, 330)
        self.ui.tabela_cadastrar_fornecedores.setColumnWidth(2, 330)

        # Tabela Alterar Fornecedores
        self.ui.tabela_alterar_fornecedores.setColumnWidth(0, 330)
        self.ui.tabela_alterar_fornecedores.setColumnWidth(1, 330)
        self.ui.tabela_alterar_fornecedores.setColumnWidth(2, 330)

        # Produtos
        self.ui.btn_produtos.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_produtos))
        self.ui.btn_cadastrar_produto.clicked.connect(
            lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_cadastar_produtos))
        self.ui.btn_alterar_produto.clicked.connect(
            lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_alterar_produtos))
        self.ui.btn_finalizar_cadastro.clicked.connect(self.CadastrarProdutos)
        self.ui.btn_excluir_produto.clicked.connect(self.ExcluirProdutos)
        self.ui.tabela_alterar_produto.doubleClicked.connect(self.setTextAlterarProdutos)
        self.ui.btn_finalizar_alterar.clicked.connect(self.AlterarProdutos)

        # Tabela Produtos
        self.ui.tabela_produto.setColumnWidth(0, 50)
        self.ui.tabela_produto.setColumnWidth(1, 131)
        self.ui.tabela_produto.setColumnWidth(2, 250)
        self.ui.tabela_produto.setColumnWidth(3, 131)
        self.ui.tabela_produto.setColumnWidth(4, 75)
        self.ui.tabela_produto.setColumnWidth(5, 155)

        # Tabela Cadastrar Produtos
        self.ui.tabela_cadastro.setColumnWidth(0, 50)
        self.ui.tabela_cadastro.setColumnWidth(1, 165)
        self.ui.tabela_cadastro.setColumnWidth(2, 300)
        self.ui.tabela_cadastro.setColumnWidth(3, 165)
        self.ui.tabela_cadastro.setColumnWidth(4, 75)
        self.ui.tabela_cadastro.setColumnWidth(5, 250)

        # Tabela Alterar Produtos
        self.ui.tabela_alterar_produto.setColumnWidth(0, 50)
        self.ui.tabela_alterar_produto.setColumnWidth(1, 165)
        self.ui.tabela_alterar_produto.setColumnWidth(2, 300)
        self.ui.tabela_alterar_produto.setColumnWidth(3, 165)
        self.ui.tabela_alterar_produto.setColumnWidth(4, 75)
        self.ui.tabela_alterar_produto.setColumnWidth(5, 250)

        # Configurações
        self.ui.btn_configs.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_configuracoes))

        # Voltar
        self.ui.btn_voltar.clicked.connect(self.Voltar)

        # Atualizando Tabelas
        self.AtualizaTabelasLogin()
        self.AtualizaTabelasClientes()
        self.AtualizaTabelasFornecedores()
        self.AtualizaTabelasProdutos()
        self.AtualizaTabelaVendas()

        # iniciando Hora e Data do Sistema
        tempo = QTimer(self)
        tempo.timeout.connect(self.HoraData)
        tempo.start(1000)

        # Atuliza previsão de texto das barras de pesquisa
        self.AtualizaCompleterSearchFornecedores()
        self.AtualizaCompleterSearchProdutos()
        self.AtualizaCompleterSearchColaboradores()
        self.AtualizaCompleterSearchClientes()

        # Conectando com a função fazer a pesquisa dos dados inseridos

        # Produtos
        self.ui.btn_pesquisar_produto.clicked.connect(lambda: self.SearchProdutos(pg='Produtos'))
        self.ui.line_search_Bar_produtos.returnPressed.connect(lambda: self.SearchProdutos(pg='Produtos'))

        self.ui.line_search_Bar_alterar_produto.returnPressed.connect(lambda: self.SearchProdutos(pg='Alterar'))
        self.ui.btn_pesquisar_alterar_produto.clicked.connect(lambda: self.SearchProdutos(pg='Alterar'))

        self.ui.line_search_Bar_cadastrar_produto.returnPressed.connect(lambda: self.SearchProdutos(pg='Cadastrar'))
        self.ui.btn_pesquisar_cadastrar_produto.clicked.connect(lambda: self.SearchProdutos(pg='Cadastrar'))

        # Fornecedores
        self.ui.btn_filtrar_fornecedores.clicked.connect(lambda: self.SearchFornecedores(pg='Fornecedores'))
        self.ui.line_search_Bar_fornecedores.returnPressed.connect(lambda: self.SearchFornecedores(pg='Fornecedores'))

        self.ui.btn_flitrar_fornecedores.clicked.connect(lambda: self.SearchFornecedores(pg='Alterar'))
        self.ui.line_search_Bar_altarar_fornecedor.returnPressed.connect(lambda: self.SearchFornecedores(pg='Alterar'))

        self.ui.btn_pesquisar_fornecedores.clicked.connect(lambda: self.SearchFornecedores(pg='Cadastrar'))
        self.ui.line_search_Bar_cadastrar_fornecedores.returnPressed.connect(
            lambda: self.SearchFornecedores(pg='Cadastrar'))

        # Colaboradores
        self.ui.btn_pesquisar_colaboradores.clicked.connect(lambda: self.SearchColaboradores(pg='Colaboradores'))
        self.ui.line_search_bar_colaboradores.returnPressed.connect(
            lambda: self.SearchColaboradores(pg='Colaboradores'))

        self.ui.btn_pesquisar_alterar_colaboradores.clicked.connect(lambda: self.SearchColaboradores(pg='Alterar'))
        self.ui.line_search_bar_buscar_colaboradores.returnPressed.connect(
            lambda: self.SearchColaboradores(pg='Alterar'))

        # Clientes
        self.ui.btn_pesquisar_clientes.clicked.connect(lambda: self.SearchClientes(pg='Clientes'))
        self.ui.line_search_Bar_clientes.returnPressed.connect(lambda: self.SearchClientes(pg='Clientes'))

        self.ui.btn_filtrar_clientes.clicked.connect(lambda: self.SearchClientes(pg='Alterar'))
        self.ui.line_search_Bar_alterar_clientes.returnPressed.connect(lambda: self.SearchClientes(pg='Alterar'))

        self.ui.btn_pesquisar_cadastrar_cliente.clicked.connect(lambda: self.SearchClientes(pg='Cadastrar'))
        self.ui.line_search_Bar_cadastrar_clientes.returnPressed.connect(lambda: self.SearchClientes(pg='Cadastrar'))

        # Formatando número de contato dos Fornecedores
        self.ui.line_cadastrar_contato_fornecedores.textChanged.connect(
            lambda: self.FormataNumeroContato(pg='CadastrarFornecedores'))
        self.ui.line_alterar_contato_fornecedor.textChanged.connect(
            lambda: self.FormataNumeroContato(pg='AlterarFornecedores'))

        # Formatando número de contato dos Clientes
        self.ui.line_contato_cadastrar_clientes.textChanged.connect(lambda: self.FormataNumeroContato(pg='CadastrarClientes'))
        self.ui.line_alterar_contato_cliente.textChanged.connect(lambda: self.FormataNumeroContato(pg='AlterarClientes'))

        # Formatando CPF dos Clientes
        self.ui.line_cpf_cadastrar_clientes.textChanged.connect(lambda: self.FormataCPFClientes(pg='Cadastrar'))
        self.ui.line_alterar_cpf_cliente.textChanged.connect(lambda: self.FormataCPFClientes(pg='Alterar'))
        self.ui.line_cliente.textChanged.connect(lambda: self.FormataCPFClientes(pg='Vendas'))

        # Pesquisando produto pelo código
        self.ui.line_codigo_produto.returnPressed.connect(self.PesquisandoProdutoPeloCodigo)
        self.ui.btn_confirmar_codigo.clicked.connect(self.PesquisandoProdutoPeloCodigo)
        self.ui.line_search_bar_vendas.returnPressed.connect(self.CodProdutoVendas)

        # Confirmando cliente informado na pg Vendas
        self.ui.line_cliente.returnPressed.connect(self.ConfirmarCliente)
        self.ui.btn_confirmar_cliente.clicked.connect(self.ConfirmarCliente)

        # Vendas
        self.ui.btn_adicionar_compra.clicked.connect(self.CadastrandoVendas)
        self.ui.btn_excluir_item.clicked.connect(self.ExcluirVenda)

        self.ui.lbl_total_venda.move(670, 20)
        self.ui.lbl_total_valor.move(910, 20)
        self.ui.line_troco.move(680, 80)
        self.ui.btn_confirmar_troco.move(860, 80)
        self.ui.lbl_devolver_troco.move(680, 130)
        self.ui.lbl_troco.move(830, 130)

        self.ui.line_troco.returnPressed.connect(self.Troco)
        self.ui.btn_confirmar_troco.clicked.connect(self.Troco)
        self.AtualizaTotal()

        self.ui.btn_finalizar_compra.clicked.connect(self.FinalizarVendas)
        self.AtualizaTabelaMonitoramentoVendas()
        self.ui.btn_limpar_tabela.clicked.connect(self.LimparTabelaMonitoramento)

    # Pequenas Funções
    def Voltar(self):
        global window

        window.close()
        window = FrmLogin()
        window.show()

    def Popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Erro - Cadastro de Colaboradores")
        msg.setText('Selecione um Nível de Usuário!')

        x = msg.exec_()

    def HoraData(self):
        tempoAtual = QTime.currentTime()
        tempoTexto = tempoAtual.toString('hh:mm:ss')
        data_atual = datetime.date.today()
        dataTexto = data_atual.strftime('%d/%m/%Y')

        # Colaradores
        self.ui.lbl_hora_data_colaboradores.setText(f'{dataTexto} {tempoTexto}')
        self.ui.lbl_hora_data_alterar_colaboradores.setText(f'{dataTexto} {tempoTexto}')

        # Monitoramento de Vendas
        self.ui.lbl_hora_data_monitoramento.setText(f'{dataTexto} {tempoTexto}')

        # Vendas
        self.ui.lbl_hora_data.setText(f'{dataTexto} {tempoTexto}')

        # Produtos
        self.ui.lbl_hora_data_produtos.setText(f'{dataTexto} {tempoTexto}')
        self.ui.lbl_hora_data_alterar_produto.setText(f'{dataTexto} {tempoTexto}')
        self.ui.lbl_hora_data_cadastrar_produto.setText(f'{dataTexto} {tempoTexto}')

        # Fornecedores
        self.ui.lbl_hora_data_fornecedores.setText(f'{dataTexto} {tempoTexto}')
        self.ui.lbl_hora_data_alterar_fornecedores.setText(f'{dataTexto} {tempoTexto}')
        self.ui.lbl_hora_data_cadastrar_fornecedores.setText(f'{dataTexto} {tempoTexto}')

        # Clientes
        self.ui.lbl_hora_data_clientes.setText(f'{dataTexto} {tempoTexto}')
        self.ui.lbl_hora_data_cadastrar_clientes.setText(f'{dataTexto} {tempoTexto}')
        self.ui.lbl_hora_data_alterar_clientes.setText(f'{dataTexto} {tempoTexto}')

    def PesquisandoProdutoPeloCodigo(self):
        produtos = list()

        cod_inserido = self.ui.line_codigo_produto

        cursor.execute('SELECT * FROM produtos')
        banco_produtos = cursor.fetchall()

        produtos.clear()
        tabela = self.ui.tabela_produto

        for produto in banco_produtos:
            produtos.append(produto[0])

        items = tabela.findItems(cod_inserido.text(), Qt.MatchExactly)

        if items:
            item = items[0]
            tabela.setCurrentItem(item)

            cod_inserido.setStyleSheet('''
                        background-color: rgba(0, 0 , 0, 0);
                        border: 2px solid rgba(0,0,0,0);
                        border-bottom-color: rgb(159, 63, 250);
                        color: rgb(0,0,0);
                        padding-bottom: 8px;
                        border-radius: 0px;
                        font: 10pt "Montserrat";''')

        else:
            cod_inserido.setStyleSheet('''
                        background-color: rgba(0, 0 , 0, 0);
                        border: 2px solid rgba(0,0,0,0);
                        border-bottom-color: rgb(255, 17, 49);;
                        color: rgb(0,0,0);
                        padding-bottom: 8px;
                        border-radius: 0px;
                        font: 10pt "Montserrat";''')

    def CodProdutoVendas(self):
        cursor.execute('SELECT * FROM produtos')
        banco_produtos = cursor.fetchall()

        produto_inserido = self.ui.line_search_bar_vendas

        for pos, produto in enumerate(banco_produtos):
            if produto[1] == produto_inserido.text():
                self.ui.line_codigo_vendas.setText(produto[0])
                break

    def ConfirmarCliente(self):
        global search_clientes

        cliente = self.ui.line_cliente

        if cliente.text() in search_clientes:
            cliente.setStyleSheet(
                '''
                background-color: rgba(0, 0 , 0, 0);
                border: 2px solid rgba(0,0,0,0);
                border-bottom-color: rgb(15, 168, 103);
                color: rgb(0,0,0);
                padding-bottom: 8px;
                border-radius: 0px;
                font: 10pt "Montserrat";'''
            )
        else:
            cliente.setStyleSheet('''
                                background-color: rgba(0, 0 , 0, 0);
                                border: 2px solid rgba(0,0,0,0);
                                border-bottom-color: rgb(255, 17, 49);
                                color: rgb(0,0,0);
                                padding-bottom: 8px;
                                border-radius: 0px;
                                font: 10pt "Montserrat";''')

    # Função para formartar o número de contato inserido
    def FormataNumeroContato(self, pg):
        global numero
        if pg == 'CadastrarFornecedores':
            numero = self.ui.line_cadastrar_contato_fornecedores
        if pg == 'AlterarFornecedores':
            numero = self.ui.line_alterar_contato_fornecedor

        if pg == 'CadastrarClientes':
            numero = self.ui.line_contato_cadastrar_clientes
        if pg == 'AlterarClientes':
            numero = self.ui.line_alterar_contato_cliente

        texto = numero.text()
        tamanho = len(numero.text())

        if tamanho == 1 and texto.isnumeric() == True:
            numero.setText(f'({texto}')

        if tamanho == 3 and texto[1:].isnumeric() == True:
            numero.setText(f'{texto}) ')

        if tamanho == 6 and texto[5].isnumeric() == True:
            numero.setText(f'{texto} ')

        if tamanho == 11 and texto[7].isnumeric() == True:
            numero.setText(f'{texto}-')

    # Função para formatar o cpf inserido
    def FormataCPFClientes(self, pg):

        if pg == 'Cadastrar':
            CPF = self.ui.line_cpf_cadastrar_clientes
        if pg == 'Alterar':
            CPF = self.ui.line_alterar_cpf_cliente
        if pg == 'Vendas':
            CPF = self.ui.line_cliente

        TextoInserido = CPF.text()
        TamanhoDoTexto = len(CPF.text())

        if TamanhoDoTexto == 3 and TextoInserido.isnumeric() == True:
            CPF.setText(f'{TextoInserido}.')
        if TamanhoDoTexto == 7 and TextoInserido[4:].isnumeric() == True:
            CPF.setText(f'{TextoInserido}.')
        if TamanhoDoTexto == 11 and TextoInserido[8:].isnumeric() == True:
            CPF.setText(f'{TextoInserido}-')

    # Função para Fazer a pesquisa dos item inserido
    def SearchProdutos(self, pg):
        tabela = self
        produto = self

        if pg == 'Produtos':
            tabela = self.ui.tabela_produto
            produto = self.ui.line_search_Bar_produtos

        if pg == 'Alterar':
            tabela = self.ui.tabela_alterar_produto
            produto = self.ui.line_search_Bar_alterar_produto

        if pg == 'Cadastrar':
            tabela = self.ui.tabela_cadastro
            produto = self.ui.line_search_Bar_cadastrar_produto

        items = tabela.findItems(produto.text(), Qt.MatchContains)

        if items:
            item = items[0]
            tabela.setCurrentItem(item)

    def SearchFornecedores(self, pg):
        tabela = self
        produto = self

        if pg == 'Fornecedores':
            tabela = self.ui.tabela_fornecedores
            produto = self.ui.line_search_Bar_fornecedores

        if pg == 'Alterar':
            tabela = self.ui.tabela_alterar_fornecedores
            produto = self.ui.line_search_Bar_altarar_fornecedor

        if pg == 'Cadastrar':
            tabela = self.ui.tabela_cadastrar_fornecedores
            produto = self.ui.line_search_Bar_cadastrar_fornecedores

        items = tabela.findItems(produto.text(), Qt.MatchContains)

        if items:
            item = items[0]
            tabela.setCurrentItem(item)

    def SearchColaboradores(self, pg):
        tabela = self
        produto = self

        if pg == 'Colaboradores':
            tabela = self.ui.tabela_colaboradores
            produto = self.ui.line_search_bar_colaboradores

        if pg == 'Alterar':
            tabela = self.ui.tabela_alterar_colaboradores
            produto = self.ui.line_search_bar_buscar_colaboradores

        items = tabela.findItems(produto.text(), Qt.MatchContains)

        if items:
            item = items[0]

            tabela.setCurrentItem(item)

    def SearchClientes(self, pg):
        tabela = self
        produto = self

        if pg == 'Clientes':
            tabela = self.ui.tabela_clientes
            produto = self.ui.line_search_Bar_clientes

        if pg == 'Alterar':
            tabela = self.ui.tabela_alterar_clientes
            produto = self.ui.line_search_Bar_alterar_clientes

        if pg == 'Cadastrar':
            tabela = self.ui.tabela_cadastrar_clientes
            produto = self.ui.line_search_Bar_cadastrar_clientes

        items = tabela.findItems(produto.text(), Qt.MatchContains)

        if items:
            item = items[0]
            tabela.setCurrentItem(item)

    # Funções para Atualiazar as previções das barras de pesquisa
    def AtualizaCompleterSearchFornecedores(self):
        global search_fornecedores

        cursor.execute('SELECT * FROM fornecedores')
        banco_fornecedores = cursor.fetchall()

        search_fornecedores.clear()

        search_fornecedores = []

        for fornecedor in banco_fornecedores:
            search_fornecedores.append(fornecedor[0])

        self.completer = QCompleter(search_fornecedores)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.line_search_Bar_fornecedores.setCompleter(self.completer)
        self.ui.line_search_Bar_altarar_fornecedor.setCompleter(self.completer)
        self.ui.line_search_Bar_cadastrar_fornecedores.setCompleter(self.completer)
        self.ui.line_fornecedor_cadastrar.setCompleter(self.completer)
        self.ui.line_fornecedor_alterar_produto.setCompleter(self.completer)

    def AtualizaCompleterSearchProdutos(self):
        global search_produtos

        cursor.execute('SELECT * FROM produtos')
        banco_produtos = cursor.fetchall()

        search_produtos.clear()

        for produto in banco_produtos:
            search_produtos.append(produto[1])

        self.completer = QCompleter(search_produtos)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)

        self.ui.line_search_Bar_produtos.setCompleter(self.completer)
        self.ui.line_search_Bar_alterar_produto.setCompleter(self.completer)
        self.ui.line_search_Bar_cadastrar_produto.setCompleter(self.completer)
        self.ui.line_search_bar_vendas.setCompleter(self.completer)

    def AtualizaCompleterSearchColaboradores(self):
        global search_colaboradores

        cursor.execute('SELECT * FROM login')
        banco_colaboradores = cursor.fetchall()

        search_colaboradores.clear()

        for colaborador in banco_colaboradores:
            search_colaboradores.append(colaborador[0])

        self.completer = QCompleter(search_colaboradores)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)

        self.ui.line_search_bar_buscar_colaboradores.setCompleter(self.completer)
        self.ui.line_search_bar_colaboradores.setCompleter(self.completer)

    def AtualizaCompleterSearchClientes(self):
        global search_clientes

        cursor.execute('SELECT * FROM clientes')
        banco_clientes = cursor.fetchall()

        search_clientes.clear()

        for clientes in banco_clientes:
            search_clientes.append(clientes[0])
            search_clientes.append(clientes[1])

        self.completer = QCompleter(search_clientes)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)

        self.ui.line_search_Bar_clientes.setCompleter(self.completer)
        self.ui.line_search_Bar_alterar_clientes.setCompleter(self.completer)
        self.ui.line_search_Bar_cadastrar_clientes.setCompleter(self.completer)
        self.ui.line_cliente.setCompleter(self.completer)


    # Funções de Cadastro
    def CadastroColaboradores(self):

        login = self.ui.line_login
        senha = self.ui.line_senha
        nome = self.ui.line_nome
        nivel = ''

        radio_admin = self.ui.radio_admin
        radio_colaborador = self.ui.radio_colaborador

        if radio_colaborador.isChecked() == False and radio_admin.isChecked() == False:
            self.Popup()
        else:
            if login.text() != '' and senha.text() != '' and nome.text() != '':
                if radio_admin.isChecked() == True:
                    nivel = 'admin'

                if radio_colaborador.isChecked() == True:
                    nivel = 'colaborador'

                cursor.execute('SELECT * FROM login')
                banco_login = cursor.fetchall()

                LoginNoBanco = False

                for loginBanco in banco_login:

                    if loginBanco[0] == login.text():
                        LoginNoBanco = True
                        break

                if LoginNoBanco == False:
                    comando_SQL = 'INSERT INTO login VALUES (%s,%s,%s,%s)'
                    dados = f'{login.text()}', f'{senha.text()}', f'{nivel}', f'{nome.text()}'
                    cursor.execute(comando_SQL, dados)
                    banco.commit()

                    login.clear()
                    senha.clear()
                    nome.clear()

                    self.ui.line_login.setStyleSheet('''
                            background-color: rgba(0, 0 , 0, 0);
                            border: 2px solid rgba(0,0,0,0);
                            border-bottom-color: rgb(159, 63, 250);
                            color: rgb(0,0,0);
                            padding-bottom: 8px;
                            border-radius: 0px;
                            font: 10pt "Montserrat";''')


                elif LoginNoBanco == True:
                    self.ui.line_login.setStyleSheet('''
                            background-color: rgba(0, 0 , 0, 0);
                            border: 2px solid rgba(0,0,0,0);
                            border-bottom-color: rgb(255, 17, 49);;
                            color: rgb(0,0,0);
                            padding-bottom: 8px;
                            border-radius: 0px;
                            font: 10pt "Montserrat";''')

            self.AtualizaTabelasLogin()
            self.AtualizaCompleterSearchColaboradores()

    def CadastrarClientes(self):

        cpf = self.ui.line_cpf_cadastrar_clientes
        nome = self.ui.line_nome_cadastrar_clientes
        endereco = self.ui.line_endereco_cadastrar_clientes
        contato = self.ui.line_contato_cadastrar_clientes

        if cpf.text() != '' and nome.text() != '' and endereco.text() != '' and contato.text() != '':
            comando_SQL = 'INSERT INTO clientes (CPF, Nome, Endereço, Contato) VALUES (%s,%s,%s,%s)'
            dados = f'{cpf.text()}', f'{nome.text()}', f'{endereco.text()}', f'{contato.text()}'
            cursor.execute(comando_SQL, dados)

            self.AtualizaTabelasClientes()
            self.AtualizaCompleterSearchClientes()

            cpf.clear()
            nome.clear()
            endereco.clear()
            contato.clear()

    def CadastrarFornecedores(self):

        nome = self.ui.line_cadastrar_nome_fornecedores
        endereco = self.ui.line_cadastrar_endereco_fornecedores
        contato = self.ui.line_cadastrar_contato_fornecedores

        cursor.execute('SELECT * FROM fornecedores')
        banco_fornecedores = cursor.fetchall()

        FornecedorNoBanco = False

        for fornecedor in banco_fornecedores:
            if fornecedor[0] == nome.text():
                FornecedorNoBanco = True

        if nome.text() != '' and endereco != '' and contato != '':
            if FornecedorNoBanco == False:
                comando_SQL = 'INSERT INTO fornecedores VALUES (%s,%s,%s)'
                dados = f'{nome.text()}', f'{endereco.text()}', f'{contato.text()}'
                cursor.execute(comando_SQL, dados)

                nome.clear()
                endereco.clear()
                contato.clear()

                nome.setStyleSheet('''
                                background-color: rgba(0, 0 , 0, 0);
                                border: 2px solid rgba(0,0,0,0);
                                border-bottom-color: rgb(159, 63, 250);
                                color: rgb(0,0,0);
                                padding-bottom: 8px;
                                border-radius: 0px;
                                font: 10pt "Montserrat";''')

                self.AtualizaTabelasFornecedores()
                self.AtualizaCompleterSearchFornecedores()

            else:
                nome.setStyleSheet(
                    '''
                        background-color: rgba(0, 0 , 0, 0);
                        border: 2px solid rgba(0,0,0,0);
                        border-bottom-color: rgb(255, 17, 49);;
                        color: rgb(0,0,0);
                        padding-bottom: 8px;
                        border-radius: 0px;
                        font: 10pt "Montserrat";'''
                )

    def CadastrarProdutos(self):

        global search_fornecedores

        cod_produto = self.ui.line_codigo_produto_cadastrar
        descricao = self.ui.line_descricao_cadastrar
        valor_unitario = self.ui.line_valor_cadastrar
        qtde_estoque = self.ui.line_qtde_cadastrar
        fornecedor = self.ui.line_fornecedor_cadastrar

        cursor.execute("SELECT * FROM produtos")
        banco_produtos = cursor.fetchall()

        ProdutoJaCadastrado = False
        FornecedorNoSearch = False

        if cod_produto.text() != '' and descricao.text() != '' and valor_unitario.text() != '' and qtde_estoque.text() != '' and fornecedor.text() != '':
            for produto in banco_produtos:
                if produto[0] == cod_produto.text():
                    cod_produto.setStyleSheet('''
                            background-color: rgba(0, 0 , 0, 0);
                            border: 2px solid rgba(0,0,0,0);
                            border-bottom-color: rgb(255, 17, 49);;
                            color: rgb(0,0,0);
                            padding-bottom: 8px;
                            border-radius: 0px;
                            font: 10pt "Montserrat";''')

                    ProdutoJaCadastrado = True

                else:
                    cod_produto.setStyleSheet('''
                                            background-color: rgba(0, 0 , 0, 0);
                                            border: 2px solid rgba(0,0,0,0);
                                            border-bottom-color: rgb(159, 63, 250);
                                            color: rgb(0,0,0);
                                            padding-bottom: 8px;
                                            border-radius: 0px;
                                            font: 10pt "Montserrat";''')

            if fornecedor.text() in search_fornecedores:
                FornecedorNoSearch = True

                fornecedor.setStyleSheet('''
                                            background-color: rgba(0, 0 , 0, 0);
                                            border: 2px solid rgba(0,0,0,0);
                                            border-bottom-color: rgb(159, 63, 250);
                                            color: rgb(0,0,0);
                                            padding-bottom: 8px;
                                            border-radius: 0px;
                                            font: 10pt "Montserrat";''')

            else:
                fornecedor.setStyleSheet('''
                            background-color: rgba(0, 0 , 0, 0);
                            border: 2px solid rgba(0,0,0,0);
                            border-bottom-color: rgb(255, 17, 49);;
                            color: rgb(0,0,0);
                            padding-bottom: 8px;
                            border-radius: 0px;
                            font: 10pt "Montserrat";''')

            if ProdutoJaCadastrado == False and FornecedorNoSearch == True:
                comando_SQL = 'INSERT INTO produtos VALUES (%s,%s,%s,%s,%s)'
                dados = f'{cod_produto.text()}', f'{descricao.text()}', f'{valor_unitario.text()}', f'{qtde_estoque.text()}', f'{fornecedor.text()}'
                cursor.execute(comando_SQL, dados)

                cod_produto.clear()
                descricao.clear()
                valor_unitario.clear()
                qtde_estoque.clear()
                fornecedor.clear()

                self.AtualizaTabelasProdutos()
                self.AtualizaCompleterSearchProdutos()

    def CadastrandoVendas(self):

        global search_produtos, StyleError, StyleNormal

        cursor.execute("SELECT * FROM produtos")
        banco_produtos = cursor.fetchall()

        produtoInserido = self.ui.line_codigo_vendas
        qtde = self.ui.line_quantidade_vendas
        desconto = self.ui.line_desconto_vendas
        NomeProduto = ''

        ProdutoNoBanco = False
        QuantidadeMenorQueEstoque = False
        DescontoOk = False
        ValorUnitario = 0

        for pos, produto in enumerate(banco_produtos):

            if produtoInserido.text() == produto[0]:
                ProdutoNoBanco = True
                produtoInserido.setStyleSheet(StyleNormal)
                if qtde.text().isnumeric() == True:
                    if int(produto[3]) >= int(qtde.text()) and int(qtde.text()) > 0:
                        QuantidadeMenorQueEstoque = True
                        qtde.setStyleSheet(StyleNormal)

                        ValorUnitario = produto[2]
                        NomeProduto = produto[1]
                        TotalQtde = int(produto[3]) - int(qtde.text())
                        cursor.execute(f"UPDATE produtos SET qtde_estoque = '{TotalQtde}' WHERE cód_produto = '{produto[0]}'")

                    else:
                        qtde.setStyleSheet(StyleError)
                else:
                    qtde.setStyleSheet(StyleError)

                break
            else:
                produtoInserido.setStyleSheet(StyleError)

        if desconto.text().isnumeric():
            DescontoOk = True

        if ProdutoNoBanco == True and QuantidadeMenorQueEstoque == True and DescontoOk == True:
            cursor.execute('SELECT MAX(id) FROM vendas')
            ultimo_id = cursor.fetchone()

            for id_antigo in ultimo_id:
                if id_antigo == None:
                    id = 0
                else:
                    id = int(id_antigo) + 1

            valor = f'0.{desconto.text()}'
            valorTotal = int(ValorUnitario) * int(qtde.text())
            descontoTotal = int(valorTotal) * float(valor)
            comando_SQL = 'INSERT INTO vendas VALUES (%s,%s,%s,%s,%s,%s)'
            dados = f'{produtoInserido.text()}', f'{NomeProduto}', f'{ValorUnitario}', f'{qtde.text()}', f'{int(valorTotal) - int(descontoTotal)}', f'{id}'
            cursor.execute(comando_SQL, dados)

            self.AtualizaTotal()
            self.AtualizaTabelasProdutos()
            self.AtualizaTabelaVendas()

    def FinalizarVendas(self):
        cursor.execute('SELECT * FROM vendas')
        banco_vendas = cursor.fetchall()

        if len(banco_vendas) > 0:
            tempoAtual = QTime.currentTime()
            tempoTexto = tempoAtual.toString('hh:mm:ss')
            data_atual = datetime.date.today()
            dataTexto = data_atual.strftime('%d/%m/%Y')

            qtde_vendido = list()
            totalVenda = list()
            vendedor = UserLogado
            clienteInserido = self.ui.line_cliente
            cliente = ''
            data_hora = f'{tempoTexto} / {dataTexto}'

            if clienteInserido.text() in search_clientes:
                cliente = clienteInserido.text()
            else:
                cliente = 'Não Informado'

            for venda in banco_vendas:
                qtde_vendido.append(int(venda[3]))
                totalVenda.append(int(venda[4]))

            comando_SQL = 'INSERT INTO monitoramento_vendas VALUES (%s,%s,%s,%s,%s)'
            dados = f'{vendedor}', f'{cliente}', f'{sum(qtde_vendido)}', f'{sum(totalVenda)}', f'{data_hora}'
            cursor.execute(comando_SQL, dados)

        cursor.execute('DELETE FROM vendas')
        self.AtualizaTabelaVendas()
        self.AtualizaTotal()
        self.AtualizaTabelaMonitoramentoVendas()

        self.ui.line_codigo_vendas.clear()
        self.ui.line_cliente.clear()
        self.ui.line_quantidade_vendas.clear()
        self.ui.line_desconto_vendas.clear()
        self.ui.lbl_troco.setText('0,00')

    def LimparTabelaMonitoramento(self):
        cursor.execute('DELETE FROM monitoramento_vendas')
        self.AtualizaTabelaMonitoramentoVendas()

    def AtualizaTabelaMonitoramentoVendas(self):
        cursor.execute('SELECT * FROM monitoramento_vendas')
        banco_monitoramento = cursor.fetchall()

        self.ui.tabela_monitoramento.clear()

        row = 0

        self.ui.tabela_monitoramento.setRowCount(len(banco_monitoramento))

        colunas = ['Vendedor', 'Cliente', 'Qtde Vendido', 'Total Venda', 'Data/horário']
        self.ui.tabela_monitoramento.setHorizontalHeaderLabels(colunas)

        for venda in banco_monitoramento:
            total_venda = lang.toString(int(venda[3]) * 0.01, 'f', 2)

            self.ui.tabela_monitoramento.setItem(row, 0, QTableWidgetItem(venda[0]))
            self.ui.tabela_monitoramento.setItem(row, 1, QTableWidgetItem(venda[1]))
            self.ui.tabela_monitoramento.setItem(row, 2, QTableWidgetItem(venda[2]))
            self.ui.tabela_monitoramento.setItem(row, 3, QTableWidgetItem('R$ ' + total_venda))
            self.ui.tabela_monitoramento.setItem(row, 4, QTableWidgetItem(venda[4]))
            row += 1

    def AtualizaTabelaVendas(self):
        cursor.execute('SELECT * FROM vendas ORDER BY id ASC')
        banco_vendas = cursor.fetchall()

        row = 0

        self.ui.tabela_vendas.setRowCount(len(banco_vendas))
        self.ui.tabela_vendas.clear()

        colunas = ['Item', 'Cód', 'Produto', 'Valor Unitário', 'Qtde', 'Total']
        self.ui.tabela_vendas.setHorizontalHeaderLabels(colunas)

        for venda in banco_vendas:

            valor_unitario = lang.toString(int(venda[2]) * 0.01, 'f', 2)
            total = lang.toString(int(venda[4]) * 0.01, 'f', 2)

            self.ui.tabela_vendas.setItem(row, 0, QTableWidgetItem(f'{venda[5]}'))
            self.ui.tabela_vendas.setItem(row, 1, QTableWidgetItem(venda[0]))
            self.ui.tabela_vendas.setItem(row, 2, QTableWidgetItem(venda[1]))
            self.ui.tabela_vendas.setItem(row, 3, QTableWidgetItem('R$ ' + valor_unitario))
            self.ui.tabela_vendas.setItem(row, 4, QTableWidgetItem(venda[3]))
            self.ui.tabela_vendas.setItem(row, 5, QTableWidgetItem('R$ ' + total))

            row += 1

    def AtualizaTotal(self):

        cursor.execute('SELECT * FROM vendas')
        banco_vendas = cursor.fetchall()

        vendas = list()

        for pos, venda in enumerate(banco_vendas):
            vendas.append(int(venda[4]))

        total = lang.toString(sum(vendas) * 0.01, 'f', 2)
        self.ui.lbl_total_valor.setText(f'{total}')
        self.Troco()

    def ExcluirVenda(self):
        id = self.ui.tabela_vendas.currentRow()
        print(id)
        if id != - 1:
            cursor.execute('SELECT * FROM vendas ORDER BY id ASC')
            banco_vendas = cursor.fetchall()
            cursor.execute('SELECT * FROM produtos')
            banco_produtos = cursor.fetchall()

            id_deletado = 0

            for venda in banco_vendas:
                if venda[5] == id:
                    id_deletado = venda[5]

                    for produto in banco_produtos:
                        if venda[0] == produto[0]:
                            TotalEstoque = int(venda[3]) + int(produto[3])
                            cursor.execute(f'UPDATE produtos SET qtde_estoque = "{TotalEstoque}" WHERE cód_produto = "{produto[0]}"')
                            break

                    cursor.execute(f'DELETE FROM vendas WHERE id = {id}')
                    banco.commit()
                    break

            cursor.execute('SELECT * FROM vendas ORDER BY id ASC')
            banco_vendas = cursor.fetchall()

            for venda in banco_vendas:
                if venda[5] > id_deletado:
                    cursor.execute(f'UPDATE vendas set id = {venda[5] - 1} WHERE id = "{venda[5]}"')
                    banco.commit()

        self.AtualizaTabelaVendas()
        self.AtualizaTotal()
        self.AtualizaTabelasProdutos()

    def Troco(self):
        cursor.execute('SELECT * FROM vendas')
        banco_vendas = cursor.fetchall()

        troco_desejado = self.ui.line_troco.text()
        if troco_desejado.isnumeric() == True:
            vendas = list()
            vendas.clear()

            for venda in banco_vendas:
                vendas.append(int(venda[4]))

            troco = int(troco_desejado) - sum(vendas)
            self.ui.lbl_troco.setText(f'{lang.toString(int(troco) * 0.01, "f", 2)}')

    # Funções de Alterar
    def AlterarColaboradores(self):
        global id_tabela_alterar

        login = self.ui.line_login_alterar_colaboradores
        senha = self.ui.line_senha_alterar_colaboradores
        nome = self.ui.line_nome_alterar_colaboradores

        cursor.execute('SELECT * FROM login')
        banco_login = cursor.fetchall()

        if login.text() != '' and senha.text() != '' and nome.text() != '':

            LoginNoBanco = False

            for pos, user in enumerate(banco_login):
                if login.text() == user[0] and pos != id_tabela_alterar:
                    LoginNoBanco = True

            for pos, user in enumerate(banco_login):
                if pos == id_tabela_alterar:
                    if LoginNoBanco == False:
                        cursor.execute(
                            f'UPDATE login set usuario = "{login.text()}", senha = "{senha.text()}", nivel = "{user[2]}", nome = "{nome.text()}"'
                            f'WHERE usuario = "{user[0]}"')
                        banco.commit()

                        login.clear()
                        senha.clear()
                        nome.clear()

                        self.AtualizaTabelasLogin()
                        self.AtualizaCompleterSearchColaboradores()

                        self.ui.line_login_alterar_colaboradores.setStyleSheet('''
                                   background-color: rgba(0, 0 , 0, 0);
                                   border: 2px solid rgba(0,0,0,0);
                                   border-bottom-color: rgb(159, 63, 250);
                                   color: rgb(0,0,0);
                                   padding-bottom: 8px;
                                   border-radius: 0px;
                                   font: 10pt "Montserrat";''')
                        break
                    else:
                        self.ui.line_login_alterar_colaboradores.setStyleSheet('''
                                   background-color: rgba(0, 0 , 0, 0);
                                   border: 2px solid rgba(0,0,0,0);
                                   border-bottom-color: rgb(255, 17, 49);;
                                   color: rgb(0,0,0);
                                   padding-bottom: 8px;
                                   border-radius: 0px;
                                   font: 10pt "Montserrat";''')

    def AlterarClientes(self):
        global id_alterar_Clientes

        cpf = self.ui.line_alterar_cpf_cliente
        nome = self.ui.line_alterar_nome_cliente
        endereco = self.ui.line_alterar_endereco_cliente
        contato = self.ui.line_alterar_contato_cliente

        cursor.execute('SELECT * FROM clientes')
        banco_clientes = cursor.fetchall()
        if cpf.text() != '' and nome.text() != '' and endereco.text() != '' and contato.text() != '':
            for pos, cliente in enumerate(banco_clientes):
                if pos == id_alterar_Clientes:
                    cursor.execute(
                        f'UPDATE clientes set CPF = "{cpf.text()}", nome = "{nome.text()}", endereço = "{endereco.text()}", contato = "{contato.text()}"'
                        f'WHERE CPF = "{cliente[0]}"')

                    cpf.clear()
                    nome.clear()
                    endereco.clear()
                    contato.clear()

                    self.AtualizaTabelasClientes()
                    self.AtualizaCompleterSearchClientes()

                    break

    def AlterarFornecedores(self):
        global id_alterar_fornecedores

        cursor.execute('SELECT * FROM fornecedores')
        banco_fornecedores = cursor.fetchall()

        nome = self.ui.line_alterar_nome_fornecedor
        endereco = self.ui.line_alterar_endereco_fornecedor
        contato = self.ui.line_alterar_contato_fornecedor

        if nome.text() != '' and endereco.text() != '' and contato.text() != '':
            for pos, fornecedores in enumerate(banco_fornecedores):
                if pos == id_alterar_fornecedores:
                    cursor.execute(
                        f'UPDATE fornecedores set nome = "{nome.text()}", endereço = "{endereco.text()}", contato = "{contato.text()}"'
                        f'WHERE nome = "{fornecedores[0]}"')

                    nome.clear()
                    endereco.clear()
                    contato.clear()

                    self.AtualizaTabelasFornecedores()
                    self.AtualizaCompleterSearchFornecedores()
                    break

    def AlterarProdutos(self):
        global id_alterar_produtos
        global search_fornecedores

        cursor.execute('SELECT * FROM produtos')
        banco_produtos = cursor.fetchall()

        cod_produto = self.ui.line_codigo_alterar_produto
        descricao = self.ui.line_decricao_alterar_produto
        valor_unitario = self.ui.line_valor_alterar_produto
        qtde_estoque = self.ui.line_qtde_alterar_produto
        fornecedor = self.ui.line_fornecedor_alterar_produto

        FornecedorNoSearch = False
        ProdutoJaCadastrado = False
        AlterarProduto = ''

        if cod_produto.text() != '' and descricao.text() != '' and valor_unitario.text() != '' and qtde_estoque != '' and fornecedor != '':
            if fornecedor.text() in search_fornecedores:
                FornecedorNoSearch = True

                fornecedor.setStyleSheet('''
                                           background-color: rgba(0, 0 , 0, 0);
                                           border: 2px solid rgba(0,0,0,0);
                                           border-bottom-color: rgb(159, 63, 250);
                                           color: rgb(0,0,0);
                                           padding-bottom: 8px;
                                           border-radius: 0px;
                                           font: 10pt "Montserrat";''')

            else:
                fornecedor.setStyleSheet('''
                                                   background-color: rgba(0, 0 , 0, 0);
                                                   border: 2px solid rgba(0,0,0,0);
                                                   border-bottom-color: rgb(255, 17, 49);;
                                                   color: rgb(0,0,0);
                                                   padding-bottom: 8px;
                                                   border-radius: 0px;
                                                   font: 10pt "Montserrat";''')

            for pos, produto in enumerate(banco_produtos):
                if cod_produto.text() == produto[0] and pos != id_alterar_produtos:
                    ProdutoJaCadastrado = True

                    cod_produto.setStyleSheet('''
                            background-color: rgba(0, 0 , 0, 0);
                            border: 2px solid rgba(0,0,0,0);
                            border-bottom-color: rgb(255, 17, 49);;
                            color: rgb(0,0,0);
                            padding-bottom: 8px;
                            border-radius: 0px;
                            font: 10pt "Montserrat";''')

                else:
                    cod_produto.setStyleSheet('''
                                   background-color: rgba(0, 0 , 0, 0);
                                   border: 2px solid rgba(0,0,0,0);
                                   border-bottom-color: rgb(159, 63, 250);
                                   color: rgb(0,0,0);
                                   padding-bottom: 8px;
                                   border-radius: 0px;
                                   font: 10pt "Montserrat";''')

                if pos == id_alterar_produtos:
                    AlterarProduto = produto[0]

        if FornecedorNoSearch == True and ProdutoJaCadastrado == False:
            cursor.execute(
                f'UPDATE produtos set cód_produto = "{cod_produto.text()}", descrição = "{descricao.text()}", valor_unitário = "{valor_unitario.text()}", qtde_estoque = "{qtde_estoque.text()}", fornecedor = "{fornecedor.text()}"'
                f'WHERE cód_produto = "{AlterarProduto}"')

            cod_produto.clear()
            descricao.clear()
            valor_unitario.clear()
            qtde_estoque.clear()
            fornecedor.clear()

            self.AtualizaTabelasProdutos()
            self.AtualizaCompleterSearchProdutos()
            self.AtualizaTabelaVendas()

    # Funções de Excluir
    def ExcluirColaboradores(self):

        id = self.ui.tabela_colaboradores.currentRow()

        cursor.execute('SELECT * FROM login')
        banco_login = cursor.fetchall()

        deletar_user = ''

        for pos, user in enumerate(banco_login):
            if id == pos:
                deletar_user = user[0]

        print(deletar_user)

        cursor.execute(f'DELETE FROM login WHERE usuario = "{deletar_user}"')
        banco.commit()

        self.AtualizaTabelasLogin()
        self.AtualizaCompleterSearchColaboradores()

    def ExcluirClientes(self):
        id = self.ui.tabela_clientes.currentRow()

        cursor.execute('SELECT * FROM clientes')
        banco_clientes = cursor.fetchall()

        deletar_cliente = ''

        for pos, cliente in enumerate(banco_clientes):
            if id == pos:
                deletar_cliente = cliente[0]

        cursor.execute(f'DELETE FROM clientes WHERE CPF = "{deletar_cliente}"')
        banco.commit()

        self.AtualizaTabelasClientes()
        self.AtualizaCompleterSearchClientes()

    def ExluirFornecedores(self):
        id = self.ui.tabela_fornecedores.currentRow()

        cursor.execute('SELECT * FROM fornecedores')
        banco_fornecedor = cursor.fetchall()

        deletar_fornecedor = ''

        for pos, fornecedor in enumerate(banco_fornecedor):
            if id == pos:
                deletar_fornecedor = fornecedor[0]

        cursor.execute(f'DELETE FROM fornecedores WHERE Nome = "{deletar_fornecedor}"')
        banco.commit()

        self.AtualizaTabelasFornecedores()
        self.AtualizaCompleterSearchFornecedores()

    def ExcluirProdutos(self):

        id = self.ui.tabela_produto.currentRow()

        cursor.execute('SELECT * FROM produtos')
        banco_produtos = cursor.fetchall()

        for pos, produto in enumerate(banco_produtos):
            if pos == id:
                cursor.execute(f'DELETE FROM produtos WHERE cód_produto = "{produto[0]}"')
                banco.commit()

                self.AtualizaTabelasProdutos()
                self.AtualizaCompleterSearchProdutos()

    # Funções de setar Texto
    def setTextAlterarColaboradores(self):
        global id_tabela_alterar
        nome = self.ui.line_nome_alterar_colaboradores
        login = self.ui.line_login_alterar_colaboradores
        senha = self.ui.line_senha_alterar_colaboradores

        id_tabela_alterar = self.ui.tabela_alterar_colaboradores.currentRow()

        cursor.execute('SELECT * FROM login')
        banco_login = cursor.fetchall()

        for pos, user in enumerate(banco_login):
            if pos == id_tabela_alterar:
                nome.setText(user[3])
                login.setText(user[0])
                senha.setText(user[1])

    def setTextAlterarClientes(self):
        global id_alterar_Clientes
        cpf = self.ui.line_alterar_cpf_cliente
        nome = self.ui.line_alterar_nome_cliente
        endereco = self.ui.line_alterar_endereco_cliente
        contato = self.ui.line_alterar_contato_cliente

        id_alterar_Clientes = self.ui.tabela_alterar_clientes.currentRow()

        cursor.execute('SELECT * FROM clientes')
        banco_clientes = cursor.fetchall()

        for pos, cliente in enumerate(banco_clientes):
            if pos == id_alterar_Clientes:
                cpf.setText(cliente[0])
                nome.setText(cliente[1])
                endereco.setText(cliente[2])
                contato.setText(cliente[3])

    def setTextAlterarFornecedores(self):
        global id_alterar_fornecedores

        nome = self.ui.line_alterar_nome_fornecedor
        endereco = self.ui.line_alterar_endereco_fornecedor
        contato = self.ui.line_alterar_contato_fornecedor

        id_alterar_fornecedores = self.ui.tabela_alterar_fornecedores.currentRow()

        cursor.execute('SELECT * FROM fornecedores')
        banco_fornecedores = cursor.fetchall()

        for pos, fornecedor in enumerate(banco_fornecedores):
            if pos == id_alterar_fornecedores:
                nome.setText(fornecedor[0])
                endereco.setText(fornecedor[1])
                contato.setText(fornecedor[2])

    def setTextAlterarProdutos(self):
        global id_alterar_produtos

        cod_produto = self.ui.line_codigo_alterar_produto
        descricao = self.ui.line_decricao_alterar_produto
        valor_unitario = self.ui.line_valor_alterar_produto
        qtde_estoque = self.ui.line_qtde_alterar_produto
        fornecedor = self.ui.line_fornecedor_alterar_produto

        id_alterar_produtos = self.ui.tabela_alterar_produto.currentRow()

        cursor.execute('SELECT * FROM produtos')
        banco_produtos = cursor.fetchall()

        for pos, produto in enumerate(banco_produtos):
            if pos == id_alterar_produtos:
                cod_produto.setText(produto[0])
                descricao.setText(produto[1])
                valor_unitario.setText(produto[2])
                qtde_estoque.setText(produto[3])
                fornecedor.setText(produto[4])

    # Funções para ver Senha
    def VerSenhaCadastroColaboradores(self):
        global click_cadastro_colaboradores

        click_cadastro_colaboradores += 1

        if click_cadastro_colaboradores % 2 == 0:
            self.ui.line_senha.setEchoMode(QLineEdit.EchoMode.Password)
            self.ui.btn_ver_senha.setStyleSheet('QPushButton {'
                                                'background-image: url(:/icones/ver senha.png);'
                                                'border: 0px;'
                                                'outline: 0;'
                                                '}'
                                                ''
                                                'QPushButton:hover {'
                                                'background-image: url(:/icones/ver senha hover.png);'
                                                '}')

        if click_cadastro_colaboradores % 2 == 1:
            self.ui.line_senha.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.btn_ver_senha.setStyleSheet('QPushButton {'
                                                'background-image: url(:/icones/bloquear senha.png);'
                                                'border: 0px;'
                                                'outline: 0;'
                                                '}'
                                                ''
                                                'QPushButton:hover {'
                                                'background-image: url(:/icones/bloquear senha hover.png);''}')

    def VerSenhaAlterarColaboradores(self):
        global click_alterar_colaboradores

        click_alterar_colaboradores += 1

        if click_alterar_colaboradores % 2 == 0:
            self.ui.line_senha_alterar_colaboradores.setEchoMode(QLineEdit.EchoMode.Password)
            self.ui.btn_ver_senha_alterar.setStyleSheet('QPushButton {'
                                                        'background-image: url(:/icones/ver senha.png);'
                                                        'border: 0px;'
                                                        'outline: 0;'
                                                        '}'
                                                        ''
                                                        'QPushButton:hover {'
                                                        'background-image: url(:/icones/ver senha hover.png);'
                                                        '}')
        if click_alterar_colaboradores % 2 == 1:
            self.ui.line_senha_alterar_colaboradores.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.btn_ver_senha_alterar.setStyleSheet('QPushButton {'
                                                        'background-image: url(:/icones/bloquear senha.png);'
                                                        'border: 0px;'
                                                        'outline: 0;'
                                                        '}'
                                                        ''
                                                        'QPushButton:hover {'
                                                        'background-image: url(:/icones/bloquear senha hover.png);''}')

    # Funções para Atualizar Tabelas
    def AtualizaTabelasLogin(self):

        cursor.execute('SELECT * FROM login')
        banco_login = cursor.fetchall()

        self.ui.tabela_colaboradores.clear()
        self.ui.tabela_alterar_colaboradores.clear()

        row = 0
        self.ui.tabela_colaboradores.setRowCount(len(banco_login))
        self.ui.tabela_alterar_colaboradores.setRowCount(len(banco_login))

        colunas = ['Nome', 'Login', 'Senha']
        self.ui.tabela_colaboradores.setHorizontalHeaderLabels(colunas)
        self.ui.tabela_alterar_colaboradores.setHorizontalHeaderLabels(colunas)

        for pos, logins in enumerate(banco_login):
            self.ui.tabela_colaboradores.setItem(row, 0, QTableWidgetItem(logins[3]))
            self.ui.tabela_colaboradores.setItem(row, 1, QTableWidgetItem(logins[0]))
            self.ui.tabela_colaboradores.setItem(row, 2, QTableWidgetItem(logins[1]))

            self.ui.tabela_alterar_colaboradores.setItem(row, 0, QTableWidgetItem(logins[3]))
            self.ui.tabela_alterar_colaboradores.setItem(row, 1, QTableWidgetItem(logins[0]))
            self.ui.tabela_alterar_colaboradores.setItem(row, 2, QTableWidgetItem(logins[1]))

            row += 1

    def AtualizaTabelasClientes(self):
        cursor.execute('SELECT * FROM clientes')
        banco_clientes = cursor.fetchall()

        self.ui.tabela_clientes.clear()
        self.ui.tabela_alterar_clientes.clear()
        self.ui.tabela_cadastrar_clientes.clear()

        row = 0

        self.ui.tabela_clientes.setRowCount(len(banco_clientes))
        self.ui.tabela_alterar_clientes.setRowCount(len(banco_clientes))
        self.ui.tabela_cadastrar_clientes.setRowCount(len(banco_clientes))

        colunas = ['CPF', 'Nome', 'Endereço', 'Contato']
        self.ui.tabela_clientes.setHorizontalHeaderLabels(colunas)
        self.ui.tabela_alterar_clientes.setHorizontalHeaderLabels(colunas)
        self.ui.tabela_cadastrar_clientes.setHorizontalHeaderLabels(colunas)

        for clientes in banco_clientes:
            self.ui.tabela_clientes.setItem(row, 0, QTableWidgetItem(clientes[0]))
            self.ui.tabela_clientes.setItem(row, 1, QTableWidgetItem(clientes[1]))
            self.ui.tabela_clientes.setItem(row, 2, QTableWidgetItem(clientes[2]))
            self.ui.tabela_clientes.setItem(row, 3, QTableWidgetItem(clientes[3]))

            self.ui.tabela_alterar_clientes.setItem(row, 0, QTableWidgetItem(clientes[0]))
            self.ui.tabela_alterar_clientes.setItem(row, 1, QTableWidgetItem(clientes[1]))
            self.ui.tabela_alterar_clientes.setItem(row, 2, QTableWidgetItem(clientes[2]))
            self.ui.tabela_alterar_clientes.setItem(row, 3, QTableWidgetItem(clientes[3]))

            self.ui.tabela_cadastrar_clientes.setItem(row, 0, QTableWidgetItem(clientes[0]))
            self.ui.tabela_cadastrar_clientes.setItem(row, 1, QTableWidgetItem(clientes[1]))
            self.ui.tabela_cadastrar_clientes.setItem(row, 2, QTableWidgetItem(clientes[2]))
            self.ui.tabela_cadastrar_clientes.setItem(row, 3, QTableWidgetItem(clientes[3]))
            row += 1

    def AtualizaTabelasFornecedores(self):

        cursor.execute('SELECT * FROM fornecedores')
        banco_fornecedores = cursor.fetchall()

        self.ui.tabela_fornecedores.clear()
        self.ui.tabela_cadastrar_fornecedores.clear()
        self.ui.tabela_alterar_fornecedores.clear()

        row = 0

        self.ui.tabela_fornecedores.setRowCount(len(banco_fornecedores))
        self.ui.tabela_cadastrar_fornecedores.setRowCount(len(banco_fornecedores))
        self.ui.tabela_alterar_fornecedores.setRowCount(len(banco_fornecedores))

        colunas = ['Nome', 'Endereço', 'Contato']
        self.ui.tabela_fornecedores.setHorizontalHeaderLabels(colunas)
        self.ui.tabela_alterar_fornecedores.setHorizontalHeaderLabels(colunas)
        self.ui.tabela_cadastrar_fornecedores.setHorizontalHeaderLabels(colunas)

        for fornecedores in banco_fornecedores:
            self.ui.tabela_fornecedores.setItem(row, 0, QTableWidgetItem(fornecedores[0]))
            self.ui.tabela_fornecedores.setItem(row, 1, QTableWidgetItem(fornecedores[1]))
            self.ui.tabela_fornecedores.setItem(row, 2, QTableWidgetItem(fornecedores[2]))

            self.ui.tabela_alterar_fornecedores.setItem(row, 0, QTableWidgetItem(fornecedores[0]))
            self.ui.tabela_alterar_fornecedores.setItem(row, 1, QTableWidgetItem(fornecedores[1]))
            self.ui.tabela_alterar_fornecedores.setItem(row, 2, QTableWidgetItem(fornecedores[2]))

            self.ui.tabela_cadastrar_fornecedores.setItem(row, 0, QTableWidgetItem(fornecedores[0]))
            self.ui.tabela_cadastrar_fornecedores.setItem(row, 1, QTableWidgetItem(fornecedores[1]))
            self.ui.tabela_cadastrar_fornecedores.setItem(row, 2, QTableWidgetItem(fornecedores[2]))
            row += 1

    def AtualizaTabelasProdutos(self):
        cursor.execute('SELECT * FROM produtos')
        banco_produtos = cursor.fetchall()

        self.ui.tabela_produto.clear()
        self.ui.tabela_alterar_produto.clear()
        self.ui.tabela_cadastro.clear()

        row = 0

        self.ui.tabela_produto.setRowCount(len(banco_produtos))
        self.ui.tabela_alterar_produto.setRowCount(len(banco_produtos))
        self.ui.tabela_cadastro.setRowCount(len(banco_produtos))

        colunas = ['Item', 'Cód', 'Produto', 'Valor Unitário', 'Qtde', 'Fornecedor']
        self.ui.tabela_produto.setHorizontalHeaderLabels(colunas)
        self.ui.tabela_alterar_produto.setHorizontalHeaderLabels(colunas)
        self.ui.tabela_cadastro.setHorizontalHeaderLabels(colunas)



        for pos, produto in enumerate(banco_produtos):

            valor_unitario = lang.toString(int(produto[2]) * 0.01, 'f', 2)

            self.ui.tabela_produto.setItem(row, 0, QTableWidgetItem(f'{pos + 1}'))
            self.ui.tabela_produto.setItem(row, 1, QTableWidgetItem(produto[0]))
            self.ui.tabela_produto.setItem(row, 2, QTableWidgetItem(produto[1]))
            self.ui.tabela_produto.setItem(row, 3, QTableWidgetItem('R$ ' + valor_unitario))
            self.ui.tabela_produto.setItem(row, 4, QTableWidgetItem(produto[3]))
            self.ui.tabela_produto.setItem(row, 5, QTableWidgetItem(produto[4]))

            self.ui.tabela_alterar_produto.setItem(row, 0, QTableWidgetItem(f'{pos + 1}'))
            self.ui.tabela_alterar_produto.setItem(row, 1, QTableWidgetItem(produto[0]))
            self.ui.tabela_alterar_produto.setItem(row, 2, QTableWidgetItem(produto[1]))
            self.ui.tabela_alterar_produto.setItem(row, 3, QTableWidgetItem('R$ ' + valor_unitario))
            self.ui.tabela_alterar_produto.setItem(row, 4, QTableWidgetItem(produto[3]))
            self.ui.tabela_alterar_produto.setItem(row, 5, QTableWidgetItem(produto[4]))

            self.ui.tabela_cadastro.setItem(row, 0, QTableWidgetItem(f'{pos + 1}'))
            self.ui.tabela_cadastro.setItem(row, 1, QTableWidgetItem(produto[0]))
            self.ui.tabela_cadastro.setItem(row, 2, QTableWidgetItem(produto[1]))
            self.ui.tabela_cadastro.setItem(row, 3, QTableWidgetItem('R$ ' + valor_unitario))
            self.ui.tabela_cadastro.setItem(row, 4, QTableWidgetItem(produto[3]))
            self.ui.tabela_cadastro.setItem(row, 5, QTableWidgetItem(produto[4]))
            row += 1


class FrmColaborador(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_FrmColaborador()
        self.ui.setupUi(self)

        # Setando página home
        self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_home)

        # Configurando páginas e os botões do menu

        # Home
        self.ui.btn_home.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_home))

        # Vendas
        self.ui.btn_Vendas.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_vendas))

        # Produtos
        self.ui.btn_produtos.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_produtos))
        self.ui.btn_cadastrar_produto.clicked.connect(
            lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_cadastar_produtos))
        self.ui.btn_alterar_produto.clicked.connect(
            lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_alterar_produtos))

        # Tabela Produtos
        self.ui.tabela_produto.setColumnWidth(0, 50)
        self.ui.tabela_produto.setColumnWidth(1, 131)
        self.ui.tabela_produto.setColumnWidth(2, 250)
        self.ui.tabela_produto.setColumnWidth(3, 131)
        self.ui.tabela_produto.setColumnWidth(4, 75)
        self.ui.tabela_produto.setColumnWidth(5, 155)

        # Tabela Cadastrar Produtos
        self.ui.tabela_cadastro.setColumnWidth(0, 50)
        self.ui.tabela_cadastro.setColumnWidth(1, 165)
        self.ui.tabela_cadastro.setColumnWidth(2, 300)
        self.ui.tabela_cadastro.setColumnWidth(3, 165)
        self.ui.tabela_cadastro.setColumnWidth(4, 75)
        self.ui.tabela_cadastro.setColumnWidth(5, 250)

        # Tabela Alterar Produtos
        self.ui.tabela_alterar_produto.setColumnWidth(0, 50)
        self.ui.tabela_alterar_produto.setColumnWidth(1, 165)
        self.ui.tabela_alterar_produto.setColumnWidth(2, 300)
        self.ui.tabela_alterar_produto.setColumnWidth(3, 165)
        self.ui.tabela_alterar_produto.setColumnWidth(4, 75)
        self.ui.tabela_alterar_produto.setColumnWidth(5, 250)

        # Configurações
        self.ui.btn_configs.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_configuracoes))

        # Voltar
        self.ui.btn_voltar.clicked.connect(self.Voltar)

    def Voltar(self):
        global window

        window.close()
        window = FrmLogin()
        window.show()


if __name__ == '__main__':
    # Variáveis Globais
    click_cadastro_colaboradores = 0
    click_alterar_colaboradores = 0

    # Id para alterar os itens das tabelas
    id_tabela_alterar = None
    id_alterar_Clientes = None
    id_alterar_fornecedores = None
    id_alterar_produtos = None

    # Lista com os itens para fazer as previções das barras
    search_fornecedores = list()
    search_produtos = list()
    search_colaboradores = list()
    search_clientes = list()
    search_monitoramento = list()
    search_vendas = list()

    vendas = list()

    loc = QLocale.system().name()
    lang = QLocale(loc)

    # Var para pegar o nome de quem logou
    UserLogado = None

    StyleError = '''
               background-color: rgba(0, 0 , 0, 0);
               border: 2px solid rgba(0,0,0,0);
               border-bottom-color: rgb(255, 17, 49);;
               color: rgb(0,0,0);
               padding-bottom: 8px;
               border-radius: 0px;
               font: 10pt "Montserrat";'''

    StyleNormal = '''
                   background-color: rgba(0, 0 , 0, 0);
                   border: 2px solid rgba(0,0,0,0);
                   border-bottom-color: rgb(159,63,250);;
                   color: rgb(0,0,0);
                   padding-bottom: 8px;
                   border-radius: 0px;
                   font: 10pt "Montserrat";'''

    # Configurando Aplicação
    app = QApplication(sys.argv)
    window = FrmLogin()
    window.show()
    sys.exit(app.exec_())
