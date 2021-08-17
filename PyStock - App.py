import os
import sys
import mysql.connector

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from View.PY.FrmLogin import Ui_login
from View.PY.FrmAdmin import Ui_FrmAdmin
from View.PY.FrmColaborador import Ui_FrmColaborador

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

        self.ui.pushButton.clicked.connect(lambda: self.logar())

    def logar(self):

        global window

        cursor.execute("SELECT * FROM login")
        logins = cursor.fetchall()

        usuario = self.ui.lineEdit.text()
        senha = self.ui.lineEdit_2.text()

        print(f"Usuario inserido: {usuario}\n"
              f"Senha inserida: {senha}")

        for login in logins:

            if usuario != login[0]:
                self.ui.lineEdit.setStyleSheet('background-color: rgba(0, 0 , 0, 0);border: 2px solid rgba(0,0,0,0);'
                                               'border-bottom-color: rgb(255, 17, 49);color: rgb(0,0,0);padding-bottom: 8px;'
                                               'border-radius: 0px;font: 10pt "Montserrat";')

            if senha != login[1]:
                self.ui.lineEdit_2.setStyleSheet('background-color: rgba(0, 0 , 0, 0);border: 2px solid rgba(0,0,0,0);'
                                                 'border-bottom-color: rgb(255, 17, 49);color: rgb(0,0,0);padding-bottom: 8px;'
                                                 'border-radius: 0px;font: 10pt "Montserrat";')

            if usuario == login[0] and senha == login[1]:

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
        QMainWindow.__init__(self)

        self.ui = Ui_FrmAdmin()
        self.ui.setupUi(self)

        # Configurando páginas e os botões do menu

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

        self.ui.line_senha_alterar_colaboradores.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.btn_exluir_colaboradores.clicked.connect(self.ExcluirColaboradores)


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

        self.ui.tabela_colaboradores.clear()
        cursor.execute('SELECT * FROM login')
        banco_login = cursor.fetchall()

        row = 0
        self.ui.tabela_colaboradores.setRowCount(len(banco_login))
        self.ui.tabela_alterar_colaboradores.setRowCount(len(banco_login))

        colunas = ['Nome', 'Login', 'Senha']
        self.ui.tabela_colaboradores.setHorizontalHeaderLabels(colunas)
        self.ui.tabela_alterar_colaboradores.setHorizontalHeaderLabels(colunas)

        for logins in banco_login:
            self.ui.tabela_colaboradores.setItem(row, 0, QTableWidgetItem(logins[3]))
            self.ui.tabela_colaboradores.setItem(row, 1, QTableWidgetItem(logins[0]))
            self.ui.tabela_colaboradores.setItem(row, 2, QTableWidgetItem(logins[1]))

            self.ui.tabela_alterar_colaboradores.setItem(row, 0, QTableWidgetItem(logins[3]))
            self.ui.tabela_alterar_colaboradores.setItem(row, 1, QTableWidgetItem(logins[0]))
            self.ui.tabela_alterar_colaboradores.setItem(row, 2, QTableWidgetItem(logins[1]))

            row += 1

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

                self.ui.tabela_colaboradores.clear()
                cursor.execute('SELECT * FROM login')
                banco_login = cursor.fetchall()

                row = 0
                self.ui.tabela_colaboradores.setRowCount(len(banco_login))
                self.ui.tabela_alterar_colaboradores.setRowCount(len(banco_login))

                colunas = ['Nome', 'Login', 'Senha']
                self.ui.tabela_colaboradores.setHorizontalHeaderLabels(colunas)
                self.ui.tabela_alterar_colaboradores.setHorizontalHeaderLabels(colunas)

                for logins in banco_login:
                    self.ui.tabela_colaboradores.setItem(row, 0, QTableWidgetItem(logins[3]))
                    self.ui.tabela_colaboradores.setItem(row, 1, QTableWidgetItem(logins[0]))
                    self.ui.tabela_colaboradores.setItem(row, 2, QTableWidgetItem(logins[1]))

                    self.ui.tabela_alterar_colaboradores.setItem(row, 0, QTableWidgetItem(logins[3]))
                    self.ui.tabela_alterar_colaboradores.setItem(row, 1, QTableWidgetItem(logins[0]))
                    self.ui.tabela_alterar_colaboradores.setItem(row, 2, QTableWidgetItem(logins[1]))

                    row += 1

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
        print('Tentando Exluir')

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

        for logins in banco_login:
            self.ui.tabela_colaboradores.setItem(row, 0, QTableWidgetItem(logins[3]))
            self.ui.tabela_colaboradores.setItem(row, 1, QTableWidgetItem(logins[0]))
            self.ui.tabela_colaboradores.setItem(row, 2, QTableWidgetItem(logins[1]))

            self.ui.tabela_alterar_colaboradores.setItem(row, 0, QTableWidgetItem(logins[3]))
            self.ui.tabela_alterar_colaboradores.setItem(row, 1, QTableWidgetItem(logins[0]))
            self.ui.tabela_alterar_colaboradores.setItem(row, 2, QTableWidgetItem(logins[1]))

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
    click_cadastro_colaboradores = 0
    click_alterar_colaboradores = 0
    app = QApplication(sys.argv)
    window = FrmLogin()
    window.show()
    sys.exit(app.exec_())
