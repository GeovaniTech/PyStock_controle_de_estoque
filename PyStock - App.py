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

        # Iniciando na página inicial
        self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_home)

        ## Clique dos botões

        # Home
        self.ui.btn_home.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_home))

        # Cadastro de Colaboradores
        self.ui.btn_colaboradores.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_colaboradores))
        self.ui.btn_cadastro.clicked.connect(self.CadastroColaborador)
        
        # Fornecedores
        self.ui.btn_fornecedores.clicked.connect(
            lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_fornecedores))

        # Vendas
        self.ui.btn_vendas.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_vendas))

        # Produtos
        self.ui.btn_produtos.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_produtos))
        self.ui.btn_alterar_produto.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_alterar_produtos))
        self.ui.btn_cadastrar_produto.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_cadastar_produtos))

        # Voltar
        self.ui.btn_voltar.clicked.connect(self.Voltar)

        ## Ajustando Tabelas

        # Ajustando Largura das Colunas da Tabela Vendas
        self.ui.tabela_vendas.setColumnWidth(0, 45)
        self.ui.tabela_vendas.setColumnWidth(1, 125)
        self.ui.tabela_vendas.setColumnWidth(2, 250)
        self.ui.tabela_vendas.setColumnWidth(3, 150)
        self.ui.tabela_vendas.setColumnWidth(4, 45)
        self.ui.tabela_vendas.setColumnWidth(5, 175)

        # Ajustando Largura das Colunas da Tabela Produtos

        self.ui.tabela_produto.setColumnWidth(0, 45)
        self.ui.tabela_produto.setColumnWidth(1, 125)
        self.ui.tabela_produto.setColumnWidth(2, 250)
        self.ui.tabela_produto.setColumnWidth(3, 150)
        self.ui.tabela_produto.setColumnWidth(4, 45)
        self.ui.tabela_produto.setColumnWidth(5, 175)

        # Ajustando Largura das Colunas da Tabela Cadastrar Produtos

        self.ui.tabela_cadastro.setColumnWidth(0, 45)
        self.ui.tabela_cadastro.setColumnWidth(1, 125)
        self.ui.tabela_cadastro.setColumnWidth(2, 350)
        self.ui.tabela_cadastro.setColumnWidth(3, 150)
        self.ui.tabela_cadastro.setColumnWidth(4, 45)
        self.ui.tabela_cadastro.setColumnWidth(5, 300)

        # Ajustando Largura das Colunas da Tabela Altearar Produtos

        self.ui.tabela_alterar.setColumnWidth(0, 45)
        self.ui.tabela_alterar.setColumnWidth(1, 125)
        self.ui.tabela_alterar.setColumnWidth(2, 350)
        self.ui.tabela_alterar.setColumnWidth(3, 150)
        self.ui.tabela_alterar.setColumnWidth(4, 45)
        self.ui.tabela_alterar.setColumnWidth(5, 300)

        # Ajustando Largura das Colunas da Tabela Produtos

        self.ui.tabela_fornecedores.setColumnWidth(0, 330)
        self.ui.tabela_fornecedores.setColumnWidth(1, 330)
        self.ui.tabela_fornecedores.setColumnWidth(2, 331)

    def Voltar(self):
        global window

        window.close()
        window = FrmLogin()
        window.show()

    def CadastroColaborador(self):
        
        nome = self.ui.line_nome
        login = self.ui.line_login
        senha = self.ui.line_senha

        if nome.text() == "":
            nome.setStyleSheet('background-color: rgba(0, 0 , 0, 0);border: 2px solid rgba(0,0,0,0);'
                                            'border-bottom-color: rgb(255, 17, 49);color: rgb(0,0,0);padding-bottom: 8px;'
                                            'border-radius: 0px;font: 10pt "Montserrat";')
        if login.text() == "":
            login.setStyleSheet('background-color: rgba(0, 0 , 0, 0);border: 2px solid rgba(0,0,0,0);'
                                            'border-bottom-color: rgb(255, 17, 49);color: rgb(0,0,0);padding-bottom: 8px;'
                                            'border-radius: 0px;font: 10pt "Montserrat";')
        
        if senha.text() == "":
            senha.setStyleSheet('background-color: rgba(0, 0 , 0, 0);border: 2px solid rgba(0,0,0,0);'
                                                'border-bottom-color: rgb(255, 17, 49);color: rgb(0,0,0);padding-bottom: 8px;'
                                                'border-radius: 0px;font: 10pt "Montserrat";')
        
        elif self.ui.radio_colaborador.isChecked() == False and self.ui.radio_admin.isChecked() == False:
            self.popup()
        
        elif nome.text() != "" and login.text() != "" and senha.text() != "":
            cursor.execute('SELECT * FROM login')
            banco_login = cursor.fetchall()

            for user in banco_login:

                if user[0] != login.text():

                    if self.ui.radio_admin.isChecked() == True:
                        comando_SQL = 'INSERT INTO login (usuario, senha, nivel, nome) VALUES (%s,%s,%s,%s)'
                        dados = (f"{login.text()}", f"{senha.text()}", "admin", f"{nome.text()}")
                        cursor.execute(comando_SQL, dados)
                        banco.commit()

                    if self.ui.radio_colaborador.isChecked() == True:
                        comando_SQL = 'INSERT INTO login (usuario, senha, nivel, nome) VALUES (%s,%s,%s,%s)'
                        dados = (f"{login.text()}", f"{senha.text()}", "colaborador", f"{nome.text()}")
                        cursor.execute(comando_SQL, dados)
                        banco.commit()


    def popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Erro - Cadastro de Colaboradores")
        msg.setText('Selecione um Nível de Usuário!')

        x = msg.exec_()
            

class FrmColaborador(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_FrmColaborador()
        self.ui.setupUi(self)

        # Iniciando na página inicial
        self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_home)

        ## Clique dos botões

        # Home
        self.ui.btn_home.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_home))

        # Fornecedores
        self.ui.btn_fornecedores.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_fornecedores))

        # Vendas
        self.ui.btn_vendas.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_vendas))

        # Produtos
        self.ui.btn_produtos.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_produtos))

        # Voltar
        self.ui.btn_voltar.clicked.connect(self.Voltar)

        ## Ajustando Tabelas

        # Ajustando Largura das Colunas da Tabela Vendas

        self.ui.tabela_vendas.setColumnWidth(0, 45)
        self.ui.tabela_vendas.setColumnWidth(1, 125)
        self.ui.tabela_vendas.setColumnWidth(2, 250)
        self.ui.tabela_vendas.setColumnWidth(3, 150)
        self.ui.tabela_vendas.setColumnWidth(4, 45)
        self.ui.tabela_vendas.setColumnWidth(5, 175)

        # Ajustando Largura das Colunas da Tabela Produtos

        self.ui.tabela_produto.setColumnWidth(0, 45)
        self.ui.tabela_produto.setColumnWidth(1, 125)
        self.ui.tabela_produto.setColumnWidth(2, 250)
        self.ui.tabela_produto.setColumnWidth(3, 150)
        self.ui.tabela_produto.setColumnWidth(4, 45)
        self.ui.tabela_produto.setColumnWidth(5, 175)

        # Ajustando Largura das Colunas da Tabela Produtos

        self.ui.tabela_fornecedores.setColumnWidth(0, 330)
        self.ui.tabela_fornecedores.setColumnWidth(1, 330)
        self.ui.tabela_fornecedores.setColumnWidth(2, 331)

    def Voltar(self):
        global window

        window.close()
        window = FrmLogin()
        window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FrmLogin()
    window.show()
    sys.exit(app.exec_())
