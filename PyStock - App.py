import os
import sys
import mysql.connector


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
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

        # Fornecedores
        self.ui.btn_fornecedores.clicked.connect(
            lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_fornecedores))

        # Vendas
        self.ui.btn_vendas.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_vendas))

        # Produtos
        self.ui.btn_produtos.clicked.connect(lambda: self.ui.Telas_do_menu.setCurrentWidget(self.ui.pg_produtos))

        # Voltar
        self.ui.btn_voltar.clicked.connect(self.Voltar)

    def Voltar(self):
        global window

        window.close()
        window = FrmLogin()
        window.show()


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
