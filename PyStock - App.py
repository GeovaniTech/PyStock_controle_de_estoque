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

        QMainWindow.__init__(self)

        self.ui = Ui_FrmAdmin()
        self.ui.setupUi(self)

        # Nome do User
        self.ui.lbl_seja_bem_vindo.setText(f'Seja Bem-Vindo(a) - {UserLogado}')
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

        # iniciando Hora e Data do Sistema
        tempo = QTimer(self)
        tempo.timeout.connect(self.HoraData)
        tempo.start(1000)

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

    def AlterarColaboradores(self):
        global id_tabela_alterar

        login = self.ui.line_login_alterar_colaboradores
        senha = self.ui.line_senha_alterar_colaboradores
        nome = self.ui.line_nome_alterar_colaboradores

        cursor.execute('SELECT * FROM login')
        banco_login = cursor.fetchall()

        if login.text() != '' and senha.text() != '' and nome.text() != '':

            LoginNoBanco = False

            for user in banco_login:
                if login.text() == user[0]:
                    LoginNoBanco = True

            for pos, user in enumerate(banco_login):
                if pos == id_tabela_alterar:
                    if LoginNoBanco == False:
                        cursor.execute(f'UPDATE login set usuario = "{login.text()}", senha = "{senha.text()}", nivel = "{user[2]}", nome = "{nome.text()}"'
                                       f'WHERE usuario = "{user[0]}"')
                        banco.commit()

                        login.clear()
                        senha.clear()
                        nome.clear()

                        self.AtualizaTabelasLogin()

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

            cpf.clear()
            nome.clear()
            endereco.clear()
            contato.clear()

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
                    cursor.execute(f'UPDATE clientes set CPF = "{cpf.text()}", nome = "{nome.text()}", endereço = "{endereco.text()}", contato = "{contato.text()}"'
                                   f'WHERE CPF = "{cliente[0]}"')

                    cpf.clear()
                    nome.clear()
                    endereco.clear()
                    contato.clear()

                    self.AtualizaTabelasClientes()

                    break

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
                    cursor.execute(f'UPDATE fornecedores set nome = "{nome.text()}", endereço = "{endereco.text()}", contato = "{contato.text()}"'
                                   f'WHERE nome = "{fornecedores[0]}"')

                    nome.clear()
                    endereco.clear()
                    contato.clear()

                    self.AtualizaTabelasFornecedores()
                    break

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

    id_tabela_alterar = None
    id_alterar_Clientes = None
    id_alterar_fornecedores = None

    UserLogado = None

    # Configurando Aplicação
    app = QApplication(sys.argv)
    window = FrmLogin()
    window.show()
    sys.exit(app.exec_())
